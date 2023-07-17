from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.formsets import formset_factory
from django.core import serializers
from cbt_app.models import Quiz, Sitting, Question, Courses, Level
from auth1.models import User, Profile
from .forms import QuestionChoiceForm

# Create your views here.

# just form
def form_quiz(request):
    # query set
    question = Question.objects.get(id =19)
    if request.method == 'POST':
        form = QuestionChoiceForm(request.POST, quest =question)

    # form instantiation
    form = QuestionChoiceForm(quest=question)
    return render(request, 'justform.html',{'form':form})

# paginate
def paginator_quiz(request):
    questions = Question.objects.all()[:30]
    quest_choice_pair = {x:x.choice_set.all() for x in questions}
    paginator = Paginator(questions, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f'this is pageobj.. ={page_obj.object_list}\nfunction include {dir(page_obj)}')
    return render(request, 'paginated_quiz.html', {'page_obj': page_obj})


# paginate with formset
def formset_quiz(request):
    # queryset
    questions = Question.objects.all()[:30]
    quest_choice_pair = {x:x.choice_set.all() for x in questions}

    # paginator
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # formset
    formset = formset_factory(QuestionChoiceForm())
    formset
    return render(request, 'paginated_quiz.html', {'page_obj': page_obj})

def jscript_quiz(request):
    
    return render(request,'paginated_jscript.html')

def get_questions(request):
    questions_db = Question.objects.all()[:20]
    
    questions = []
    for q in questions_db:
        answer =[]
        for a in q.choice_set.all():
            answer.append(a.content)
        questions.append({q.content:answer})
    # json_data = serializers.serialize('json',questions)
    # print(f'question and choice are {questions}')
    return JsonResponse({'questions':questions}, safe=False)