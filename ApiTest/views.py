from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import jwt,datetime
from .models import People,Movie
from django.core import serializers
from .serializers import PeopleSerializer,MovieSerializer
import json


@api_view(['POST'])
def register(request):
    if request.method == 'POST': 
        try:
            validate_email(request.data["email"])
            print(len(request.data["password"]))
            serializer = PeopleSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    people = People.objects.get(email = request.data["email"])
                    return Response("email already registered", status = status.HTTP_400_BAD_REQUEST)
                except:
                    if(len(request.data["password"])<10):
                        return Response("password shoud contains at least 10 characters", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.isupper() for char in request.data["password"])):
                        return Response("password shoud at least contains one uppercase", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.islower() for char in request.data["password"])):
                        return Response("password shoud at least contains one lowercase", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char in ['$', '@', '#', '%'] for char in request.data["password"])):
                        return Response("password shoud at least contains $, @, # or %", status = status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)    
        except ValidationError:
            return Response("not valid email", status = status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        try:
            validate_email(request.data["email"])
            try:
                    people = People.objects.get(email = request.data["email"])
                    if(len(request.data["password"])<10):
                        return Response("password shoud contains at least 10 characters", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.isupper() for char in request.data["password"])):
                        return Response("password shoud at least contains one uppercase", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.islower() for char in request.data["password"])):
                        return Response("password shoud at least contains one lowercase", status = status.HTTP_400_BAD_REQUEST)
                    elif (not any(char in ['$', '@', '#', '%'] for char in request.data["password"])):
                        return Response("password shoud at least contains $, @, # or %", status = status.HTTP_400_BAD_REQUEST)
                    else:
                        if(request.data["password"]==people.password):
                            payload = {
                                'email':people.email,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
                                'iat': datetime.datetime.utcnow()
                            }
                            token = jwt.encode(payload,'secret',algorithm='HS256')
                            return Response({'jwt':token}, status = status.HTTP_200_OK)
                        else:
                            return Response("password is not correct", status = status.HTTP_400_BAD_REQUEST)        
            except:
                return Response("email not register", status = status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response("not valid email", status = status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def addItem(request):
    if request.method == 'POST':
        token = request.headers['Token']
        if not token:
            return Response("Unauthorized", status = status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
                try:
                    m = Movie(name = request.data['name'],
                              gender= request.data['gender'],
                              duration= request.data['duration'],
                              objectType = request.data['objectType'],
                              clasification = request.data['clasification'],
                              creatorEmail = payload['email'])
                    m.save()
                    return Response(payload, status = status.HTTP_200_OK)
                except:
                    return Response("invalid JSON", status = status.HTTP_400_BAD_REQUEST)
            except jwt.ExpiredSignatureError:
                return Response("token expired", status = status.HTTP_401_UNAUTHORIZED)
            
def obj_dict(obj):
    return obj.__dict__

@api_view(['GET'])
def getPublicList(request):
    if request.method == 'GET':           
        token = request.headers['Token']
        if not token:
            return Response("Unauthorized", status = status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
                movie_list = Movie.objects.filter(objectType = 'public').values()
                return JsonResponse({ "movies": list(movie_list)}, status = status.HTTP_200_OK,safe=False)
            except jwt.ExpiredSignatureError:
                return Response("token expired", status = status.HTTP_401_UNAUTHORIZED)
            
@api_view(['GET'])
def getPrivateList(request):
    if request.method == 'GET':           
        token = request.headers['Token']
        if not token:
            return Response("Unauthorized", status = status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
                movie_list = Movie.objects.filter(objectType = 'private', creatorEmail=payload['email']).values()
                return JsonResponse({ "movies": list(movie_list)}, status = status.HTTP_200_OK,safe=False)
            except jwt.ExpiredSignatureError:
                return Response("token expired", status = status.HTTP_401_UNAUTHORIZED)


           
@api_view(['POST'])
def editMovie(request):
    if request.method == 'POST':                     
        token = request.headers['Token']
        if not token:
            return Response("Unauthorized", status = status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
                movie = Movie.objects.filter(id=request.data['id'])[0]
                if(movie.creatorEmail == payload['email'] and movie.objectType == 'private'):
                    movie.name = request.data['name']
                    movie.gender = request.data['gender']
                    movie.duration = request.data['duration']
                    movie.clasification = request.data['clasification']
                    movie.save()
                    return Response("Update Successfull",status=status.HTTP_200_OK)
                else:
                    return Response("trying to edit unauthorized movie", status = status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return Response("token expired", status = status.HTTP_401_UNAUTHORIZED)