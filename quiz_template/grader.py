"""
Grader class to handle assessment of submissions
"""
from quiz_template.models import Question_Master, User_Submissions
import json


class Grader():

    """
    Grader class to handle assessment of submissions
    """

    question = None
    submission = None
    the_question = None

    def __init__(self, submission, question):
        """ Initialize this class """
        self.submission = submission
        self.question = question

        if self.question is None:
            self.question = self.submission.question

    def update_marks(self, is_correct=True):
        """
        Get and update the marks for this submission
        """

        difference = 0
        if is_correct:

            attempts = self.submission.attempts
            marks = 0
            if(self.submission.hint_taken):
                attempts += 1
            granularity = json.loads(self.question.marks)
            attempts -= 1
            if(attempts < len(granularity)):
                marks = granularity[attempts]
            self.submission.status = User_Submissions.CORRECT
            self.submission.marks = marks
        else:
            self.submission.status = User_Submissions.ATTEMPTED

            if(self.submission.attempts >= self.question.attempts):
                self.submission.status = User_Submissions.WRONG

        self.submission.save()
        return

    def grade(self):
        """
        Grade the submission or pass it appropriate grader
        IMPORTANT: This method must save the submission
        IMPORTANT: Ensure that update_marks() gets called
        Return True if result is directly available, false otherwise
        """

        if self.submission is None:
            return False

        else:

            answer = self.submission.answer
            self.the_question = Question_Master.objects.get_subclass(
                pk=self.question.pk)
            correct_answer = self.the_question.answer

            if self.question.type == \
                    Question_Master.SINGLE_CHOICE_QUESTION:
                self.grade_single_choice(answer, correct_answer)
                return True

            elif self.question.type == \
                    Question_Master.MULTIPLE_CHOICE_QUESTION:
                self.grade_multiple_choice(answer, correct_answer)
                return True

            elif self.question.type == \
                    Question_Master.FIXED_ANSWER_QUESTION:
                self.grade_fixed_answer(answer, correct_answer)
                return True

            elif self.question.type == \
                    Question_Master.DESCRIPTIVE_ANSWER_QUESTION:
                self.submission.status = User_Submissions.CORRECT
                self.submission.marks = 0
                self.submission.save()

        return True

    def grade_fixed_answer(self, answer, correct_answer):
        """ Grade fixed answer Question """
        print answer, correct_answer
        correct = False
        explainations = json.loads(self.the_question.explainations)
        cur_explain = ""
        for ans in correct_answer:
            if ans.lower() == answer.lower():
                correct = True
                cur_explain = explainations[correct_answer.index(ans)]
                break
        if(not correct):
            cur_explain = self.the_question.default_explanation_wrong
        self.submission.explaination = cur_explain
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_single_choice(self, answer, correct_answer):
        """ Grade single choice correct  Question """
        print answer, correct_answer
        correct = False
        explainations = json.loads(self.the_question.explainations)
        cur_explain = ""
        if(int(answer) < len(explainations)):
            cur_explain = explainations[int(answer)]

        if int(answer) == int(correct_answer):
            correct = True
            if(cur_explain == ""):
                cur_explain = self.the_question.default_explanation_correct
        else:
            if(cur_explain == ""):
                cur_explain = self.the_question.default_explanation_wrong

        self.submission.explaination = cur_explain
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_multiple_choice(self, answer, correct_answer):
        """ Grade Multiple choice correct Question """
        print "grade_multiple_choice : ", answer, correct_answer
        correct = False
        cur_explain = ""
        explainations = json.loads(self.the_question.explainations)
        answers = json.loads(answer)
        for index in range(len(answers)):
            print answers[index], explainations[index]
            if (answers[index]):
                cur_explain += explainations[index] + "\n"

        if answer == correct_answer:
            correct = True
            if(cur_explain == ""):
                cur_explain = self.the_question.default_explanation_correct
        else:
            if(cur_explain == ""):
                cur_explain = self.the_question.default_explanation_wrong
        self.submission.explaination = cur_explain
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_descriptive_answer(self, answer, correct_answer, submission):
        """ Grade Descriptive Question """
        pass
