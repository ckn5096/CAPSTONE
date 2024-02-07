from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.urls import reverse


User = get_user_model()

# Create your views here.

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    queryset = []  # Add this line

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            send_welcome_email(user.email)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_welcome_email(user_email):
    subject = 'Welcome to Your Website'
    message = 'Welcome to Music Match! \nThank you for signing up \n. Please confirm your email address in order to activate your account.'
    from_email = 'music.match.django@gmail.com'

    send_mail(subject, message, from_email, [user_email], fail_silently=True)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)

            home_url = reverse('home')

            print('Generated Token:', token.key)

            return Response({'token': token.key, 'redirect_url': home_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class HomeView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        print('Request Headers:', request.headers)
        return Response({'message': f'Welcome, {request.user.username}!'})

