from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Quiz, Question, Choice, UserQuiz
from django.contrib.auth.decorators import login_required
from django.http import Http404

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def quiz_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    quizzes = category.quiz_set.all()
    return render(request, 'quiz_list.html', {'category': category, 'quizzes': quizzes})

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
