from rest_framework import serializers
from usercollection.models import UserCollection

# User Collection
# ------------------------------------------------
class UserCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCollection
        fields = '__all__'

