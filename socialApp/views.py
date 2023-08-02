from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from socialApp.serializers import SignupSerializer, LoginSerlizer, SearchSerializer, FriendSerializer
from socialApp.models import Friend

class SignupView(generics.CreateAPIView):
	serializer_class = SignupSerializer


class LoginView(APIView):
	serializer_class = LoginSerlizer

	def post(self, request):
		serializer = LoginSerlizer(data=request.data)
		if serializer.is_valid():
			email = serializer.validated_data['email']
			password = serializer.validated_data['password']
			try:
				user_object = User.objects.get(email__iexact=email)
			except:
				return Response({'message': 'Invalid data'}, 
					status=status.HTTP_400_BAD_REQUEST)
			user = authenticate(request, username=user_object.username, password=password)
			if user:
				token, created = Token.objects.get_or_create(user=user)
				return Response({'token': token.key}, status=status.HTTP_200_OK)
			else:
				return Response({'message': 'Invalid credentials'}, 
					status=status.HTTP_401_UNAUTHORIZED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchAPIView(generics.ListAPIView):
	serializer_class = SearchSerializer
	queryset = User.objects.all()
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		search_keyword = self.request.query_params.get('search_keyword', None)
		if not search_keyword:
			return User.objects.none()
		
		queryset = User.objects.filter(email=search_keyword).exclude(email=
			self.request.user.email).order_by('email')
		if not queryset:
			queryset = User.objects.filter(Q(first_name__icontains=search_keyword)
				|Q(last_name__icontains=search_keyword)).order_by('first_name')
		
		return queryset

class FriendAPIView(generics.ListCreateAPIView):
	serializer_class = FriendSerializer
	permissions_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		requested_user = self.request.user
		status = self.request.query_params.get('status', None)
		if not status:
			return Friend.objects.none()
		queryset = Friend.objects.filter(sender_user=requested_user, status__iexact=
		status).order_by('receiver_user')
		return queryset

	def post(self, request, *args, **kwargs):
		requested_user = request.user
		serializer = FriendSerializer(data=request.data, context={'request':request})
		if serializer.is_valid():
			friend_object, _ = Friend.objects.get_or_create(sender_user=requested_user,receiver_user_id=
				serializer.data['receiver_user'])
			friend_object.status = serializer.data['status']
			friend_object.save()
			return Response(status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


