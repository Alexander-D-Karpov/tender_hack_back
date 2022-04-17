from django.urls import path

from competence.api import views

urlpatterns = [
    path("companies/", views.CompanyListCreateView.as_view(), name="company_list"),
    path(
        "companies/quotations/<int:id>",
        views.CompanyQuotationSessionView.as_view({"get": "list", "post": "create"}),
        name="company_quotation",
    ),
    path(
        "companies/<str:slug>",
        views.CompanyView.as_view({"get": "list", "post": "create"}),
        name="company",
    ),
    path(
        "companies/<str:company__slug>/<int:quotation_session_id>",
        views.CompanyPriceMinView.as_view(),
        name="company",
    ),
    path(
        "quotations/",
        views.QuotationSessionListCreateView.as_view(),
        name="quotation_list",
    ),
    path(
        "quotations/<int:id>",
        views.QuotationSessionView.as_view(),
        name="quotation",
    ),
    path(
        "competence/",
        views.CompetenceListCreateView.as_view(),
        name="competence_list",
    ),
    path(
        "competence/<int:id>",
        views.CompetenceCompanyView.as_view(),
        name="competence",
    ),
]
