from django.urls import path, include
from .views import formset_quiz, form_quiz, paginator_quiz, jscript_quiz


app_name = "paginated_quiz"

urlpatterns=[
    path('paginator_quiz/', view=paginator_quiz, name='paginator_quiz'),
    path('form_quiz/', view=form_quiz, name='form_quiz'),
    path('quiz_js',view=jscript_quiz, name='js_quiz')
]