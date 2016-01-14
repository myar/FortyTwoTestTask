from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.hello.models import StorageRequests

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

        # check response when data doesn't exist
        response = self.client.get(reverse('home-page',  kwargs={'pk': 99}))
        self.assertEqual(response.status_code, 404)


class MiddlewareTest(TestCase):
    """
    It is testing the process middleware.
    """

    def test_middleware(self):
        """
        This is function testing of process middleware
        """
        objs = StorageRequests.objects.all()
        # Verify the presence of data in the databese.
        self.assertEqual(objs.count(), 0)
        # Create request
        req = self.client.get(reverse('home-page', kwargs={'pk': 9999}))
        objs = StorageRequests.objects.all()
        self.assertEqual(objs.count(), 1)
        self.assertEqual(req.request['PATH_INFO'], objs[0].path)

        for i in xrange(10):
            self.client.get(reverse('home-page', kwargs={'pk': int(i)}))

        objs = StorageRequests.objects.all()
        for i in objs:
            self.assertEqual(i.viewed, False)

    def test_http_request_storage(self):
        """
        This is function testing views store
        """
        # Needed create a some requests for test
        contact_url = reverse('home-page', kwargs={'pk': 325})
        for __ in xrange(12):
            self.client.get(contact_url)
        res = self.client.get(reverse('middleware-storage'))
        # Check if only last 10 items displayed
        self.assertContains(res, 'to testserver -- GET:%s' % contact_url,
                            count=9, status_code=200)
        self.assertContains(res, 'to testserver -- GET:/store/',
                            count=1, status_code=200)

        objs = StorageRequests.objects.filter(viewed=False).\
            values_list('id', flat=True)
        request = self.client.post(
            reverse('middleware-storage'),
            {'ids_json': str(objs), },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest', )

        self.assertContains(request, 'to testserver -- GET:',
                            count=9, status_code=200)
        self.assertContains(request, 'to testserver -- POST:',
                            count=1, status_code=200)
        # chack only last 9 items, last post request not updated
        objs = StorageRequests.objects.all()[1:10]
        for i in objs:
            self.assertEqual(i.viewed, True)
