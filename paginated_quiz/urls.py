from django.urls import path, include
from .views import take_quiz_formset, take_quiz_form, take_quiz_paginate


app_name = "paginated_quiz"

urlpatterns=[
    path('take_quiz_paginate/', view=take_quiz_paginate, name='take_quiz_paginate'),
    path('take_quiz_form/', view=take_quiz_form, name='take_quiz_form')
]