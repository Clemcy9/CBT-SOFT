from django.db import models
from django.conf import settings

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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, max_length=16)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Courses)
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.user
    
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
    examiner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    single_attempt = models.BooleanField(blank=False, default=True)
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

class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    score = models.IntegerField()

    def __str__(self) -> str:
        return self.student.first_name


