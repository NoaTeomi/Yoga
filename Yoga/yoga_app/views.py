from django.shortcuts import render, redirect
from .models import YogaPose, YogaSequence
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        # The user is logged in, show the gallery
        context = {
            'show_gallery': True,
            'poses': YogaPose.objects.all()  
        }
    else:
        # The user is not logged in, show the message
        context = {
            'show_gallery': False,
            'poses': []  # Empty list or no data for poses when logged out
        }
    
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def create_sequence(request):
    if request.method == 'POST':
        name = request.POST['name']
        duration = request.POST['duration']
        pose_ids = request.POST.getlist('poses')  # List of pose IDs selected by the user
        sequence = YogaSequence.objects.create(user=request.user, name=name, duration=duration)
        sequence.poses.set(pose_ids)  # Associate selected poses with the sequence
        return redirect('home')

    poses = YogaPose.objects.all()
    return render(request, 'create_sequence.html', {'poses': poses})
