from django.contrib import admin

from datacenter.models import Bonus
from datacenter.models import Transaction
from datacenter.models import Department


admin.site.register(Transaction)


class BonusAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "photo")


admin.site.register(Bonus)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'parent')  # Указываем поля, которые вы хотите отображать в админке
    # Добавьте другие настройки, если необходимо


admin.site.register(Department, DepartmentAdmin)
