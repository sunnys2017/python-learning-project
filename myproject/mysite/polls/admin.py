from django.contrib import admin

# Register your models here.
from .models import Choice, Question

#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date', 'question_text']
	search_fields = ['question_text']
	list_filter = ['pub_date']
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	fieldsets = [
		(None,	{'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline]

#tell the admin that Question objects have an admin interface
admin.site.register(Question, QuestionAdmin)