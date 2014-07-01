"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

"""
add_fixed_answer_question:

{
"question_module": 1,
"quiz": 1,
"description": "My first question",
"hint": null,
"grader_type": "D",
"answer_description": "the answer is password",
"marks": "5",
"granularity": "5,0",
"granularity_hint":"1,0",
"type": "F",
"answer": "password"
}


Test script to populate data:

from courseware.models import *
from django.contrib.auth.models import *
from quiz.models import *

saif = User(username='saif',first_name='',last_name='',email='saifhhasan@gmail.com',is_active=True)
saif.set_password('0')
saif.save()

alankar = User(username='alankar',first_name='',last_name='',email='alankar111@gmail.com',is_active=True)
alankar.set_password('0')
alankar.save()

category = Category(title="My category")
category.save()

course = Course(title='My course', category=category)
course.save()

concept=Concept(title="My concept")
concept.save()

quiz = Quiz(title="Quiz - 1", course=course, concept=concept)
quiz.save()

saif_ch = CourseHistory(course=course, user=saif, is_instructor=True)
alankar_ch = CourseHistory(course=course, user=alankar, is_instructor=False)

"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
