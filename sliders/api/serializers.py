from rest_framework import serializers
from sliders.models import Sliders

# UserActivity
# ------------------------------------------------
class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sliders
        fields = '__all__'
