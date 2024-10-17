from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import YogaSequence, YogaPose

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

