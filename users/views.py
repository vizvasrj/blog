from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

import jwt, datetime
from users.serializers import UserSerializer
from .models import User

from .serializers import (
    UserListSerializer, UserRegistrationSerializer,
    UserLoginSerializer)

# # not using
# class RegisterView(APIView):
#     def post(self, request):
#         serializers = UserSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data)

# # not using
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = User.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not Found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }
#         token = jwt.encode(
#             payload, 'secret', algorithm='HS256'
#         )
#         response = Response()
#         response.set_cookie(key='jwt', value=token)
#         # print(request.COOKIES['jwt'])
#         response.data = {
#             'jwt': token
#         }

#         return response

# # not using
# class UserView(APIView):
    
#     def get(self, request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
        
#         user = User.objects.get(id=payload['id'])
#         serializer = UserSerializer(user)


#         return Response(serializer.data)

# not using
class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwtt')
        response.data = {
            'message': 'logout susscessfully'
        }
        return response



# ppppppppppppppppppppppppppppppppppppppppppppppppppppp

from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import timedelta

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return JsonResponse(routes)

class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            data = serializer.data
            try:
                data.pop('password')
            except KeyError:
                pass
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': data
            }

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                }
            }
            r = Response(response)
            r.set_cookie(key='jwtt', value=serializer.data['access'])

            # return Response(response, status=status_code)
            return r

class UserListView(APIView):
    serializer_class = UserListSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            access_token = request.COOKIES['jwtt']
        except KeyError:
            raise AuthenticationFailed("Key missing try to login" \
                " again(you have been loged out)")
        if not access_token:
            raise AuthenticationFailed("Unauthenticate access token missing")

        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user = User.objects.get(id=payload['user_id'])

        # user = request.user
        if user.is_superuser != 1:
            status_code = status.HTTP_403_FORBIDDEN
            response = {
                'success': False,
                'status_code': status_code,
                'message': 'you are not authenticated to perform this action'
            }
            return Response(response, status=status_code)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            return Response(response, status=status_code)