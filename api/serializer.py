from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from project.models import Project , Tags , Review
from users.models import Userprofile


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class UserprofileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = '__all__'

class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class ProjectSerializers(serializers.ModelSerializer):
    owner = UserprofileSerializers(many=False)
    tags = TagsSerializers(many=False)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self , obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializers(reviews , many = True)

        return serializer.data

