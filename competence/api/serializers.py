from rest_framework import serializers

from competence.models import Company, Competence, QuotationSession, CompanyCompetence, CompanyQuotationSession


class CompetenceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competence", lookup_field="id", allow_empty=True
    )

    class Meta:
        model = Competence
        fields = ["id", "url", "name"]
        read_only_fields = ["id", "url"]


class GetCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ["id"]


class QuotationSessionSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name="quotation", lookup_field="id"
    )

    class Meta:
        model = QuotationSession
        fields = ["name", "start_price", "time", "description", "documentation", "url", "product_amount", "competence"]
        read_only_fields = ["time"]


class CompanySerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="company", lookup_field="slug", allow_empty=True
    )
    quotations = QuotationSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "url",
            "competences",
            "quotations",
        ]
        read_only_fields = [
            "id",
            "url",
            "competences",
            "quotations",
        ]
        depth = 1


class CompanyQuotationSessionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name="company_quotation", lookup_field="id"
    )

    class Meta:
        model = CompanyQuotationSession
        fields = ["company", "is_bot", "min_cost", "url"]
        read_only_fields = ["company", "url"]


class FullQuotationSessionSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer()
    company = CompanySerializer()
    participants = CompanyQuotationSessionSerializer(many=True)

    class Meta:
        model = QuotationSession
        fields = ["name", "start_price", "time", "description", "documentation", "company", "status", "product_amount", "competence",
                  "participants"]


class CompanyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)
    competences = serializers.ListSerializer(
        child=serializers.IntegerField(),
        write_only=True,
        allow_null=True,
        allow_empty=True,
    )

    def to_representation(self, instance):
        representation = CompanySerializer(
            instance, context={"request": self.context["request"]}
        )
        return representation.data

    def create(self, validated_data):
        company = Company.objects.create(
            name=validated_data["name"],
        )
        for x in validated_data["competences"]:
            if Competence.objects.filter(id=x).exists():
                CompanyCompetence.objects.create(company=company, competence_id=x)
        return company


class CreateQuotationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationSession
        fields = "__all__"
