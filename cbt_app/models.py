from django.db import models
from django.db.models import Min, Max,Count
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator
import json

# Create your models here.
class Discipline(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)
    def __str__(self):
        return self.name
class Level(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)

    def __str__(self):
        return self.name

class Courses(models.Model):
    name = models.CharField(max_length=50,blank=False, unique=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.level.name +' '+ self.name

class Topic(models.Model):
    courses= models.ForeignKey(Courses, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=50,blank=False)

    class Meta:
        unique_together=[['courses','name']]
    def __str__(self):
        return self.name

ANSWER_ORDER_OPTIONS = (
    ('content', ('Content')),
    ('random', ('Random')),
    ('none', ('None'))
)

# model to store user choice for mcq
class Question(models.Model):
    content = models.TextField(blank=False)
    topic = models.ManyToManyField(Topic)
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


class SittingManager(models.Manager):
    def new_sitting(self, user, quiz):
        if quiz.random_order:
            question_set = quiz.questions.all().order_by('?')
        else:
            question_set = quiz.questions.all()
        
        # store the question id in a list
        question_set = [quest.id for quest in question_set]
        # check if max number of question, return list of that size if yes
        # question_set = question_set[:len(question_set) and len(question_set)>quiz.max_questions]
        question_set = question_set[:quiz.max_questions]
                                    
        # convert the question list to a string separated by a comma
        question_set = ','.join(map(str,question_set))

        sitting = self.create(
            user=user,quiz=quiz,
            question_all=question_set,
            question_unattempted=question_set,
            question_failed ='',
            question_passed='',
            question_choice_pair ='{}',
            is_completed = False,
            current_score = 0
            )
        return sitting

    def check_sitting(self,user,quiz):
        # check if already attempted the quiz for single_attempt quiz
        if quiz.single_attempt and self.filter(user=user,quiz=quiz,is_completed=True):
            return False
        
        # check for uncompleted quiz instance to resume, else create new one
        try:
            sitting = self.get(user=user, quiz=quiz, is_completed =False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user,quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, is_completed = False)[0]

        return sitting

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
    question_attempted = models.CharField(max_length=1024, verbose_name='Answered Questions', validators=[validate_comma_separated_integer_list])
    question_unattempted = models.CharField(max_length=1024, verbose_name='Unanswered Questions', validators=[validate_comma_separated_integer_list])
    question_failed = models.CharField(max_length=1024, verbose_name='Failed Questions', validators=[validate_comma_separated_integer_list])
    question_passed = models.CharField(max_length=1024, verbose_name='Passed Questions', validators=[validate_comma_separated_integer_list])
    question_choice_pair = models.JSONField(blank=True, default=dict, help_text='json format question choice pair')
    is_completed = models.BooleanField('Is completed', default=False)
    current_score = models.IntegerField(default=0)
    start_time =models.DateTimeField(auto_now_add=True)
    end_time =models.DateTimeField(null=True, blank=True)
    
    objects = models.Manager()
    sits = SittingManager()

    def __str__(self):
        return str(self.user) + ' result for '+str(self.quiz.title)

    # first_10 =[]
    def get_questions_in_10s(self):
        '''
        returns a list of atmost 10 question from question_all list
        '''
        if self.question_unattempted:
            # question_id in int list
            # convert id of strings to list of int(id)
            all_quest = list(map(int,self.question_unattempted.split(',')))
            self.first_10 = all_quest[:2]
            
            # # remove first_10 from question_all list(remaining quest)
            # minus_first_10_int = [x for x in all_quest if x not in self.first_10 ]
            # # update unattempted questions, converted to str
            # self.question_unattempted = ','.join(map(str,minus_first_10_int))
            
            return Question.objects.filter(id__in= self.first_10)
    
    def remove_question_in_10s(self):
        '''
        remove 1 to 10 questions from the sitting (question all) list 
        '''

        if self.question_all:
            all_quest = list(map(int,self.question_unattempted.split(',')))
            # remove first_10 from question_all list(remaining quest)
            # minus_first_10_int = [x for x in all_quest if x not in self.first_10 ]
            minus_first_10_int = all_quest[2: ]
            # update unattempted questions, converted to str
            self.question_unattempted = ','.join(map(str,minus_first_10_int))
            self.save()
    
    def sitting_complete(self):
        self.is_completed=True
        self.end_time = now()
        self.save()
    
    def record_attempt(self,quest,quest_choice):
        # attempted question list
        # get previous attempt_question, extend it with new quest
        previous_attempt =self.question_attempted.split(',')
        if previous_attempt and previous_attempt != ['']:
            print(f'old values are {previous_attempt}')
            self.quest = list(map(int,self.question_attempted.split(',')))
            self.quest.extend(quest)
            question_set = ','.join(map(str,self.quest))
        else:
            question_set = ','.join(map(str,quest))
        self.question_attempted = question_set

        # question_choice pair
        self.quest_pair = json.loads(self.question_choice_pair)
        print(f'this is json load {self.quest_pair}')
        for k,v in quest_choice.items():
            self.quest_pair[k] = v
        self.question_choice_pair = json.dumps(self.quest_pair)
        print(f'this is json dump {self.question_choice_pair}')

        # score
        # if a particular choice exist in question-pair
        c=Choice.objects.filter(id__in=self.quest_pair.values())

        # sum all choice with is_answer == true, store result in dict correct
        # models.functions.cast does type casting of boolean to int that it might be working in postgresql
        correct= c.aggregate(count = models.Sum(models.functions.Cast('is_answer',models.IntegerField())))
        self.current_score = correct['count']
    
        self.end_time = now()
        self.save()

    def get_score(self):
        all_quest = list(map(int,self.question_all.split(',')))
        total_quest = len(all_quest)
        total_points = self.current_score
        percent_score = (total_points/total_quest)*100
        return round(percent_score,2)

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


