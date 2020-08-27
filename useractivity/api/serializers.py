from rest_framework import serializers
from useractivity.models import UserActivity

# UserActivity
# ------------------------------------------------
class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = '__all__'
