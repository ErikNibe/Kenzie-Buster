from rest_framework import serializers
from movies.models import Movie
from movies.models import RatingChoices


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(
        allow_null=True, choices=RatingChoices.choices, default=RatingChoices.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)

    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
