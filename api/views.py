from django.shortcuts import render
from rest_framework import viewsets
from api.models import *
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class Student_view(viewsets.ViewSet):
    def list(self,request):
        stu=Student.objects.all()
        serial=StudentSerializer(stu,many=True)
        return Response({'data':serial.data})

    def create(self,request):
        serial=StudentSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'data':'Data Created'})
        else:
            return Response({'data':'some error occurred'})
        
    def retrieve(self,request,pk=None):
        id=pk
        if id is not None:
            stu=Student.objects.get(id=id)
            serial=StudentSerializer(stu)
            return Response({'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'data':serial.errors})
        
    def update(self,request,pk):
        id=pk
        stu=Student.objects.get(pk=id)
        serial=StudentSerializer(stu,data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'data':serial.data})
        else:
            return Response({'data':serial.errors})
        
    def partial_update(self,request,pk=None):
        id=pk
        stu=Student.objects.get(id=pk)
        serial=StudentSerializer(stu,data=request.data,partial=True)
        if serial.is_valid():
            serial.save()
            return Response({'data':serial.data})
    def destroy(self,request,pk):
        id=pk
        stu=Student.objects.get(pk=id)
        stu.delete()
        return Response({'data':'data deleted successfullY!'})







    


    
