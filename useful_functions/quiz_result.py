import re

# regex below matches 1 to infinix *(1000) digit at the end of a string
id = re.compile(r'[0-9]{1,}$')
text = 'hello how are you doing 45, and2 mummy 13'
res =id.findall(text) #returns a list
# print(id.search(text).group())
# print(res)


def question_choice_pair(querydict):
    """
    returns a tuple of dictionary containing (question_id:choice_id, and total questions)
    """
    print(querydict)
    all_questions =[]
    question_answer_pair ={} #diction of quest_id:choice_id pair
    found_key=''
    found_choice=' '
    for key,value in querydict.items():
        if re.search(r'^question',key):
            # print(f'questions are {key + ":" + value[0] }')
            found_key = value[0]
            all_questions.append(found_key)
        if re.search(r'^choice',key):
            print(f'choices quest_id: {key + ":" + value[0] }')
            found_choice = key
        try :
            quest_id = id.search(found_key).group()
            print(f'quest_id = {quest_id}')
            try:
                choice_id = id.search(found_choice).group()
                print(f'choice_id = {choice_id}')
                if quest_id == choice_id:
                    question_answer_pair[found_key] = querydict[found_choice][0]
            except:
                print('no choice only question found')
                # if only question without choice, give null
                question_answer_pair[found_key] =None
        except:
            print('no match found')
    return question_answer_pair,all_questions

def mark_quiz(result, model):
    my_result = []
    for question,choice in result.items():
        try:
            is_correct = model.objects.get(id=choice).is_answer 
            if is_correct:
                my_result.append(1)
            else:
                my_result.append(0)
            print(f'my_result is : {my_result}')
        except:
            my_result.append(0)
    return my_result

def score(marks,no_of_questions):
    """returns the score in percentage for a given test"""
    points =marks.count(1)
    total_questions = len(no_of_questions)
    percent_score = (points/total_questions)*100
    return percent_score
    

# # testing
# content3 ={
#     'csrfmiddlewaretoken': ['JsL0S1OoeGKJlomeW27jg4orwLM0v57etUWcuL9ncJAuN77PSceRSPTo8eintTdz'], 'question2': ['2'], 
#     'choice2': ['4'], 
#     'question1': ['1'], 
#     'choice1': ['2'], 
#     'question3': ['3'], 
#     'choice3': ['9']
#     }

# print(f'testing {match_question_with_choice(content3)}')

'''
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('registration successful')
    else:  
        form = RegisterForm()
    return render(request, 'register.html', {'forms':form})
'''


"""
def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST['questions']
        print(f'questions are {questions}')
        each = [x for x in questions.contents]
        print(f'each is:{each}')
        results = {} #empty dict for storing question and choosen option
        # print(f'this is all data: {request.POST}')
        for question, choice in request.POST:
            results={request.POST.extend}
            results[r'^quest'] = request.POST[r'']


        # for i in range(1,5):
        #     question = request.POST['question'+str(i)]
        #     choice = request.POST['choice'+str(i)]
        #     results[question] = choice
        #     final_results = mark_quiz(results)
        #     return HttpResponse( f'your result is {final_results}')
"""
"""
@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')
    paginator = Paginator(contents, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data = [
        {'question':x,'guess':x.choice_set.all()} for x in contents
        # {
        #     'question':'how old was Jesus when he died',
        #     'choices' :[1,23,45,33]

        # }
    ]

    QuizFormSet = formset_factory(QuizForm,extra=5)
    QuizFormSet = QuizFormSet(initial=data)
    context = {
        # 'contents':contents,
        'page_obj':page_obj,
        'formset': QuizFormSet
    }
    return render(request, 'quiz.html', context)
"""
