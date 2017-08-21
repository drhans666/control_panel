from django.db import models
from datetime import date
from django.core.validators import MinValueValidator


class Vacation(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(default='???', max_length=30)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    vac_days = models.IntegerField(verbose_name='Vacation days to use:', default=0,
                                   validators=[MinValueValidator(1)])
    accepted = models.BooleanField(default=False)
