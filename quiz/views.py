from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication,permissions

from quiz.models import Category,Questions,Answers
from quiz.serializers import CategorySerializer,QuestionSerializer,AnswerSerializer

# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    #  authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # localhost:8000/api/v1/categories/id/add_question
    @action(methods=['post'],detail=True)
    def add_question(self,request,*args,**kwargs):
        serializer=QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=self.get_object())
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class QuestionView(viewsets.ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    filter_backends=[DjangoFilterBackend]
    filterset_fields=['mode','mark']

    # localhost/8000/api/v1/questions/1/add_answers/
    @action(methods=['post'],detail=True)
    def add_answer(self,request,*args,**kwargs):
        serializer=AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=self.get_object())
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    
        




