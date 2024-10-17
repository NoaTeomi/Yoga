from django.urls import path
from . import views
from .views import home, signup, user_login, create_sequence,delete_sequence, sequence_detail,my_sequences
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),  # Use the function-based home view
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('create-sequence/', create_sequence, name='create-sequence'),
    path('my-sequences/', views.my_sequences, name='my-sequences'),
    path('sequence/<int:pk>/', views.sequence_detail, name='sequence_detail'),
    path('delete-sequence/<int:sequence_id>/', views.delete_sequence, name='delete_sequence'),
    path('edit-sequence/<int:sequence_id>/', views.edit_sequence, name='edit_sequence'),
    #path('sequence/edit/<int:pk>/', views.sequence_edit, name='sequence_edit'),  # Edit view
]
