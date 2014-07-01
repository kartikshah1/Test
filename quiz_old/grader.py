"""
Grader class to handle assessment of submissions
"""
from quiz.models import Question, QuestionHistory, Submission


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

    def update_marks(self, is_correct=True):
        """
        Get and update the marks for this submission
        Update question history
        Applicable for Direct Grading ONLY
        """
        if self.question is None:
            self.question = \
                Question.objects.get(question=self.submission.question)
        if self.question_history is None:
            self.question_history = QuestionHistory.objects.filter(
                                              question=self.question,
                                              user=self.submission.user)
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

            self.submission.result = marks

        else:
            self.question_history.status = QuestionHistory.ATTEMPTED_ONCE

        if (self.question_history.attempts >= self.question.attempts or
            self.question_history.status == QuestionHistory.SOLVED):
            self.question_history.answer_shown = True
        self.question_history.save()

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
            
            if self.submission.question.type == \
                Question.SINGLE_CHOICE_QUESTION:
                pass
            
            elif self.submission.question.type == \
                Question.MULTIPLE_CHOICE_QUESTION:
                pass
            
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
        correct = False
        for ans in correct_answer:
            if ans == answer:
                correct = True
                break
        self.update_marks(correct)

    def grade_single_choice(self, answer, correct_answer, submission):
        """ Grade single choice correct  Question """
        pass

    def grade_multiple_choice(self, answer, correct_answer, submission):
        """ Grade Multiple choice correct Question """
        pass

    def grade_descriptive_answer(self, answer, correct_answer, submission):
        """ Grade Descriptive Question """
        pass

    def grade_programming(self, submission):
        """ Grade Programming Question """
        pass
