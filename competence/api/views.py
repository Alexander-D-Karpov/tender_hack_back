from rest_framework import generics, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from competence.api.serializers import (
    CompanySerializer,
    CreateQuotationSessionSerializer,
    CompanyCreateSerializer, CompetenceSerializer, FullQuotationSessionSerializer, QuotationSessionSerializer,
    CompanyQuotationSessionSerializer,
)
from competence.models import Company, QuotationSession, Competence, CompanyCompetence, CompanyQuotationSession


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Company.objects.all()
        return queryset

    def get_object(self):
        if self.request.method == "PUT":
            company = Company.objects.filter(slug=self.kwargs["slug"]).first()
            if company:
                return company
            else:
                return Company(slug=self.kwargs["slug"])

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanySerializer
        else:
            return CompanyCreateSerializer


class CompanyView(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(slug=self.kwargs["slug"])

    def perform_create(self, serializer):
        serializer.save()

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
            return QuotationSessionSerializer
        else:
            return CreateQuotationSessionSerializer


class CompetenceListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CompetenceSerializer
    queryset = Competence.objects.all()


class CompetenceCompanyView(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return [x.company for x in CompanyCompetence.objects.filter(competence_id=self.kwargs["id"])]


class QuotationSessionView(generics.ListAPIView):
    pagination_class = None
    serializer_class = FullQuotationSessionSerializer

    def get_queryset(self):
        return QuotationSession.objects.filter(id=self.kwargs["id"])


class CompanyQuotationSessionView(viewsets.ModelViewSet, UpdateAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)

    queryset = CompanyQuotationSession.objects.all()
    serializer_class = CompanyQuotationSessionSerializer

    def get_queryset(self):
        return CompanyQuotationSession.objects.filter(id=self.kwargs["id"])

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        return CompanyQuotationSessionSerializer


