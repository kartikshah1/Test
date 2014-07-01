"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from user_profile.models import CustomUser
from quiz.models import *
import json
from quiz.grader import Grader

class QuizModelTest(TestCase):
    def setUp(self):
        #instructor or content developer
        user = User(username='user', is_active=True, email="user@user.com")
        user.set_password('pass')
        user.save()

        self.instructor = CustomUser.objects.get(user=user)
        self.instructor.is_instructor = True
        self.instructor.is_content_developer = True
        self.instructor.default_mode = 'C'
        self.instructor.save()

        #student user
        user = User(username='student', is_active=True, email="student@user.com")
        user.set_password('pass')
        user.save()

        self.student = CustomUser.objects.get(user=user)
        self.student.is_instructor = False
        self.student.is_content_developer = False
        self.student.default_mode = 'S'
        self.student.save()

        quiz1 = Quiz(title='quiz 1')
        quiz1.save()
        module1 = QuestionModule(quiz=quiz1, title='module 1')
        module1.save()
        question1 = DescriptiveQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='this is the answer',grader_type='M')
        question1.save()

        submission = Submission(question=question1,student=user, answer='this is the answer', grader_type='M')
        submission.save()

        question1 = SingleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]',answer=0)
        question1.save()

        submission = Submission(question=question1,student=user, answer='1')
        submission.save()
        submission = Submission(question=question1,student=user, answer='0')
        submission.save()

        question1 = MultipleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]', answer='[true, false, true]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='[true, false, false]')
        submission.save()
        submission = Submission(question=question1,student=user, answer='[true, false, true]')
        submission.save()

        question1 = FixedAnswerQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='["a1", "a2", "a3"]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='a4')
        submission.save()
        submission = Submission(question=question1,student=user, answer='a2')
        submission.save()

    def test_quiz_model(self):
        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(quiz.title, 'quiz 1')
        self.assertEqual(quiz.question_modules, 1)
        self.assertEqual(quiz.questions, 4)
        self.assertEqual(quiz.marks, 12)

        module = QuestionModule.objects.get(pk=1)
        self.assertEqual(module.quiz, quiz)
        self.assertEqual(module.title, 'module 1')
        self.assertEqual(module.questions, 4)

        question = DescriptiveQuestion.objects.get(pk=1)
        self.assertEqual(question.question_module, module)
        self.assertEqual(question.quiz, quiz)
        self.assertEqual(question.description, 'q1')
        self.assertEqual(question.marks, 3)
        self.assertEqual(question.attempts, 2)
        self.assertEqual(question.grader_type, 'M')
        self.assertEqual(question.granularity, '3,2,0')
        self.assertEqual(question.answer, 'this is the answer')
        question.delete()

        question = SingleChoiceQuestion.objects.get(pk=2)
        self.assertEqual(question.options, '["a1","a2","a3"]')
        self.assertEqual(question.answer, 0)
        self.assertEqual(question.get_answer(), 0)
        self.assertEqual(question.get_answer(True), 'a1')

        question = MultipleChoiceQuestion.objects.get(pk=3)
        self.assertEqual(question.options, '["a1","a2","a3"]')
        self.assertEqual(question.answer, '[true, false, true]')
        self.assertEqual(question.get_answer(), '[true, false, true]')
        self.assertEqual(question.get_answer(True), '["a1", "a3"]')

        question = FixedAnswerQuestion.objects.get(pk=4)
        self.assertEqual(question.answer, '["a1", "a2", "a3"]')
        self.assertEqual(question.get_answer(), json.loads('["a1", "a2", "a3"]'))

        module = QuestionModule.objects.get(pk=1)
        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(module.questions, 3)
        self.assertEqual(quiz.questions, 3)
        self.assertEqual(quiz.marks, 9)

        module.delete()

        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(quiz.question_modules, 0)
        self.assertEqual(quiz.questions, 0)

    def test_quiz_history_model(self):
        submission = Submission.objects.get(pk=1)
        self.assertEqual(submission.question, Question.objects.get(pk=1))
        self.assertEqual(submission.student, self.student.user)
        self.assertEqual(submission.answer, 'this is the answer')
        self.assertEqual(submission.status, 'A')

        grader = Grader(submission,None,None)
        self.assertFalse(grader.grade())

        self.assertEqual(submission.status, 'A')

        with self.assertRaises(QuestionHistory.DoesNotExist):
            QuestionHistory.objects.get(student=submission.student, question=submission.question)



        submission = Submission.objects.get(pk=2)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())

        self.assertEqual(submission.status, 'D')
        self.assertEqual(submission.is_correct, False)
        self.assertEqual(submission.result, 0.0)

        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        #Note : attempts not increased in grader or submission model
        # self.assertEqual(question_hist.attempts, 1)
        self.assertEqual(question_hist.status, 'O')

        quiz_hist = QuizHistory(user=submission.student, quiz=Quiz.objects.get(pk=1))
        self.assertEqual(quiz_hist.marks, 0.0)

        submission = Submission.objects.get(pk=3)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())

        self.assertEqual(submission.status, 'D')
        self.assertEqual(submission.is_correct, True)
        # marks not updated as depend on attempts
        # self.assertEqual(submission.result, 2.0)


        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        self.assertEqual(question_hist.status, 'S')
        # self.assertEqual(quiz_hist.marks, 2.0)

        quiz_hist = QuizHistory(user=submission.student, quiz=Quiz.objects.get(pk=1))
        # self.assertEqual(quiz_hist.marks, 2.0)


        submission = Submission.objects.get(pk=4)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())
        self.assertEqual(submission.is_correct, False)
        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        self.assertEqual(question_hist.status, 'O')
        submission = Submission.objects.get(pk=5)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())
        self.assertEqual(submission.is_correct, True)
        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        self.assertEqual(question_hist.status, 'S')

        submission = Submission.objects.get(pk=6)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())
        self.assertEqual(submission.is_correct, False)
        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        self.assertEqual(question_hist.status, 'O')
        submission = Submission.objects.get(pk=7)
        grader = Grader(submission,None,None)
        self.assertTrue(grader.grade())
        self.assertEqual(submission.is_correct, True)
        question_hist = QuestionHistory.objects.get(student=submission.student, question=submission.question)
        self.assertEqual(question_hist.status, 'S')


