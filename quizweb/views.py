from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView,View,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from quizweb.forms import RegistrationForm,SignInForm

from quiz.models import Category,Questions,QuizRecord

import random

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

@signin_required
@never_cache
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect('signin')

class RegistrationView(CreateView):
    form_class=RegistrationForm
    model=User
    template_name='register.html'
    success_url=reverse_lazy('signin')

    def form_valid(self, form):
        messages.success(self.request,'account has been created')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'failed to create account')
        return super().form_invalid(form)
    
class SignInView(FormView):
    form_class=SignInForm
    template_name='signin.html'
    success_url=reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect('home')
        return render(request,self.template_name,{'form':form})    

@method_decorator(decs,name='dispatch')
class IndexView(TemplateView):
    template_name='home.html'

@method_decorator(decs,name='dispatch')
class QuizHomeView(View):
    def get(self,request,*args,**kwargs):
        qs=Category.objects.all()
        return render(request,'quiz-home.html',{'cats':qs})
    
    def post(self,request,*args,**kwargs):
        cat=request.POST.get('category')
        mode=request.POST.get('mode')
        print(cat,mode)
        return redirect('questions-list',cat=cat,mode=mode)
    

from django.db.models import Sum
@method_decorator(decs,name='dispatch')
class QuestionListView(View):
    def get(self,request,*args,**kwargs):
        category=kwargs.get('cat')
        mode=kwargs.get('mode')
        qs=list(Questions.objects.filter(mode=mode,category__name=category))
        random.shuffle(qs)
        return render(request,'question-list.html',{'questions':qs,'mode':mode,'category':category})

    def post(self,request,*args,**kwargs):
        data=request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        questions_attended=len(data)
        marks_obtained=0
        wrong_answer_count=0
        for q,ans in data.items():
            question=Questions.objects.get(question=q)
            right_answer_obj=question.answer
            if(right_answer_obj.options==ans):
                marks_obtained=marks_obtained+question.mark

            else:
                wrong_answer_count+=1
            right_answer_count=questions_attended-wrong_answer_count
        print(marks_obtained,questions_attended,wrong_answer_count,right_answer_count)

        category=kwargs.get('cat')
        mode=kwargs.get('mode')
        result=''
        total=Questions.objects.filter(mode=mode,category__name=category).aggregate(Sum('mark')).get('mark__sum')
        if total/2 <= marks_obtained:
            result='pass'
        else:
            result='failed'


        data=QuizRecord.objects.create(marks_obtained=marks_obtained,right_answer_count=right_answer_count,wrong_answer_count=wrong_answer_count,user=request.user)
        return render(request,'quiz-mark.html',{'marks_obtained':marks_obtained,'question_attended':questions_attended,'result':result,'right_answer_count':right_answer_count,'wrong_answer_count':wrong_answer_count})
        

@method_decorator(decs,name='dispatch')
class QuizRecordView(ListView):
    model=QuizRecord
    template_name='quiz-record.html'
    context_object_name='records'

    def get_queryset(self):
        return QuizRecord.objects.filter(user=self.request.user)