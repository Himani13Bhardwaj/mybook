from rest_framework import serializers
from comment.models import Comments


# Comments
# ------------------------------------------------
class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'