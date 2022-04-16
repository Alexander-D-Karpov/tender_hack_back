from rest_framework import serializers

from competence.models import Company, Competence


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'name']


class CompanySerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='company', lookup_field="slug")

    class Meta:
        model = Company
        fields = ['id', 'name', 'url', 'competences']
        read_only_fields = ["id", "url", "competences"]
