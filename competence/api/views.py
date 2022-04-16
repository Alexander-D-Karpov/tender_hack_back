from rest_framework import generics
from rest_framework.permissions import AllowAny

from competence.api.serializers import (
    CompanySerializer,
    GetQuotationSessionSerializer,
    CreateQuotationSessionSerializer, CompanyCreateSerializer,
)
from competence.models import Company, QuotationSession


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Company.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanySerializer
        else:
            return CompanyCreateSerializer


class CompanyView(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Company.objects.filter(slug=self.kwargs["slug"])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanySerializer
        else:
            return CompanyCreateSerializer


class QuotationSessionListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return QuotationSession.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetQuotationSessionSerializer
        else:
            return CreateQuotationSessionSerializer
