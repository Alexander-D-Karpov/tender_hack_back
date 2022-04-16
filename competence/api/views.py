from rest_framework import generics
from rest_framework.permissions import AllowAny

from competence.api.serializers import CompanySerializer
from competence.models import Company


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)


class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Company.objects.filter(slug=self.kwargs['slug'])
        return queryset
