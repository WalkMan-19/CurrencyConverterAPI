from django.contrib import admin

from converter.models import Currency, ExchangeRate

admin.site.register(Currency)
admin.site.register(ExchangeRate)
