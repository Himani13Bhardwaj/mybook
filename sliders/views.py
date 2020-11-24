from django.shortcuts import render
from rest_framework.views import APIView
from sliders.models import Sliders
from sliders.api.serializers import SliderSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
# Create your views here.
class SliderView(APIView):
    
    model = Sliders

    def get(self, request):
        slider_list = Sliders.objects.all().order_by('type_slider')
        serialzer = SliderSerializer(slider_list, context={"request": request}, many=True)
        return Response(serialzer.data)
