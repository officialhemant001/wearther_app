from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('auth:signup')
        self.login_url = reverse('auth:login')
        self.profile_url = reverse('users:profile')
        self.settings_url = reverse('users:settings')
        
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'StrongPassword123!'
        
    def test_signup_and_login_flow(self):
        # 1. Signup
        signup_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'password_confirm': self.password
        }
        response = self.client.post(self.signup_url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['username'], self.username)
        self.assertIn('access', response.data['data']['tokens'])

        # 2. Login
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['email'], self.email)
        access_token = response.data['data']['tokens']['access']
        
        # Authenticate future requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 3. Retrieve Profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['email'], self.email)

        # 4. Update Profile
        response = self.client.put(self.profile_url, {
            'username': 'newusername',
            'phone_number': '+1234567890'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'newusername')
        self.assertEqual(response.data['data']['phone_number'], '+1234567890')

        # 5. Retrieve Settings
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['temperature_unit'], 'celsius') # default value
        
        # 6. Update Settings
        response = self.client.put(self.settings_url, {
            'temperature_unit': 'fahrenheit',
            'push_notifications': False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['temperature_unit'], 'fahrenheit')
