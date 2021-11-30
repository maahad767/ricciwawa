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

    @property
    def total_points(self):
        mcq_marks = self.quiz_multiplechoicequestion_related.aggregate(models.Sum('points'))['points__sum'] or 0
        iaq_marks = self.quiz_inputanswerquestion_related.aggregate(models.Sum('points'))['points__sum'] or 0
        return mcq_marks + iaq_marks

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.creator == request.user

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


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

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.quiz.creator == request.user

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['position']


class MultipleChoiceQuestion(Question):
    has_multiple_correct_choices = models.BooleanField(default=False)

    @property
    def get_total_attempts(self):
        return self.multiplechoicequestionattempt_set.count()


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='choices')
    position = models.PositiveSmallIntegerField(null=True, blank=True)
    choice_text = models.TextField(null=True)
    is_correct_choice = models.BooleanField(default=False)
    explanation = models.TextField(null=True, blank=True)
    attachment = models.JSONField(null=True, blank=True)

    @property
    def get_total_questions_selected_choice(self):
        return self.questions_selected_choices.count()

    @property
    def get_users_selected(self):
        return self.questions_selected_choices.values_list('quiz_attempt__examinee__username', flat=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.question.has_object_write_permission(request)

    def __str__(self):
        return self.choice_text

    class Meta:
        ordering = ['position']


class InputAnswerQuestion(Question):
    answer = models.TextField()
    attachment = models.JSONField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)

    @property
    def get_question_attempts(self):
        return self.inputanswerquestionattempt_set.count()


class QuizAttempt(models.Model):
    examinee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_first_attempt = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_points_achieved(self):
        mcq_marks = self.quiz_multiplechoicequestionattempt_related.aggregate(
            models.Sum('points_achieved'))['points_achieved__sum'] or 0
        iaq_marks = self.quiz_inputanswerquestionattempt_related.aggregate(models.Sum('points_achieved'))[
            'points_achieved__sum'] or 0
        return mcq_marks + iaq_marks

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.examinee == request.user

    class Meta:
        ordering = ['created_at']


class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt,
                                     on_delete=models.CASCADE,
                                     related_name="%(app_label)s_%(class)s_related",
                                     related_query_name="%(app_label)s_%(class)ss",
                                     )
    points_achieved = models.PositiveSmallIntegerField(null=True, blank=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.quiz_attempt.has_object_write_permission(request)

    class Meta:
        abstract = True


class MultipleChoiceQuestionAttempt(QuestionAttempt):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice, related_name='questions_selected_choices')


class InputAnswerQuestionAttempt(QuestionAttempt):
    question = models.ForeignKey(InputAnswerQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField()
