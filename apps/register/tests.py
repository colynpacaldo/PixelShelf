from django.test import TestCase
from django.urls import reverse


class RegisterPageThemeTests(TestCase):
	def test_register_page_uses_shared_dark_theme(self):
		response = self.client.get(reverse("register:register"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'class="dark-mode auth-page"')
		self.assertContains(response, "redesign.")
from django.test import TestCase

# Add Register-feature-specific tests here.
