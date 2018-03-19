from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse


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
''' !!!good to know!!!
Why do we use a helper function get_object_or_404() instead of automatically 
catching the ObjectDoesNotExist exceptions at a higher level, or having the 
model API raise Http404 instead of ObjectDoesNotExist?
Because that would couple the model layer to the view layer. 
One of the foremost design goals of Django is to maintain loose coupling. 
'''
def results(request, question_id):
	#response = "you are looing at the results of question %s."
	#return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	#return HttpResponse("you are voting on question %s." %question_id)
	# Problem of this vote view: db update at the same time by different user.
	# refer to:Avoiding race conditions using F() 
	question = get_object_or_404(Question, pk=question_id)
	try:
		# request.POST: a dictionary-like object that lets you access submitted data by key name
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# !!!good to do!!!
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))