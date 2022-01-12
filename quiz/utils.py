

def grade_quiz_attempt(instance):
    quiz = instance.quiz
    mcq_questions = quiz.quiz_multiplechoicequestion_related.all()
    ia_questions = quiz.quiz_inputanswerquestion_related.all()
    mcq_attempts = instance.quiz_multiplechoicequestionattempt_related.all()
    ia_attempts = instance.quiz_inputanswerquestionattempt_related.all()

    for mcq, mcqa in zip(mcq_questions, mcq_attempts):
        correct_choices = mcq.choices.all().filter(is_correct_choice=True)
        selected_choices = mcqa.selected_choices.all()

        if list(correct_choices) == list(selected_choices):
            mcqa.points_achieved = mcq.points
            mcqa.save()
    for iaq, iaqa in zip(ia_questions, ia_attempts):
        if iaq.answer == iaqa.user_answer:
            iaqa.points_achieved = iaq.points
            iaqa.save()
    instance.save()
