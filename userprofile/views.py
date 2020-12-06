from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from userprofile.models import UserProfile
from userprofile.api.serializers import UserProfileSerializer
from account.api.serializers import AccountPropertiesSerializer

# Create your views here.
# User Profile    
# ------------------------------------------------
class UserProfileView(APIView):

    model = UserProfile
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            user_activity_list = UserProfile.objects.get(user_id=request.user.id)
            data = {}
            print(request.user, type(request.user))
            serialzer = UserProfileSerializer(user_activity_list)
            data['userprofile'] = serialzer.data
            data['user'] = AccountPropertiesSerializer(
                request.user
                ).data
            return Response(data)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile is not created. Kindly login first'})

    def post(self, request):
        serialzer = UserProfileSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCoinsView(APIView):
    
    model = UserProfile
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_activity_list = UserProfile.objects.all()
        serialzer = UserProfileSerializer(user_activity_list, many=True)
        return Response(serialzer.data)

    def patch(self, request):
        coin = request.data.get('coins')

        if request.user is not None:
            userprofile = UserProfile.objects.get(user_id = request.user)
            if userprofile is not None:
                userprofile.coins =  int(userprofile.coins) + int(coin)
                userprofile.save()
                return Response({'message':'added the coins', 'login': True, 'valid': True})
            return Response({'message':'Kindly create the profile with coins', 'login': False})
        return Response({'message':'No Such user exist. Kindly login first.', 'login': False})
