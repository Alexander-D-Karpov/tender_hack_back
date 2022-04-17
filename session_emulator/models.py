from django.core.validators import MinValueValidator
from django.db import models

from competence.models import CompanyQuotationSession


class Lot(models.Model):
    comp_quotation_session = models.ForeignKey(
        CompanyQuotationSession, on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=False, validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ("time",)

    def __str__(self):
        return self.comp_quotation_session.company.name + " " + str(self.price)
