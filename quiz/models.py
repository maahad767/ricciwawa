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
    has_multiple_correct_choices = models.BooleanField(default=False)


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

    class Meta:
        abstract = True


class AttemptMultipleChoiceQuestion(AttemptQuestion):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)


class AttemptChoice(models.Model):
    question_attempt = models.ForeignKey(AttemptMultipleChoiceQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)


class AttemptInputAnswerQuestion(AttemptQuestion):
    question = models.ForeignKey(InputAnswerQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField()
