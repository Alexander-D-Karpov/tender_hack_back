from django.urls import path

from competence.api import views

urlpatterns = [
    path('companies/', views.CompanyListCreateView.as_view(), name='company_list'),
    path('companies/<str:slug>', views.CompanyView.as_view(), name='company')
]
