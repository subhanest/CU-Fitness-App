from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
import csv
import json
from django.shortcuts import render

def signup_view(request):
    return render(request, 'ok.html')  

def login_view(request):
    return render(request, 'b.html') 

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Save to JSON
            with open('users.json', 'a') as f:
                json.dump(serializer.data, f)
                f.write('\n')
            # Save to CSV
            with open('users.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([serializer.data['email'], serializer.data['username'], serializer.data['password'], serializer.data['receive_updates']])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        



    