"""
Grader class to handle assessment of submissions
"""
from quiz.models import Question, QuestionHistory, Submission, QuizHistory


class Grader():
    """
    Grader class to handle assessment of submissions
    """

    question = None
    question_history = None
    the_question = None
    submission = None

    def __init__(self, submission, question, question_history):
        """ Initialize this class """
        self.submission = submission
        self.question = question
        self.question_history = question_history

        if self.question is None:
            self.question = self.submission.question

    def update_marks(self, is_correct=True):
        """
        Get and update the marks for this submission
        Update question history
        Applicable for Direct Grading ONLY
        """

        old_marks = self.question_history.marks
        difference = 0
        if is_correct:
            if self.question_history.hint_taken:
                granularity = self.question.granularity_hint
            else:
                granularity = self.question.granularity
            granularity = granularity.split(',')
            if (self.question_history.attempts - 1) > len(granularity):
                marks = granularity.pop()
            else:
                marks = granularity.pop(self.question_history.attempts - 1)

            self.question_history.status = QuestionHistory.SOLVED
            self.question_history.marks = marks
            difference = float(marks) - float(old_marks)
            self.submission.result = marks

        else:
            self.question_history.status = QuestionHistory.ATTEMPTED_ONCE

        if (self.question_history.attempts >= self.question.attempts
            or self.question_history.status == QuestionHistory.SOLVED):
            self.question_history.answer_shown = True
        self.question_history.save()
        if is_correct:
            quiz_history, created = QuizHistory.objects.get_or_create(
                quiz=self.question.quiz,
                user=self.question_history.student
            )
            quiz_history.update_score(difference)
        self.submission.status = Submission.DONE
        self.submission.is_correct = is_correct
        self.submission.save()

        return

    def grade(self):
        """
        Grade the submission or pass it appropriate grader
        IMPORTANT: This method must save the submission and question_history
        IMPORTANT: Ensure that update_marks() gets called
        Return True if result is directly available, false otherwise
        """

        if self.submission is None:
            return False

        if self.submission.grader_type == Question.MANUAL_GRADING:
            self.submission.save()
            return False

        elif self.submission.grader_type == Question.DIRECT_GRADING:

            answer = self.submission.answer
            self.the_question = \
                Question.objects.get_subclass(pk=self.submission.question.pk)
            correct_answer = self.the_question.get_answer()

            #either creating or getting the question history
            if self.question_history is None:
                self.question_history, created = QuestionHistory.objects.get_or_create(
                                              question=self.question,
                                              student=self.submission.student)

            if self.submission.question.type == \
                    Question.SINGLE_CHOICE_QUESTION:
                self.grade_single_choice(answer, correct_answer)
                return True

            elif self.submission.question.type == \
                    Question.MULTIPLE_CHOICE_QUESTION:
                self.grade_multiple_choice(answer, correct_answer)
                return True

            elif self.submission.question.type == \
                    Question.FIXED_ANSWER_QUESTION:
                self.grade_fixed_answer(answer, correct_answer)
                return True

            elif self.submission.question.type == \
                    Question.DESCRIPTIVE_ANSWER_QUESTION:
                pass

            elif self.submission.question.type == \
                    Question.PROGRAMMING_QUESTION:
                pass

        return True

    def grade_fixed_answer(self, answer, correct_answer):
        """ Grade fixed answer Question """
        print answer, correct_answer
        correct = False
        for ans in correct_answer:
            if ans.lower() == answer.lower():
                correct = True
                break
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_single_choice(self, answer, correct_answer):
        """ Grade single choice correct  Question """
        print answer, correct_answer
        correct = False
        if int(answer) == int(correct_answer):
            correct = True
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_multiple_choice(self, answer, correct_answer):
        """ Grade Multiple choice correct Question """
        print "grade_multiple_choice : ", answer, correct_answer
        correct = False
        if answer == correct_answer:
            correct = True
        print "result is ", correct, "\n\n\n"
        self.update_marks(correct)

    def grade_descriptive_answer(self, answer, correct_answer, submission):
        """ Grade Descriptive Question """
        pass

    def grade_programming(self, submission):
        """ Grade Programming Question """
        pass
