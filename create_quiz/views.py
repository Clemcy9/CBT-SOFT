from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateByTopicForm
from cbt_app.models import UploadTitle, Question, Quiz

# Create your views here.


# create quiz funtions
def create_quiz(questions,**kwargs):
    """examiner = kwargs['user']
    title =kwargs['title']
    course = kwargs['course']
    level = kwargs['level']
    max_questions = kwargs['max_questions']
    duration = kwargs['duration']
    is_available = kwargs['is_available']"""
    
    # quiz = Quiz(examiner=user,title=title, course = course,level =level,max_questions=max_questions,end_time=now(), duration=duration,is_available=activate)

    print(f'kwargs is {kwargs}')

    quiz = Quiz(end_time=now(), **kwargs)
    quiz.save()
    for quest in kwargs['questions']:
        quiz.questions.add(quest)
    quiz.save()
    print('quiz created successfully')

def create_quiz_by_uploads(user,title,course,uploading,duration,activate):
    uploading.join() #wait for uploading to complete
    print('starting quiz creation')
    print(f'user is = {user}\ntitle = {title}\ncourse ={course}\ntype of course ={type(course)}')
    level = course.level
    print('uploading completed, now creating quiz')
    # questions = Question.objects.filter(upload_title=title)
    # uploaded title object
    ut = UploadTitle.objects.filter(examiner=user,title=title)[0]
    questions = ut.question_set.all()
    total_questions = questions.count()
    print(f'total questions are {total_questions}')
    data = {
        'examiner' : user,
        'title' :title,
        'course' : course,
        'level' : level,
        'max_questions' : total_questions,
        'duration' : duration,
        'is_available' : activate,
    }
    create_quiz(questions=questions, kwargs= data)
    return True

def create_quiz_by_topic(request):
    if request.method == 'POST':
        form = CreateByTopicForm(request.post, user = request.user)
        if form.is_valid():
            title = form.cleaned_data['title']
            course = form.cleaned_data['course']
            topic = form.cleaned_data['topic']
            max_no_question =form.cleaned_data['max_no_question']
            duration = form.cleaned_data['duration']
            activate = form.cleaned_data['activate']

            level = course.level
            questions = topic.question_set.all()
            data ={
                'examiner' : request.user,
                'title' :title,
                'course' : course,
                'level' : level,
                'max_questions' : max_no_question,
                'duration' : duration,
                'is_available' : activate,
            }
            create_quiz(questions=questions, kwargs= data)
            messages.info(request, f'Created quiz successfully')
            return HttpResponseRedirect(reverse('cbt_app:dashboard'))
        else:
            messages.error(request,'something went wrong')
            return render(request, template_name,{'form':form})

    form = CreateByTopicForm(user=request.user)
    return render(request, 'create_quiz_by_topic.html',{'form':form})



def create_quiz_by_random(title):
    pass
