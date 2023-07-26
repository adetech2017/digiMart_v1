from django.test import TestCase
from django.contrib.auth import get_user_model
from buyer.models import Buyer  # Replace "yourapp" with the name of your Django app
#from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from buyer.models import Buyer
from rest_framework_simplejwt.tokens import RefreshToken
from buyer.views import BuyerTokenObtainPairView
from rest_framework.reverse import reverse



class BuyerModelTest(TestCase):
    def test_buyer_model_creation(self):
        # Create a user instance for the buyer
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            # Add any other required fields for the user model
        )

        # Create a buyer instance
        buyer = Buyer.objects.create(
            user=user,
            user_type='buyer',
            gender='Male',
            phone_number='1234567890',
            address='123 Main Street, City',
            # Add any other required fields for the buyer model
        )

        # Test that the buyer instance is saved in the database
        self.assertEqual(Buyer.objects.count(), 1)

        # Test that the user instance is correctly associated with the buyer instance
        self.assertEqual(buyer.user, user)

        # Add more assertions to test other fields as needed
        self.assertEqual(buyer.user_type, 'buyer')
        self.assertEqual(buyer.gender, 'Male')
        self.assertEqual(buyer.phone_number, '1234567890')
        self.assertEqual(buyer.address, '123 Main Street, City')
        # Add more assertions for other fields in the buyer model

class BuyerTokenObtainPairViewTest(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.url = reverse('token_obtain_pair')  # Replace 'token_obtain_pair' with your actual URL name

    def test_buyer_token_obtain_pair(self):
        # Log in the test user before making the request
        self.client.force_authenticate(user=self.user)

        # Test token obtain pair endpoint with valid credentials
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

        buyer_data = response.data.get('user').get('buyer', None)
        if buyer_data:
            self.assertIn('id', buyer_data)
            self.assertIn('user', buyer_data)
            self.assertIn('buyer_id', response.data)
            self.assertIn('buyer_username', response.data)
        else:
            self.assertIsNone(buyer_data)
            self.assertNotIn('buyer_id', response.data)
            self.assertNotIn('buyer_username', response.data)

    def test_buyer_token_obtain_pair_invalid_credentials(self):
        # Test token obtain pair endpoint with invalid credentials
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Corrected status code here
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertNotIn('buyer_id', response.data)
        self.assertNotIn('buyer_username', response.data)