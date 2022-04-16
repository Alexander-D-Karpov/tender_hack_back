from rest_framework import serializers

from competence.models import Company, Competence, QuotationSession, CompanyCompetence


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ["id", "name"]
        read_only_fields = ["id"]


class GetCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ["id"]


class QuotationSessionSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer()

    class Meta:
        model = QuotationSession
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="company", lookup_field="slug")
    quotations = QuotationSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "url", "competences", "quotations"]
        read_only_fields = ["id", "url", "competences", "quotations"]
        depth = 1


class CompanyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)
    competences = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True)

    def create(self, validated_data):
        company = Company.objects.create(name=validated_data["name"])
        for x in validated_data["competences"]:
            if Competence.objects.filter(id=x).exists():
                CompanyCompetence.objects.create(company=company, competence_id=x)
        return company


class GetQuotationSessionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    competence = CompetenceSerializer()

    class Meta:
        model = QuotationSession
        fields = "__all__"
        depth = 1


class CreateQuotationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationSession
        fields = "__all__"
