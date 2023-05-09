from django.contrib.auth import get_user_model,get_user

# quiz form
"""
<!-- <form action="{% url 'cbt_app:quiz_progress' %}" method="post">
        {% csrf_token %}
        
        {% for question in page_obj %}
            <legend>
                <h3>{{forloop.counter}}. {{question.content}} </h3>
            </legend>
            {% if error_message %}
            <p><strong>{{ error_message }}</strong></p>
            {% endif %}
            <input type="hidden" value="{{question.id}}" name="question{{question.id}}">
            <fieldset>
                {% for choice in question.choice_set.all %}
                    <input  type="radio" name="choice{{question.id}}" value="{{choice.id}}" required> 
                    <label for="choice{{question.id}}">{{choice.content}} </label> <br>
                {% endfor %}
            </fieldset>
        {% endfor %}
        <input type="submit" value="submit" style="margin-top: 2em;">
    </form> -->

    <div class="pagination"> <span class="step-links">
        {% if page_obj.has_previous %}
        <a href="?page=1">&laquo; first</a> <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}
        <span class="current">
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>
        {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">next</a> <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
        </span>
    </div>

    <!-- without pagination -->
    {% for question in contents %}
    <!-- <div class="question">
        <h3>{{question.content}}</h3>

        <div class="choice">
            {% for choice in question.choice_set.all %}
            <input type="radio" id="{{choice.id}}">{{choice}} <br>
            {% endfor %}
        </div>
    </div> -->
    {% endfor %}

    <!-- when using formset -->
    <!-- {% for form in formset %}
        {{form.as_p}}
        <p>hello</p>
    {% endfor %} -->
"""

# views.py
"""
# @login_required
# def take_quiz(request,quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)
#     questions = Question.objects.filter(quiz__id = quiz_id).order_by('?')[0:3]
#     paginator = Paginator(questions, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'questions':questions,
#         'page_obj':page_obj
#     }
#     return render(request, 'quiz.html', context)

"""

# javascript request (get) data async: frontend
"""
x = await fetch('http://127.0.0.1:8000/quiz/api/')
y = await x.json()
console.log(y)
"""