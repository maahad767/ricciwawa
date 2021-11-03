from django.contrib.auth import get_user_model
from django.db import models

from post.models import Post


class Quiz(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,
                             on_delete=models.CASCADE,
                             related_name="%(app_label)s_%(class)s_related",
                             related_query_name="%(app_label)s_%(class)ss",
                             )
    title = models.CharField(max_length=256)
    question = models.TextField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(null=True)
    points = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class MultipleChoiceQuestion(Question):
    has_multiple_correct_choices = models.BooleanField(default=False)


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='choices')
    position = models.PositiveSmallIntegerField(null=True, blank=True)
    choice_text = models.TextField(null=True)
    is_correct_choice = models.BooleanField(default=False)
    explanation = models.TextField(null=True, blank=True)
    attachment = models.JSONField(null=True, blank=True)


class InputAnswerQuestion(Question):
    answer = models.TextField()
    attachment = models.JSONField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)


class QuizAttempt(models.Model):
    examinee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_first_attempt = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt,
                                     on_delete=models.CASCADE,
                                     related_name="%(app_label)s_%(class)s_related",
                                     related_query_name="%(app_label)s_%(class)ss",
                                     )
    points_achieved = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class MultipleChoiceQuestionAttempt(QuestionAttempt):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice, related_name='selected_choices')


class InputAnswerQuestionAttempt(QuestionAttempt):
    question = models.ForeignKey(InputAnswerQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField()
