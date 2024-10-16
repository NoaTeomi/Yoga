from django.urls import path
from .views import home, signup, user_login, create_sequence
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),  # Use the function-based home view
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('create-sequence/', create_sequence, name='create_sequence'),
]
