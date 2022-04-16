from rest_framework import generics
from rest_framework.permissions import AllowAny

from competence.api.serializers import CompanySerializer, QuotationSessionSerializer
from competence.models import Company, QuotationSession


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)


class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Company.objects.filter(slug=self.kwargs['slug'])
        return queryset


class QuotationSessionListCreateView(generics.ListCreateAPIView):
    queryset = QuotationSession.objects.all()
    serializer_class = QuotationSessionSerializer
    permission_classes = (AllowAny,)
