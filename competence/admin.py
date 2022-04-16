from django.contrib import admin

# Register your models here.
from competence.models import (
    Company,
    Competence,
    CompanyCompetence,
    QuotationSession,
)


@admin.register(Company)
class RateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)


@admin.register(Competence)
class RateAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)


@admin.register(CompanyCompetence)
class RateAdmin(admin.ModelAdmin):
    list_display = ("company", "competence")
    list_filter = ("company", "competence")
    search_fields = ("company", "competence")


@admin.register(QuotationSession)
class RateAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "status", "product_amount", "competence")
    list_filter = ("company", "status", "competence")
    search_fields = ("name", "competence")

