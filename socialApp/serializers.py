from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from rest_framework import serializers

from socialApp.models import Friend



class SignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name', 'username', 'password']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def validate_email(self, email):
		if email and User.objects.filter(email__iexact=email).exists():
			raise serializers.ValidationError("Email is in User")
		return email


class LoginSerlizer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'password']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def validate_email(self, email):
		if email and not User.objects.filter(email__iexact=email).exists():
			raise serializers.ValidationError("Email does not exists")
		return email

	def validate(self, data):
		email = data.get('email')
		password = data.get('password')
		if email and password:
			user = User.objects.filter(email__iexact=email).first()
			if user and user.check_password(password):
				return data

		raise serializers.ValidationError('Invalid email or password.')

class SearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']

class FriendSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friend
		fields = ['receiver_user', 'status']

	def validate(self, data):
		request = self._context.get("request")
		receiver_user = data.get('receiver_user')
		enter_before_datetime = self.get_datetime_for_send_request_validation()
		if Friend.objects.filter(sender_user=request.user, 
			receiver_user=receiver_user, status=data.get('status')).exists():
			raise serializers.ValidationError('Already made choice')
		elif Friend.objects.filter(sender_user=request.user, status__iexact=
			'pending', added_datetime__gte=enter_before_datetime).count() == settings.NUMBER_OF_REQUEST:
			raise serializers.ValidationError("only allow %s within time frame" %(settings.NUMBER_OF_REQUEST))
		elif request.user == receiver_user:
			raise serializers.ValidationError("can't make request to your own user")

		return data

	def get_datetime_for_send_request_validation(self):
		current_datetime = timezone.localtime(timezone.now())
		enter_before_datetime = current_datetime - timezone.timedelta(minutes=settings.REQUEST_WITHIN_IN_MINUTE)
	
		return enter_before_datetime