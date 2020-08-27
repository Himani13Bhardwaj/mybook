from rest_framework import serializers
from userprofile.models import UserProfile

# User Profile
# ------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
