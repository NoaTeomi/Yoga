from django.shortcuts import render, redirect, get_object_or_404
from .models import YogaPose, YogaSequence
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, YogaSequenceForm
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger('django.request')

def home(request):
    logger.debug('Home view accessed')
    # Show the gallery to everyone, even if they are not logged in
    context = {
        'show_gallery': True,
        'poses': YogaPose.objects.all()  # Always show poses
    }
    
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f'New user {user.username} signed up and logged in')
            return redirect('home')
        else:
            logger.warning('Failed signup attempt')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f'User {user.username} logged in successfully')
            return redirect('home')
        else:
            logger.warning('Failed login attempt')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def custom_logout(request):
    if request.user.is_authenticated:
        logger.info(f'User {request.user.username} logged out')  # Log the username
    logout(request)
    return redirect('home')


@login_required
def create_sequence(request):
    logger.debug('Create sequence accessed')
    if request.method == 'POST':
        name = request.POST['name']
        pose_ids = request.POST.getlist('poses')  # List of pose IDs selected by the user
        sequence = YogaSequence.objects.create(user=request.user, name=name)
        sequence.poses.set(pose_ids)  # Associate selected poses with the sequence
        return redirect('home')

    # Fetch all poses and pass to the template, including their images
    poses = YogaPose.objects.all()
    return render(request, 'create_sequence.html', {'poses': poses})


@login_required
def my_sequences(request):
    logger = logging.getLogger('django.request')  # Get the same logger
    logger.debug('My sequences view accessed')
    sequences = YogaSequence.objects.filter(user=request.user)
    return render(request, 'my_sequences.html', {'sequences': sequences})

@login_required
def sequence_detail(request, pk):
    sequence = get_object_or_404(YogaSequence, pk=pk, user=request.user)
    return render(request, 'sequence_detail.html', {'sequence': sequence})

@login_required
def delete_sequence(request, sequence_id):
    sequence = get_object_or_404(YogaSequence, id=sequence_id, user=request.user)
    sequence.delete()
    return redirect('my-sequences')

@login_required
def edit_sequence(request, sequence_id):
    sequence = get_object_or_404(YogaSequence, pk=sequence_id, user=request.user)
    
    if request.method == 'POST':
        form = YogaSequenceForm(request.POST, instance=sequence)
        if form.is_valid():
            sequence = form.save(commit=False)  # Save the sequence data but not the poses yet
            sequence.poses.set(form.cleaned_data['poses'])  # Update the poses
            sequence.save()  # Save the sequence with updated poses
            return redirect('sequence_detail', pk=sequence_id)
    else:
        form = YogaSequenceForm(instance=sequence)

    return render(request, 'edit_sequence.html', {'form': form, 'sequence': sequence})

def trigger_error(request):
    # Intentional division by zero error
    1 / 0  # This will raise ZeroDivisionError
    return HttpResponse("This will never be reached.") 

def trigger_db_error(request):
    # Attempt to get a non-existent YogaPose (assuming ID 9999 doesn't exist)
    pose = YogaPose.objects.get(id=9999)  # This will raise a DoesNotExist error
    return HttpResponse(f"Pose: {pose.name}")