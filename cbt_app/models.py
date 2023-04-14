from django.db import models
from django.contrib.auth.models import AbstractUser

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

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    is_student = models.BooleanField('Are you a student?',blank=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username','is_student','password']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, max_length=16)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Courses)
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

ANSWER_ORDER_OPTIONS = (
    ('content', ('Content')),
    ('random', ('Random')),
    ('none', ('None'))
)

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

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    duration = models.TimeField()
    start_time =models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.title

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

class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    score = models.IntegerField()

    def __str__(self) -> str:
        return self.student.first_name


