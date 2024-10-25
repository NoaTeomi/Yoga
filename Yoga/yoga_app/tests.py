from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import YogaSequence, YogaPose
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

class SignupViewTest(TestCase):
    
    def test_signup_get_request(self):
        # Test a GET request to load the signup form
        response = self.client.get(reverse('signup'))
        
        # Check if the response is successful and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
        # Verify the form is in the response context
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_successful_signup_and_redirect_to_home(self):
        # Define the data for a new user signup
        signup_data = {
            'username': 'newuser',
            'password1': 'strong_password123',
            'password2': 'strong_password123',
            'email': 'newuser@example.com'
        }
        
        # Submit a POST request to the signup view with valid data
        response = self.client.post(reverse('signup'), data=signup_data)
        
        # Check that the user is redirected to the home page after successful signup
        self.assertRedirects(response, reverse('home'))
        
        # Verify the new user is created and is authenticated in the session
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='newuser').id)

    def test_signup_with_invalid_data(self):
        # Define invalid signup data (passwords do not match)
        signup_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'different_password',
            'email': 'testuser@example.com'
        }
        
        # Submit a POST request to the signup view with invalid data
        response = self.client.post(reverse('signup'), data=signup_data)
        
        # Check that the signup page is rendered again due to form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
        # Verify that the form is in the response context before checking for form errors
        self.assertIn('form', response.context)
        form = response.context['form']
        
        # Ensure the user was not created
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        # Check for form errors to confirm invalid submission
        self.assertTrue(form.errors)
        self.assertIn('password2', form.errors)
        
        # Adjusted assertion to handle typographic single quotes
        self.assertIn("The two password fields didn't match", form.errors['password2'][0].replace("’", "'"))


class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_get_request(self):
        # Test a GET request to load the login form
        response = self.client.get(reverse('login'))
        
        # Check if the response is successful and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
        # Verify the form is in the response context
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_successful_login_and_redirect_to_home(self):
        # Define valid login data
        login_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        
        # Submit a POST request to the login view with valid data
        response = self.client.post(reverse('login'), data=login_data)
        
        # Check that the user is redirected to the home page after successful login
        self.assertRedirects(response, reverse('home'))
        
        # Verify the user is logged in by checking the session
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_with_invalid_data(self):
        # Define invalid login data (incorrect password)
        login_data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        
        # Submit a POST request to the login view with invalid data
        response = self.client.post(reverse('login'), data=login_data)
        
        # Check that the login page is rendered again due to form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
        # Verify that the form is in the response context before checking for form errors
        self.assertIn('form', response.context)
        form = response.context['form']
        
        # Ensure the user was not logged in
        self.assertNotIn('_auth_user_id', self.client.session)
        
        # Check for form errors to confirm invalid submission
        self.assertTrue(form.errors)
        self.assertIn('__all__', form.errors)
        self.assertIn("Please enter a correct username and password", form.errors['__all__'][0])


@override_settings(SECURE_SSL_REDIRECT=False)
class CreateSequenceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pose1 = YogaPose.objects.create(name='Pose 1', description='First pose')
        self.pose2 = YogaPose.objects.create(name='Pose 2', description='Second pose')

    def test_create_sequence_get_request(self):
        self.client.login(username='testuser', password='testpass') # Log in the test user
        response = self.client.get(reverse('create_sequence'))  # Simulate a GET request to the create_sequence view
        self.assertEqual(response.status_code, 200)  # Check if the page loads successfully
        self.assertContains(response, 'Pose 1') # Check that the response contains the yoga poses
        self.assertContains(response, 'Pose 2')

    def test_create_sequence_post_request(self):
        self.client.login(username='testuser', password='testpass') # Log in the test user

        # Simulate a POST request to create a new sequence
        data = {
            'name': 'Morning Routine',
            'poses': [self.pose1.id, self.pose2.id],  # Select multiple poses
        }
        response = self.client.post(reverse('create_sequence'), data)

        self.assertEqual(response.status_code, 302) # Check if the sequence was created and the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))

        # Verify the sequence was created in the database
        sequence = YogaSequence.objects.get(name='Morning Routine')
        self.assertEqual(sequence.user, self.user)
        self.assertEqual(sequence.poses.count(), 2)
        self.assertIn(self.pose1, sequence.poses.all())
        self.assertIn(self.pose2, sequence.poses.all())

    def test_create_sequence_requires_login(self):
        # Simulate an unauthenticated GET request to the create_sequence view
        response = self.client.get(reverse('create_sequence'))

        # Check that the user is redirected to the login page
        self.assertRedirects(response, '/login/?next=/create-sequence/')

class EditSequenceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pose1 = YogaPose.objects.create(name='Pose 1', description='First pose')
        self.pose2 = YogaPose.objects.create(name='Pose 2', description='Second pose')
        self.sequence = YogaSequence.objects.create(name='Test Sequence', user=self.user)
        self.sequence.poses.add(self.pose1)

    def test_edit_sequence_view(self):
        # Log in the user, allows accsess
        self.client.login(username='testuser', password='testpass')
        
        # Test GET request
        response = self.client.get(reverse('edit_sequence', args=[self.sequence.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Sequence')

        # Test POST request to update the sequence
        data = {
            'name': 'Updated Sequence',
            'poses': [self.pose1.id, self.pose2.id],  # Select multiple poses
        }
        response = self.client.post(reverse('edit_sequence', args=[self.sequence.id]), data)
        self.assertEqual(response.status_code, 302)  # Check if it redirects after successful edit

        # Check that the sequence was updated in the database
        self.sequence.refresh_from_db()
        self.assertEqual(self.sequence.name, 'Updated Sequence')
        self.assertEqual(self.sequence.poses.count(), 2)

