from django.shortcuts import get_object_or_404, render
from .models import Question
from django.http import Http404
# do not need below two after refactor for index, but the other views need.
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)
'''
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)
	template = loader.get_template('polls/index.html')
	#The context is a dictionary mapping template variable names to Python objects
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))
'''
def detail(request, question_id):
	#return HttpResponse("You are looking at question %s." %question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})
''' refactor to above code
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})
'''
''' !!!important!!!
Why do we use a helper function get_object_or_404() instead of automatically 
catching the ObjectDoesNotExist exceptions at a higher level, or having the 
model API raise Http404 instead of ObjectDoesNotExist?
Because that would couple the model layer to the view layer. 
One of the foremost design goals of Django is to maintain loose coupling. 
'''
def results(request, question_id):
	response = "you are looing at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("you are voting on question %s." %question_id)