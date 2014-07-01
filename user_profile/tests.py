"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from user_profile.models import CustomUser
from user_profile.views import *
import json

class UserModelTest(TestCase):
    def setUp(self):
        #instructor or content developer
        user = User(username='user', is_active=True, email="user@user.com")
        user.set_password('pass')
        user.save()

        c_user = CustomUser.objects.get(user=user)
        c_user.is_instructor = True
        c_user.is_content_developer = True
        c_user.default_mode = 'C'
        c_user.save()

        #student user
        user = User(username='student', is_active=True, email="student@user.com")
        user.set_password('pass')
        user.save()

        c_user = CustomUser.objects.get(user=user)
        c_user.is_instructor = False
        c_user.is_content_developer = False
        c_user.default_mode = 'S'
        c_user.save()

        College(college='college1').save()
        Major(major='major1').save()

    def test_user_model(self):
        u = User.objects.get(pk=1)
        cu = CustomUser.objects.get(user=u)

        self.assertEqual(u.username, 'user')
        self.assertTrue(cu.is_instructor)

    def test_user_login_required(self):
        c = Client()
        #without login
        response = c.get('/user/home/')
        self.assertEqual(response.status_code, 302)
        #login
        response = c.post('/accounts/login/', {'username':'user','password':'pass'}, follow=True)
        self.assertEqual(response.status_code, 200)
        #trying to get a login required page
        response = c.get('/user/home/')
        self.assertEqual(response.status_code, 200)

    def test_user_all_data(self):
        c = Client()
        response = c.post('/accounts/login/', {'username':'user','password':'pass'}, follow=True)
        response = c.get('/user/all/college')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertTrue('college1' in j)

    def test_switch_mode_instructor(self):
        c = Client()
        response = c.post('/accounts/login/', {'username':'user','password':'pass'}, follow=True)
        response = c.post('/user/switch-mode/', {'new_mode':'I'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_switch_mode_student(self):
        c = Client()
        response = c.post('/accounts/login/', {'username':'student','password':'pass'}, follow=True)
        response = c.post('/user/switch-mode/', {'new_mode':'I'}, follow=True)
        self.assertEqual(response.status_code, 400)

    def test_user_profile_edit(self):
        c = Client()
        response = c.post('/accounts/login/', {'username':'user','password':'pass'}, follow=True)
        response = c.post('/user/view-profile/',{'form_method':'about', 'first_name':'user', 'last_name':'1', 'about':'test user'}, follow=True)
        self.assertEqual(response.status_code, 200)

        response = c.post('/user/view-profile/',{'form_method':'personal_info', 'gender':'F'}, follow=True)
        self.assertEqual(response.status_code, 200)

        response = c.post('/user/view-profile/',{'form_method':'add_education', 'college':'college1', 'major':'major1', 'degree':'BTECH', 'start_date':'10/2/2014', 'end_date':'12/2/2014'}, follow=True)
        self.assertEqual(response.status_code, 200)

        response = c.post('/user/view-profile/',{'form_method':'social','twitter':'user'}, follow=True)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='user')
        profile = UserProfile.objects.get(user=user)
        education = Education.objects.get(user=user)

        self.assertEqual(profile.user.first_name, 'user')
        self.assertEqual(profile.user.last_name, '1')
        self.assertEqual(profile.about, 'test user')
        self.assertEqual(profile.gender, 'F')
        self.assertEqual(education.college.college, 'college1')
        self.assertEqual(education.major.major, 'major1')
        self.assertEqual(profile.website_twitter, 'user')

        response = c.post('/user/view-profile/',{'form_method':'remove_education','education_id': education.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Education.DoesNotExist):
            Education.objects.get(user=user)