from matchmaker.models import Candidate, FamilyMember, Party, Question, Race, Answer
from django.contrib.auth.models import User
from django.contrib import admin

class FamilyInline(admin.TabularInline):
    model = FamilyMember
    extra = 3

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'party', 'race')
    list_filter = ['party', 'race']
    search_fields = ['user']
    fieldsets=[
        ("Bio", {'fields':['user','birthday', 'occupation', 'education']}),
        (None, {'fields':['race', 'party','accolades', 'genStatement', ]}),
        ("Web Stuff", {'fields':['website', 'twitter', 'facebook', 'mugshot']})
    ]
    inlines = [FamilyInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'candidate', 'edits')
    list_filter = ['question', 'candidate']
    search_fields = ['answer']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    seach_fields = ['question']
    filter_horizontal = ['race']



admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Party)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Race)
admin.site.register(Answer, AnswerAdmin)