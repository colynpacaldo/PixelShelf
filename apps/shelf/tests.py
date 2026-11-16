from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Shelf


class CommunityDiscoveryTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="pixelartist")
		self.shelf = Shelf.objects.create(
			user=self.user,
			title="Museum Platformer Tiles",
			is_public=True,
		)
		self.client.force_login(self.user)

	def test_search_without_matches_shows_popular_public_shelves(self):
		response = self.client.get(reverse("shelf:community"), {"q": "no match"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Popular public shelves")
		self.assertContains(response, self.shelf.title)

	def test_matching_search_does_not_repeat_shelf_in_discovery_section(self):
		response = self.client.get(reverse("shelf:community"), {"q": "Museum"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.shelf.title, count=1)
