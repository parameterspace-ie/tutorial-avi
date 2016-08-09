from rest_framework import serializers
from avi.models import TutorialModel


class TutorialModelSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = TutorialModel
        fields = '__all__'
        depth = 2