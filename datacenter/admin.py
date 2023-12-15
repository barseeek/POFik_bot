from django.contrib import admin
from datacenter.models import Bonus
from datacenter.models import Transaction

admin.site.register(Bonus)
admin.site.register(Transaction)

class BonusAdmin(admin.ModelAdmin):
    list_display = ["name", "cost", "photo"]
