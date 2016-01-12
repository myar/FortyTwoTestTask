from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.


class SomeTests(TestCase):

    def test_home_page(self):
        """
        Tests for added hard-coded data on home page.
        """
        # create response
        response = self.client.get(reverse('home-page', kwargs={'pk': 1}))
        # check status code
        self.assertEqual(response.status_code, 200)
        # check if correct data in response
        self.assertContains(response, '<p>Name: Mykola</p>',
                            count=1, status_code=200)
