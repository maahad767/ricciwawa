from django.contrib import admin

from .models import Quiz, MultipleChoiceQuestion, InputAnswerQuestion, Choice, QuizAttempt, \
    MultipleChoiceQuestionAttempt, ChoiceAttempt, InputAnswerQuestionAttempt


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(InputAnswerQuestion)
class InputAnswerQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizAttempt)
class AttemptQuizAdmin(admin.ModelAdmin):
    pass


@admin.register(InputAnswerQuestionAttempt)
class AttemptInputAnswerQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceQuestionAttempt)
class AttemptMultipleChoiceQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(ChoiceAttempt)
class AttemptChoiceAdmin(admin.ModelAdmin):
    pass
