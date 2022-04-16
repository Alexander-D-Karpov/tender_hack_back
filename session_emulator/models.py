from django.db import models

from competence.models import QuotationSession, Company


class Lot(models.Model):
    quotation_session = models.ForeignKey(QuotationSession, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    class Meta:
        ordering = ('time',)
