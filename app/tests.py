from django.test import TestCase
from .models import LandingPageUser

class LandingPageUserModelTest(TestCase):

    def setUp(self):
        # Set up data for the tests
        self.lpu = self.LandingPageUser = LandingPageUser.objects.create(
            email='test@example.com',
            first_name='Mark',
        )

    def test_lpu_creation(self):
        """
        Test the creation of a LandingPageUser instance.
        """
        self.assertEqual(self.lpu.first_name, 'Mark')
        self.assertEqual(self.lpu.email, 'test@example.com')
        self.assertEqual(self.lpu.referred_by, None)

