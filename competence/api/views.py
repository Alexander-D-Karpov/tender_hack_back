from rest_framework import generics, viewsets
from rest_framework.generics import (
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    get_object_or_404,
    GenericAPIView,
)
from rest_framework.permissions import AllowAny
from competence.api.serializers import (
    CompanySerializer,
    CreateQuotationSessionSerializer,
    CompanyCreateSerializer,
    CompetenceSerializer,
    FullQuotationSessionSerializer,
    QuotationSessionSerializer,
    CompanyQuotationSessionSerializer,
    CompanyPriceMinSerializer,
)
from competence.models import (
    Company,
    QuotationSession,
    Competence,
    CompanyCompetence,
    CompanyQuotationSession,
    CompanyPriceMin,
)


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
        return [
            x.company
            for x in CompanyCompetence.objects.filter(competence_id=self.kwargs["id"])
        ]


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
    lookup_field = "id"

    def get_queryset(self):
        return CompanyQuotationSession.objects.filter(id=self.kwargs["id"])

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        return CompanyQuotationSessionSerializer


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class CompanyPriceMinView(
    MultipleFieldLookupMixin,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
):
    serializer_class = CompanyPriceMinSerializer
    queryset = CompanyPriceMin.objects.all()

    lookup_fields = ["quotation_session_id", "company__slug"]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