class QuizViewAdminTest(TestCase):
    def setUp(self):
        #instructor or content developer
        user = User(username='user', is_active=True, email="user@user.com")
        user.set_password('pass')
        user.save()

        self.instructor = CustomUser.objects.get(user=user)
        self.instructor.is_instructor = True
        self.instructor.is_content_developer = True
        self.instructor.default_mode = 'C'
        self.instructor.save()

        quiz1 = Quiz(title='quiz 1')
        quiz1.save()
        module1 = QuestionModule(quiz=quiz1, title='module 1')
        module1.save()
        # question1 = DescriptiveQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='this is the answer',grader_type='M')
        # question1.save()

        # submission = Submission(question=question1,student=user, answer='this is the answer', grader_type='M')
        # submission.save()

        question1 = SingleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]',answer=0)
        question1.save()

        submission = Submission(question=question1,student=user, answer='1')
        submission.save()
        submission = Submission(question=question1,student=user, answer='0')
        submission.save()

        question1 = MultipleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]', answer='[true, false, true]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='[true, false, false]')
        submission.save()
        submission = Submission(question=question1,student=user, answer='[true, false, true]')
        submission.save()

        question1 = FixedAnswerQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='["a1", "a2", "a3"]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='a4')
        submission.save()
        submission = Submission(question=question1,student=user, answer='a2')
        submission.save()

        self.c = Client()
        self.c.post('/accounts/login/', {'username':'user','password':'pass'}, follow=True)

    def test_quiz_view_get(self):
        response = self.c.get('/quiz/api/quiz/', follow=True)
        self.assertEqual(response.status_code, 200)

        quiz_list = json.loads(response.content)
        self.assertEqual(len(quiz_list), 1)


        response = self.c.get('/quiz/api/quiz/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        quiz = json.loads(response.content)
        self.assertEqual(quiz['id'], 1)
        self.assertEqual(quiz['title'], 'quiz 1')
        self.assertEqual(quiz['question_modules'], 1)
        self.assertEqual(quiz['questions'], 3)
        self.assertEqual(quiz['marks'], 9)


        response = self.c.get('/quiz/api/quiz/1000/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.c.get('/quiz/api/quiz/1/get_question_modules/',follow=True)
        self.assertEqual(response.status_code, 200)

        module_list = json.loads(response.content)
        self.assertEqual(len(module_list), 1)

        response = self.c.get('/quiz/api/quiz/1/get_questions_manual_grade/',follow=True)
        self.assertEqual(response.status_code, 200)

        question_list = json.loads(response.content)
        self.assertEqual(len(question_list), 0)


    def test_quiz_view_post(self):
        response = self.c.post('/quiz/api/quiz/', {'title':'Quiz 2'})
        self.assertEqual(response.status_code, 201)

        response = self.c.post('/quiz/api/quiz/1/', {'title':'Quiz 1 mod', '_method':'PUT'})
        self.assertEqual(response.status_code, 200)

        quiz = json.loads(response.content)
        self.assertEqual(quiz['id'], 1)
        self.assertEqual(quiz['title'], 'Quiz 1 mod')
        self.assertEqual(quiz['question_modules'], 1)
        self.assertEqual(quiz['questions'], 3)
        self.assertEqual(quiz['marks'], 9)

        response = self.c.post('/quiz/api/quiz/2/', {'_method':'DELETE'})
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Quiz.DoesNotExist):
            Quiz.objects.get(pk=2)


        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'quiz':1,'title': 'module'})
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'title': 'module'})
        self.assertEqual(response.status_code, 400)

    def test_quiz_module_view_get(self):
        response = self.c.get('/quiz/api/question_module/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        module = json.loads(response.content)
        self.assertEqual(module['quiz'], 1)
        self.assertEqual(module['title'], 'module 1')
        self.assertEqual(module['questions'], 3)


        response = self.c.get('/quiz/api/question_module/1000/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.c.get('/quiz/api/question_module/1/get_questions_admin/')
        self.assertEqual(response.status_code, 200)
        questions = json.loads(response.content)
        self.assertEqual(len(questions), 3)

        response = self.c.get('/quiz/api/question_module/1/get_questions/')
        self.assertEqual(response.status_code, 200)
        questions = json.loads(response.content)
        self.assertEqual(len(questions), 3)

        # /quiz/api/question_module/1/get_question_and_history_data/

    def test_quiz_module_view_post(self):
        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'quiz':1,'title': 'module'})
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/quiz/api/question_module/2/', {'quiz':'1', 'title':'module mod', '_method':'PUT'})
        self.assertEqual(response.status_code, 200)

        module = json.loads(response.content)
        self.assertEqual(module['quiz'], 1)
        self.assertEqual(module['title'], 'module mod')
        self.assertEqual(module['questions'], 0)

        response = self.c.post('/quiz/api/question_module/2/', {'_method':'DELETE'})
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(QuestionModule.DoesNotExist):
            QuestionModule.objects.get(pk=2)

        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'answer':'["a1", "a2", "a3"]', 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_fixed_answer_question/', question)
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/quiz/api/question_module/1/add_fixed_answer_question/', {})
        self.assertEqual(response.status_code, 400)

        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'options':'["a1","a2","a3"]', 'answer':0, 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_single_choice_question/', question)
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/quiz/api/question_module/1/add_single_choice_question/', {})
        self.assertEqual(response.status_code, 400)

        #TODO should give error if form of answer is wrong it accepts 0 as answer
        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'options':'["a1","a2","a3"]', 'answer':'[true, false, true]', 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_multiple_choice_question/', question)
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/quiz/api/question_module/1/add_multiple_choice_question/', {})
        self.assertEqual(response.status_code, 400)

