from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


#Local Imports
from utils import success_response,error_response,get_tokens_for_user
from .validators import UserRegisterValidators, LoginValidator



# Create your views here.
class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        try:
            validator = UserRegisterValidators(data=request.data)
            if not validator.is_valid():
                return Response(
                    error_response
                    (message="Invalid data",
                     errors="Invalid data"),
                    status=status.HTTP_400_BAD_REQUEST)

            validated = validator.validated_data
            username  = validated.get('username')
            email     = validated.get('email')
            password  = validated.get('password')

            if User.objects.filter(username=username).exists():
                return Response(
                    error_response(
                        message='Username already exists.',
                        errors='Username already exists.',
                    ),
                    status=status.HTTP_409_CONFLICT,
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    error_response(
                        message='Email already exists.',
                        errors='Email already exists.',
                    ),
                    status=status.HTTP_409_CONFLICT,
                )
            default_group = Group.objects.get(name='User')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            user.groups.add(default_group)


            return Response(
                success_response(
                    message='User registered successfully.',
                    data={
                        "username": user.username,
                        "email": user.email,
                        "role": "User"
                        },
                ),
                status=status.HTTP_201_CREATED,
            )
        
        except Group.DoesNotExist:
            return Response(
                error_response(message='Group Not Found.', errors='groups not found first create the Groups.'),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            return Response(
                error_response(message='Something went wrong.', errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        try:

            validator = LoginValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    error_response
                    (message="Invalid data",
                     errors="Invalid data"),
                    status=status.HTTP_400_BAD_REQUEST)
                

            validated = validator.validated_data
            username  = validated.get('username')
            password  = validated.get('password')

            if not User.objects.filter(username=username).exists():

                return Response(
                    error_response(message='User not found.',
                        errors='No account found with this username.',
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )

            user = authenticate(username=username, password=password)
            if user is None:
                return Response(
                    error_response(
                        message='Invalid credentials.',
                        errors='Password is incorrect.',
                    ),
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            tokens = get_tokens_for_user(user)

            return Response(
                success_response(
                    message='Login successful.',
                    data={
                        'user': user.username,
                        "tokens":tokens
                    },
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                error_response(message='Something went wrong.', errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            print(refresh_token)

            if not refresh_token:
                return Response(
                    error_response(
                        message='Refresh token is required.',
                        errors='Refresh token is required.',
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            return Response(
                success_response(
                    message="Access token refreshed successfully",
                    data={
                        "refresh":str(refresh),
                        "access": str(access_token),
                        "expiry_time": access_token["exp"] * 1000
                    }
                ),
                status=status.HTTP_200_OK
            )
  

        except Exception as e:
                    return Response(
                        error_response(
                            message='Something went wrong.',
                            errors=str(e),
                        ),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )