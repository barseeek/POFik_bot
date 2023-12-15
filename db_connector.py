import environs
import mariadb
import pandas as pd


env = environs.Env()
env.read_env()

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
    cur.execute("SELECT ID, PARENT_ID, TYPE, EMP_TYPE, NAME, DESCRIPTION, POS, TABID, STATUS, CREATEDTIME, FIREDTIME, EXTSOURCEID FROM personal")
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
