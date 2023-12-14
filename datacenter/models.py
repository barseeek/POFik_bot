from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    head = models.OneToOneField('Employee', on_delete=models.SET_NULL, related_name='organization_head', null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.OneToOneField('Employee', on_delete=models.SET_NULL, related_name='department_head', null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class Bonus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.IntegerField()
    photo = models.ImageField(upload_to='bonus_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    telegram_id = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    mmpof_login = models.CharField(max_length=100)
    pofik_count = models.IntegerField(default=0)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='employees', null=False, blank=True)
    balance = models.IntegerField(default=0)

    def recharge_balance(self, amount):
        self.balance += amount
        self.save()

    def give_coins(self, recipient, amount):
        if self.balance >= amount:
            transaction = Transaction.objects.create(sender=self, recipient=recipient, amount=amount, transaction_type="Giveaway")
            self.balance -= amount
            recipient.balance += amount
            self.save()
            recipient.save()
            transaction.save()
        else:
            # Действие в случае недостаточного баланса
            pass

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Transaction(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)  # Тип транзакции: "Giveaway", "Purchase", и т.д.
    amount = models.IntegerField()
    bonus = models.ForeignKey('Bonus', on_delete=models.CASCADE, related_name='related_transactions', blank=True, null=True)
    trans_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        if self.transaction_type == "Purchase" and self.bonus:
            self.amount = -self.bonus.cost  # Отрицательная сумма для покупки бонуса
        super().save()

    def __str__(self):
        return f"{self.employee.firstname} - {self.transaction_type}"
