from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
	sender_user = models.ForeignKey(User, related_name='sent_user_requests', on_delete=models.CASCADE)
	receiver_user = models.ForeignKey(User, related_name='received_user_requests', on_delete=models.CASCADE)
	status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)
	added_datetime = models.DateTimeField(auto_now_add=True)
	updated_datetime = models.DateTimeField(auto_now=True)