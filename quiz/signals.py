from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Quiz, MultipleChoiceQuestion, InputAnswerQuestion, MultipleChoiceQuestionAttempt,\
    QuizAttempt, MultipleChoiceQuestionAttempt, InputAnswerQuestionAttempt


# def grade_quiz_attempt(instance, created, *args, **kwargs):
#     if not created:
#         return
#     quiz = instance.quiz
#     mcq_questions = quiz.quiz_multiplechoicequestion_related.all()
#     ia_questions = quiz.quiz_inputanswerquestion_related.all()
#     mcq_attempts = instance.quiz_multiplechoicequestionattempt_related.all()
#     ia_attempts = instance.quiz_inputanswerquestionattempt_related.all()
#
#     for mcq, mcqa in zip(mcq_questions, mcq_attempts):
#         correct_choices = mcq.choices.all().filter(is_correct_choice=True)
#         selected_choices = mcqa.selected_choices.all()
#
#         if list(correct_choices) == list(selected_choices):
#             mcqa.points_achieved = mcq.points
#         else:
#             mcqa.points_achieved = 0
#
#     for iaq, iaqa in zip(ia_questions, ia_attempts):
#         if iaq.answer == iaqa.user_answer:
#             iaqa.points_achieved = iaq.points
#         else:
#             iaqa.points_achieved = 0
