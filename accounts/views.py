from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer, UserSerializer
import jwt, datetime
from django.conf import settings

def make_token(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def get_user_from_request(request):
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['id'])
    except Exception as e:
        print('JWT ERROR:', e)
        return None

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            user = s.save()
            return Response({'token': make_token(user), 'user': UserSerializer(user).data}, status=201)
        return Response(s.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return Response({'token': make_token(user), 'user': UserSerializer(user).data})
            return Response({'error': 'Wrong password'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class MeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = get_user_from_request(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        return Response(UserSerializer(user).data)

    def put(self, request):
        user = get_user_from_request(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        s = UserSerializer(user, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=400)