from django.contrib import admin
from .models import Currency, ExchangeRate

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'target_currency', 'rate', 'last_update')
