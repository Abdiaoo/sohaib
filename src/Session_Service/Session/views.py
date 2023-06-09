from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed, ValidationError, ParseError, NotAuthenticated
from adrf.decorators import api_view
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from django.core import serializers
from django.forms.models import model_to_dict
from .serializers import UserSerializer
from Session_Service.settings import SECRET_KEY
import datetime
import jwt
import json


@api_view(['POST'])
def register(request):
    try:
        if 'role' not in request.data:
            request.data.update({'role': 'user'})
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        raise ValidationError('Incorrect data')
    
    user = Users.objects.filter(username=username).first()
    
    if user is None:
        raise AuthenticationFailed('User not found!')
    
    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect Password!')
    profile_info = {
        'first_name': user.name,
        'last_name': user.username,
    }
    payload = {
        'user_uid': str(user.user_uid),
        'username': str(username),
        'role': str(user.role),
        'email': str(user.email),
        'profile':profile_info,
        'scope': 'openid profile email',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
    
    response = Response()
    
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data = {
        'detail': 'Authenticated'
    }
    return response


@api_view(['POST'])
def logout(request):
    try:
        data = auth(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'detail':'success',
            'user_uid': data['user_uid'],
            'username': data['username']
        }
        return response
    except Exception as e:
        return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)


def auth(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'],options={"verify_exp": False})
    
    payload.pop('exp')
    payload.pop('iat')
    return payload

@api_view(['GET'])
def verify(request):
    token = request.COOKIES.get('jwt')
    
    if token is None:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except jwt.DecodeError:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    response = JsonResponse({'detail': 'Authenticated'}, status=status.HTTP_200_OK)
    response.set_cookie(key='jwt',value=token,httponly=True)
    return response

@api_view(['GET'])
def refresh(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
    except Exception as e:
        raise ParseError('Parse error!')
    
    profile_info = {
        'first_name': payload['profile']['first_name'],
        'last_name': payload['profile']['last_name'],
    }
    payload = {
        'user_uid': str(payload['user_uid']),
        'username': str(payload['username']),
        'role': str(payload['role']),
        'email': str(payload['email']),
        'profile': profile_info,
        'scope': 'openid profile email',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
    
    response = Response()
    
    response.set_cookie(key='jwt', value=token,httponly=True)
    
    response.data = {
        'jwt': token
    }
    return response


@api_view(['GET'])
def users(request):
    try:
        data = auth(request)
        if data['role']!='admin':
            return Response({'detail':'You are not admin!'})
        
        users = Users.objects.all()
        users_json = json.loads(serializers.serialize('json',users))
        for user in users_json:
            fields = user["fields"]
            user.clear()
            user.update(fields)
        return Response(users_json, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def one_user(request, user_uid):
    try:
        auth(request)
        user = Users.objects.get(user_uid=user_uid)
        user = model_to_dict(user)
        rem_list = ['is_superuser', 'is_active', 'is_staff', 'id', 'password', 'groups', 'user_permissions', 'last_login']
        [user.pop(key) for key in rem_list]
        return Response(user, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def one_user_by_username(request,username=None):
    try:
        auth(request)
        user = Users.objects.get(username=username)
        user = model_to_dict(user)
        rem_list = ['is_superuser', 'is_active', 'is_staff', 'id', 'password', 'groups', 'user_permissions', 'last_login']
        [user.pop(key) for key in rem_list]
        return Response(user, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify(request):
    token = request.COOKIES.get('jwt')
    
    if token is None:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except jwt.DecodeError:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)

    response = JsonResponse({'detail': 'Authenticated'}, status=status.HTTP_200_OK)
    response.set_cookie(key='jwt', value=token, httponly=True)
    return response