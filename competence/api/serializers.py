from rest_framework import serializers

from competence.models import Company, Competence, QuotationSession


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'name']
        read_only_fields = ["id"]


class CompanySerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='company', lookup_field="slug")

    class Meta:
        model = Company
        fields = ['id', 'name', 'url', 'competences']
        read_only_fields = ["id", "url", "competences"]


class QuotationSessionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    competence = CompetenceSerializer()

    class Meta:
        model = QuotationSession
        fields = "__all__"
