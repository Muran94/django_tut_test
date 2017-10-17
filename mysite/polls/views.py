from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("こんにちは！")

def detail(request, question_id):
    return HttpResponse("質問%sの詳細ページです" % question_id)

def results(request, question_id):
    return HttpResponse("質問%sの投票結果ページです" % question_id)

def vote(request, question_id):
    return HttpResponse("質問%sの投票結果ページです" % question_id)
