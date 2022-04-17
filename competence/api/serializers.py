from rest_framework import serializers

from competence.models import Company, Competence, QuotationSession, CompanyCompetence


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
        view_name="quotation", lookup_field="id", allow_empty=True
    )

    class Meta:
        model = QuotationSession
        fields = ["name", "description", "documentation", "url", "product_amount", "competence"]


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
            "is_bot",
            "min_cost",
            "name",
            "url",
            "competences",
            "quotations",
        ]
        read_only_fields = [
            "id",
            "is_bot",
            "min_cost",
            "url",
            "competences",
            "quotations",
        ]
        depth = 1


class FullQuotationSessionSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer()
    company = CompanySerializer()
    participants = CompanySerializer(many=True)

    class Meta:
        model = QuotationSession
        fields = ["name", "description", "documentation", "company", "status", "product_amount", "competence", "participants"]


class CompanyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)
    is_bot = serializers.BooleanField(default=False)
    min_cost = serializers.IntegerField(min_value=0)
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
            is_bot=validated_data["is_bot"],
            min_cost=validated_data["min_cost"],
        )
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
