from django.db import models
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator

# Create your models here.
class Discipline(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)

class Level(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)

    def __str__(self):
        return self.name

class Courses(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.level.name +' '+ self.name



ANSWER_ORDER_OPTIONS = (
    ('content', ('Content')),
    ('random', ('Random')),
    ('none', ('None'))
)

# model to store user choice for mcq
class Question(models.Model):
    content = models.TextField(blank=False)
    answer_order = models.CharField(max_length=30, null=True, blank=True, choices=ANSWER_ORDER_OPTIONS, help_text=("The order in which multichoice answer options are displayed to the user"))

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset
    
    def __str__(self) -> str:
        return self.content
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    is_answer = models.BooleanField(blank=False, default=False)

    def __str__(self) -> str:
        return self.content



# model to store respective quiz(exams)
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    examiner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)

    # features of quiz
    single_attempt = models.BooleanField(blank=False, default=True)
    random_order = models.BooleanField(blank=False, default=True, help_text='orders with which questions will appear')
    max_questions = models.PositiveIntegerField(help_text='Display the questions in a random order or as they are set?')
    duration = models.IntegerField(help_text='duration in minutes')
    start_time =models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.level.name+' ' + self.title

    # creating options field from opt1... opt4 by overiding the save() method
    """
    
    def save(self, *args, **kwargs):
        self.choices = []
        # get course query set
        c = Courses.objects.all()
        # loop throught d query set and save it in choices variable
        for course in c:
            self.choices.append(
                (course.id, course)
            )
        
        self.course = models.ForeignKey(Courses, on_delete=models.CASCADE, choices=self.choices, null=True)
        super().save(*args, **kwargs)

    """

# model to store User sitting (exams attempt)
class Sitting(models.Model):
    """
    used to store the progress of users taking a quiz.
    
    Questions_all = scheduled questions for a particular sitting
    Questions_unattempted = questions left to be answered
    Questions_attempted = questions answered
    Questions_failed = questions with wrong user choice
    Questions_passed = questions with correct user choice
    Question_Choice_pair = just as the name suggest; json

    Questions_unattempted = Questions_all - Questions_attempted
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    quiz = models.ForeignKey(Quiz,on_delete=models.DO_NOTHING)
    question_all = models.CharField(max_length=1024, verbose_name='All Questions', validators=[validate_comma_separated_integer_list])
    question_unattempted = models.CharField(max_length=1024, verbose_name='Unanswered Questions', validators=[validate_comma_separated_integer_list])
    question_failed = models.CharField(max_length=1024, verbose_name='Failed Questions', validators=[validate_comma_separated_integer_list])
    question_passed = models.CharField(max_length=1024, verbose_name='Passed Questions', validators=[validate_comma_separated_integer_list])
    question_choice_pair = models.JSONField(blank=True, default='{}', help_text='json format question choice pair')
    is_attempted = models.BooleanField('if any attempt', default=False)
    current_score = models.IntegerField()
    start_time =models.DateTimeField(auto_now_add=True)




class UserGuess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    quiz = models.ForeignKey(Quiz,null=True, on_delete=models.DO_NOTHING)
    # guess = models.ForeignKey(Choice,on_delete=models.DO_NOTHING, null=True, )
    guess = models.JSONField()

class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    quiz = models.ForeignKey(Quiz,null=True, on_delete=models.DO_NOTHING)
    score = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.student.first_name


