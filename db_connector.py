import environs
import mariadb
import pandas as pd
import os
from datacenter.models import Department

env = environs.Env()
env.read_env()


def get_personal():
    try:
        conn = mariadb.connect(
            user=env.str("MARIADB_USERNAME"),
            password=env.str("MARIADB_PASSWORD"),
            host=env.str("MARIADB_HOST"),
            port=env.int("MARIADB_PORT"),
            database=env.str("MARIADB_NAME")
        )

        cur = conn.cursor()

        # Выполнение SQL-запроса
        cur.execute("SELECT ID, PARENT_ID, TYPE, EMP_TYPE, NAME, POS, TABID, STATUS FROM personal WHERE STATUS = 'AVAILABLE'")
        results = cur.fetchall()

        # Создание DataFrame из результатов запроса
        df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])

        # Запись в Excel файл
        df.to_excel('personal.xlsx', index=False)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    finally:
        if 'conn' in locals() and conn:
            cur.close()
            conn.close()


def insert_departments(file_path):
    df = pd.read_excel(file_path)
    exists_id = [0]
    # Создание объектов моделей Django и сохранение их в базу данных
    for index, row in df.iterrows():
        print(row)
        exists_id.append(int(row['ID']))
        if row['TYPE'] == 'DEP' and int(row['PARENT_ID']) in exists_id:  # Проверка типа департамента
            department = Department(
                id=int(row['ID']),
                name=row['NAME'],
                parent=Department.objects.get(pk=int(row['PARENT_ID'])) if int(row['PARENT_ID']) else None
                # ... другие поля модели
            )
            department.save()
