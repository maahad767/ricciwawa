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
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    question = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MultipleChoiceQuestion(Question):
    pass


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    choice_text = models.TextField(null=True)
    is_correct_choice = models.BooleanField(default=False)


class InputAnswerQuestion(Question):
    answer = models.TextField()


class AttemptQuiz(models.Model):
    examinee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # total score


class AttemptQuestion(models.Model):
    quiz_attempt = models.ForeignKey(AttemptQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

