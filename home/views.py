from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Quiz, Question, Choice, UserQuiz
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'base.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def quiz_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    quizzes = category.quiz_set.all()
    
    return render(request, 'quiz_list.html', {'category': category, 'quizzes': quizzes})
pass


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    score = 0

    for question in questions:
        selected_choice = request.POST.get(str(question.id))
        if selected_choice:
            choice = get_object_or_404(Choice, pk=selected_choice)
            if choice.is_correct:
                score += 1

    UserQuiz.objects.create(user=request.user, quiz=quiz, score=score)
    return redirect('quiz_results', quiz_id=quiz.id)

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # user_quiz = get_object_or_404(UserQuiz, user=request.user, quiz=quiz)
    user_quiz = UserQuiz.objects.filter(user=request.user, quiz=quiz).first()
    if not user_quiz:
    # Handle case where no UserQuiz is found
        raise Http404("UserQuiz not found")
    return render(request, 'quiz_results.html', {'quiz': quiz, 'user_quiz': user_quiz})

@csrf_exempt
def signUp(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
    
        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        subject = 'Welcome TO Quiz Website'
        message = f'Hi {user.username}, thank you for registering in newsportal.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail( subject, message, email_from, recipient_list )
        return redirect('login')
   
       
    return render(request,'signup.html')

@csrf_exempt
def custom_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'you are successfully logged in')
            return redirect('category_list')
        else:
            messages.error(request,'invalid password or username')
    return render(request,'login.html')
