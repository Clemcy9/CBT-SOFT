from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from .forms import QuestionUploadForm, CourseTemplate

# Create your views here.

def question_upload(request):
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST)
        if form.is_valid():
            form.save()
            print(f'errors: {form.errors}')
            return HttpResponse('successfully Uploaded')
        else:
            print(f'error:{request.POST}')
            print(f'errors2: {form.errors}')
            messages.error(request,'something went wrong')
            form = QuestionUploadForm(request.POST)
            return render(request, 'question_upload.html',{'form':form})
    form = QuestionUploadForm()
    
    return render(request, 'question_upload.html',{'form':form})