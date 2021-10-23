from django.contrib import admin

from .models import Quiz, MultipleChoiceQuestion, Choice


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass
