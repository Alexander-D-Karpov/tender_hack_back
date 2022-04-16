from django.db import models

# Create your models here.
from django.urls import reverse

from common.gen_slug import gen_int_slug


class Competence(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=8, blank=True, unique=True)

    def competences(self) -> list[Competence]:
        return [x.competence for x in CompanyCompetence.objects.filter(provider=self)]

    def get_absolute_url(self) -> str:
        return reverse("provider", kwargs={"slug": self.slug})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            slug = gen_int_slug(8)
            while Company.objects.filter(slug=slug).exists():
                slug = gen_int_slug(8)
            self.slug = slug
            super(Company, self).save()

    def __str__(self):
        return self.name


class CompanyCompetence(models.Model):
    provider = models.ForeignKey(Company, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)

    def __str__(self):
        return self.provider.name + " " + self.competence.name


QUOTATION_SESSIONS_LIST = [
    ("in_process", "В процессе"),
    ("finished", "Закончена")
]


class QuotationSession(models.Model):
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)
    documentation = models.FileField(upload_to="uploads/docs")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=QUOTATION_SESSIONS_LIST, default="in_process")

