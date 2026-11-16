from django.test import TestCase
from django.urls import reverse


class LoginPageThemeTests(TestCase):
	def test_login_page_uses_shared_dark_theme(self):
		response = self.client.get(reverse("login:login"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'class="dark-mode auth-page"')
		self.assertContains(response, "redesign.")
from django.test import TestCase

# Add Login-feature-specific tests here.
