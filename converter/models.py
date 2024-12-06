from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=255, verbose_name="Валюта")

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return f"{self.name} ({self.code})"


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="base_rates",
        verbose_name="Исходная валюта"
    )
    target_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="target_rates",
        verbose_name="Целевая валюта"
    )
    rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс валюты")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    class Meta:
        verbose_name = 'Курс обмена'
        verbose_name_plural = 'Курсы обмена'

    def __str__(self):
        return f"1 {self.base_currency.code} = {self.rate} {self.target_currency.code}"