class QuizViewStudentTest(TestCase):
    def setUp(self):
        #student user
        user = User(username='student', is_active=True, email="student@user.com")
        user.set_password('pass')
        user.save()

        self.student = CustomUser.objects.get(user=user)
        self.student.is_instructor = False
        self.student.is_content_developer = False
        self.student.default_mode = 'S'
        self.student.save()

        quiz1 = Quiz(title='quiz 1')
        quiz1.save()
        module1 = QuestionModule(quiz=quiz1, title='module 1')
        module1.save()
        # question1 = DescriptiveQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='this is the answer',grader_type='M')
        # question1.save()

        # submission = Submission(question=question1,student=user, answer='this is the answer', grader_type='M')
        # submission.save()

        question1 = SingleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]',answer=0)
        question1.save()

        submission = Submission(question=question1,student=user, answer='1')
        submission.save()
        submission = Submission(question=question1,student=user, answer='0')
        submission.save()

        question1 = MultipleChoiceQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,options='["a1","a2","a3"]', answer='[true, false, true]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='[true, false, false]')
        submission.save()
        submission = Submission(question=question1,student=user, answer='[true, false, true]')
        submission.save()

        question1 = FixedAnswerQuestion(quiz=quiz1, question_module=module1, description='q1',marks=3,attempts=2,answer='["a1", "a2", "a3"]')
        question1.save()
        submission = Submission(question=question1,student=user, answer='a4')
        submission.save()
        submission = Submission(question=question1,student=user, answer='a2')
        submission.save()

        self.c = Client()
        self.c.post('/accounts/login/', {'username':'student','password':'pass'}, follow=True)

    def test_quiz_view_get(self):
        response = self.c.get('/quiz/api/quiz/', follow=True)
        self.assertEqual(response.status_code, 200)

        quiz_list = json.loads(response.content)
        self.assertEqual(len(quiz_list), 1)


        response = self.c.get('/quiz/api/quiz/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        quiz = json.loads(response.content)
        self.assertEqual(quiz['id'], 1)
        self.assertEqual(quiz['title'], 'quiz 1')
        self.assertEqual(quiz['question_modules'], 1)
        self.assertEqual(quiz['questions'], 3)
        self.assertEqual(quiz['marks'], 9)


        response = self.c.get('/quiz/api/quiz/1000/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.c.get('/quiz/api/quiz/1/get_question_modules/',follow=True)
        self.assertEqual(response.status_code, 200)

        module_list = json.loads(response.content)
        self.assertEqual(len(module_list), 1)

        response = self.c.get('/quiz/api/quiz/1/get_questions_manual_grade/',follow=True)
        self.assertEqual(response.status_code, 200)

        question_list = json.loads(response.content)
        self.assertEqual(len(question_list), 0)


    def test_quiz_view_post(self):
        response = self.c.post('/quiz/api/quiz/', {'title':'Quiz 2'})
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/quiz/1/', {'title':'Quiz 1 mod', '_method':'PUT'})
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/quiz/2/', {'_method':'DELETE'})
        self.assertEqual(response.status_code, 403)
        with self.assertRaises(Quiz.DoesNotExist):
            Quiz.objects.get(pk=2)

        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'quiz':1,'title': 'module'})
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'title': 'module'})
        self.assertEqual(response.status_code, 403)

    def test_quiz_module_view_get(self):
        response = self.c.get('/quiz/api/question_module/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        module = json.loads(response.content)
        self.assertEqual(module['quiz'], 1)
        self.assertEqual(module['title'], 'module 1')
        self.assertEqual(module['questions'], 3)


        response = self.c.get('/quiz/api/question_module/1000/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.c.get('/quiz/api/question_module/1/get_questions_admin/')
        self.assertEqual(response.status_code, 200)
        questions = json.loads(response.content)
        self.assertEqual(len(questions), 3)

        response = self.c.get('/quiz/api/question_module/1/get_questions/')
        self.assertEqual(response.status_code, 200)
        questions = json.loads(response.content)
        self.assertEqual(len(questions), 3)

        # /quiz/api/question_module/1/get_question_and_history_data/

    def test_quiz_module_view_post(self):
        response = self.c.post('/quiz/api/quiz/1/add_question_module/', {'quiz':1,'title': 'module'})
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/question_module/1/', {'quiz':'1', 'title':'module mod', '_method':'PUT'})
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/question_module/1/', {'_method':'DELETE'})
        self.assertEqual(response.status_code, 403)
        with self.assertRaises(QuestionModule.DoesNotExist):
            QuestionModule.objects.get(pk=2)

        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'answer':'["a1", "a2", "a3"]', 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_fixed_answer_question/', question)
        self.assertEqual(response.status_code, 403)

        response = self.c.post('/quiz/api/question_module/1/add_fixed_answer_question/', {})
        self.assertEqual(response.status_code, 403)

        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'options':'["a1","a2","a3"]', 'answer':0, 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_single_choice_question/', question)
        self.assertEqual(response.status_code, 403)
        response = self.c.post('/quiz/api/question_module/1/add_single_choice_question/', {})
        self.assertEqual(response.status_code, 403)

        question = {'quiz':1, 'question_module':1, 'description':'q1', 'marks':3, 'attempts':2, 'options':'["a1","a2","a3"]', 'answer':'[true, false, true]', 'type':'D', 'granularity':' '}
        response = self.c.post('/quiz/api/question_module/1/add_multiple_choice_question/', question)
        self.assertEqual(response.status_code, 403)
        response = self.c.post('/quiz/api/question_module/1/add_multiple_choice_question/', {})
        self.assertEqual(response.status_code, 403)
