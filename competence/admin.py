from django.contrib import admin

# Register your models here.
from competence.models import Company, Competence, CompanyCompetence

admin.site.register(Company)
admin.site.register(Competence)
admin.site.register(CompanyCompetence)
