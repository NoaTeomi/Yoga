from django.shortcuts import render, redirect, get_object_or_404
from .models import YogaPose, YogaSequence
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, YogaSequenceForm
from django.contrib.auth.decorators import login_required
import logging
import requests


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
        pose_ids = request.POST.getlist('poses')  # List of pose IDs selected by the user
        sequence = YogaSequence.objects.create(user=request.user, name=name)
        sequence.poses.set(pose_ids)  # Associate selected poses with the sequence
        return redirect('home')

    # Fetch all poses and pass to the template, including their images
    poses = YogaPose.objects.all()
    return render(request, 'create_sequence.html', {'poses': poses})


@login_required
def my_sequences(request):
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

# Create a logger instance for external API calls
logger = logging.getLogger('external_api')

def fetch_api_data_view(request):
    try:
        logger.debug('Sending request to external API...')
        response = requests.get('https://api.example.com/data')
        response.raise_for_status()  # Raise an exception for HTTP error codes (4xx/5xx)
        logger.debug(f'Successfully received data from external API: {response.status_code}')
        data = response.json()  # Parse the JSON response
    except requests.RequestException as e:
        logger.error(f"Error occurred while fetching data from external API: {e}")
        data = None  # Handle the error by setting data to None or showing an error message

    # Render the data in the template, passing it to 'api_data.html'
    return render(request, 'api_data.html', {'data': data})