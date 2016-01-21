import json
import datetime

from StringIO import StringIO

from django.db import models
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.models import User
from django.template import Template, Context

from apps.hello.models import StorageRequests, MyData, LogWorks
from apps.hello.forms import EditDataForm

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
        self.assertContains(response, '<p>Photo: ')

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
        request = self.client.get(reverse('middleware-storage'),
                                  {'ids_json': str(objs), }, )
        # ckeck if oll item had has cpecial class 'odd'
        self.assertContains(request, 'class="odd"',
                            count=10, status_code=200)
        data = [u'#10: at 2016-01-19 14:05:47 to testserver -- GET:/325/',
                u'#9: at 2016-01-19 14:05:47 to testserver -- GET:/325/']
        # post 2 items how view, from medium list
        request = self.client.post(
            reverse('middleware-storage'),
            {'ids_json': json.dumps(data), },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # check if only 8 items has had special class 'odd'
        self.assertContains(request, 'class="odd"',
                            count=8, status_code=200)


class EditDataTest(TestCase):
    """
    This test verifying, if can edit data after authorization
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        User.objects.create_user(username='testuser',
                                 email='user@host.net',
                                 password='pass')

    def test_login(self):
        """
        This is function verify login on page
        """
        # Verifying if redirected as url on login page
        url = reverse('edit-data', kwargs={'pk': 1})
        res = self.client.get(reverse('home-page', kwargs={'pk': 1}))
        self.assertContains(res, 'title="Login">Login</a>',
                            count=1, status_code=200)
        res = self.client.get(url)
        self.assertRedirects(res, reverse('login') + '?next=' + url)
        # Verifying if correct login on page
        self.client.login(username='testuser', password='pass')
        res = self.client.get(reverse('home-page', kwargs={'pk': 1}))
        self.assertContains(res, 'title="edit my data">Edit</a>',
                            count=1, status_code=200)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'class="submit" type="submit" value="Save"')

    def test_edit_page(self):
        """
        This is simple function validation data in form
        """
        # Logged
        self.client.login(username='testuser', password='pass')
        # Add all data
        image = open('uploads/photos/12.jpg')
        data = {"name": u'Mykola',
                "surname": u'Yaremov',
                "date_birth": datetime.date(1980, 9, 27),
                "bio": u'trala la la la la',
                "email": u'n.yaremov@gmail.com',
                "jabber": u'jaber',
                "skype": u'skype',
                "contacts": u'akakkd23edfrwssdcvf',
                "photo": image,
                }
        # Verifying request post , redirect - true
        res = self.client.post(reverse('edit-data', kwargs={'pk': 1}), data,
                               follow=True,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Load page (/contacts/1/) if correct data

        self.assertEqual(res.status_code, 200)
        self.assertTrue('"success": true' in res.content)
        objs = MyData.objects.all()
        self.assertTrue(objs[0].contacts, data['contacts'])
        self.assertEqual(objs[0].photo.width, 200)

    def test_return_error_edit(self):
        """
        This is function testing if return error list with not correct data
        """
        self.client.login(username='testuser', password='pass')
        # Add part data
        data = {"name": "Rasem",
                "email": "wqwert", }
        # Verifying request post , redirect - true
        res = self.client.post(reverse('edit-data', kwargs={'pk': 1}),
                               data, follow=True,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'This field is required', count=6,
                            status_code=200)
        self.assertContains(res, 'Enter a valid email address.', count=1,
                            status_code=200)

    def test_clalendar_widget(self):
        """
        This is test to simple test if add datepicker widget on page
        """
        temp = Template(EditDataForm())
        cont = Context()
        # Verification
        self.assertTrue("$('#id_date_birth').datepicker(" in temp.render(cont))


class TagTest(TestCase):
    """
    This is test to test template tag edit_data
    """

    def test_tag_via_template_without_login(self):
        """
           Test when user is not authentificate
        """
        t = Template('{% load admin_edit_object %}' + '{% edit_link obj %}')
        c = Context()
        self.assertEqual(t.render(c), '<a href="#">(admin)</a>')
        resp = self.client.get(reverse('home'))
        self.assertNotContains(resp, '(admin)</a>')

    def test_tag_via_template_with_login(self):
        """
           Test when user is authentificate
        """
        user = self.client.login(username='admin', password='admin')
        t = Template('{% load admin_edit_object %}{% edit_link obj%}')
        obj = MyData.objects.get(id=1)
        c = Context({'user': user, 'obj': obj})
        self.assertEqual(t.render(c),
                         '<a href="/admin/hello/mydata/1/">(admin)</a>')
        # Test witout obj
        c = Context({'user': user})
        self.assertEqual(t.render(c), '<a href="#">(admin)</a>')
        resp = self.client.get(reverse('home-page', kwargs={'pk': 1}))
        self.assertNotContains(resp, '<a href="#">(admin)</a>')

        user = self.client.login(username='admin', password='admin')
        t = Template('{% load admin_edit_object %}' + '{% edit_link obj %}')
        obj = StorageRequests.objects.get(id=1)
        c = Context({'user': user, 'obj': obj})
        self.assertEqual(
            t.render(c),
            '<a href="/admin/hello/storagerequests/1/">(admin)</a>')
        resp = self.client.get("/admin/hello/storagerequests/1/")
        self.assertEqual(resp.status_code, 200)


class OtherTests(TestCase):

    def test_list_all_models(self):
        """
        This is function call function and verify if correct response
        """

        out = StringIO()
        err = StringIO()
        call_command('list_all_models', stdout=out, stderr=err)
        self.assertTrue(u'Model MyData has -' in out.getvalue())
        self.assertTrue(u'error: Model MyData has -' in err.getvalue())
        self.assertEqual(out.getvalue().count('Model'),
                         len(models.get_models()))

    def test_my_callback_signal(self):
        """
        This is function verify if correct work my own signal
        """
        obj = StorageRequests(pk=1)
        obj.host = 'My_own_host'
        obj.save()
        work = LogWorks.objects.all()[0]
        self.assertEqual(work.mod_name, 'StorageRequests')
        self.assertEqual(work.work, 'creation')
