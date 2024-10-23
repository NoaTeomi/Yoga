from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import YogaSequence, YogaPose

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

