from django.urls import path

from socialApp.views import SignupView, LoginView, SearchAPIView, FriendAPIView

urlpatterns = [
	path('signup/', SignupView.as_view(), name='signup'),
	path('login/', LoginView.as_view(), name='login'),
	path('search/', SearchAPIView.as_view(), name='search'),
	path('friend/', FriendAPIView.as_view(), name='friend')
]