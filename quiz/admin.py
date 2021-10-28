from django.contrib import admin

from .models import Quiz, MultipleChoiceQuestion, InputAnswerQuestion, Choice, AttemptQuiz, \
    AttemptMultipleChoiceQuestion, AttemptChoice, AttemptInputAnswerQuestion


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


@admin.register(AttemptQuiz)
class AttemptQuizAdmin(admin.ModelAdmin):
    pass


@admin.register(AttemptInputAnswerQuestion)
class AttemptInputAnswerQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(AttemptMultipleChoiceQuestion)
class AttemptMultipleChoiceQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(AttemptChoice)
class AttemptChoiceAdmin(admin.ModelAdmin):
    pass
