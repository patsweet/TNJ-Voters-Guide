from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from matchmaker.models import Candidate, Race, FamilyMember, Question, Answer
from matchmaker.forms import *
from datetime import date

# Main Page with all races.
def index(request):
    today = date.today()
    race_list = []
    unopposed = []
    rList = Race.objects.filter(election_date__gte=today).order_by('race')
    past_races = Race.objects.filter(election_date__lte=today).order_by('race')
    for r in rList:
        c = Candidate.objects.filter(race=r)
        if len(c) > 1:
            race_list.append(r)
        else:
            unopposed.append(r)
    variables = RequestContext(request, {
        'past_races': past_races,
        'race_list': race_list,
        'unopposed': unopposed,
        'user': request.user
    })

    return render_to_response('matchmaker/index.html', variables)

# Logout User
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/matchmaker/')

# Page with list of candidates for the specified race.
def race_page(request, Race_id):

    candidate_list = Candidate.objects.filter(race__exact=Race_id)
    race_info = Race.objects.get(id__exact=Race_id)

    variables = RequestContext(request, {
        'candidate_list':candidate_list,
        'race_info':race_info,
    })
    
    return render_to_response('matchmaker/candidate_list.html', variables)

# Candidate Bio Page
def candidate_page(request, Race_id, Candidate_id):
    # Candidate information
    candidate_info = Candidate.objects.get(id__exact=Candidate_id)
    family_info = FamilyMember.objects.filter(candidate__exact=Candidate_id)

    # Calculate Candidates Age
    today = date.today()
    born = candidate_info.birthday
    if born:
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            candidate_age = today.year - born.year - 1
        else:
            candidate_age = today.year - born.year
    else:
        candidate_age = "Not Provided"

    # Race Info for the Header and Footer information
    race_info = Race.objects.get(id__exact=Race_id)

    # Info for the main section.
    question_list = Question.objects.filter(race__exact=Race_id)

    qAndA = []
    for q in question_list:
        try:
            aobject = Answer.objects.get(candidate__exact=Candidate_id, question__exact=q)
            a = aobject.answer
        except:
            a = "Candidate hasn't answered this question yet."
        qAndA.append([q.question,a])

    answer_list = Answer.objects.filter(candidate__exact=Candidate_id)
    
    # Information for the footer
    candidate_list = Candidate.objects.filter(race__exact=Race_id)

    variables = RequestContext(request, {
        'candidate_age': candidate_age,
        'candidate_info':candidate_info,
        'candidate_list':candidate_list,
        'race_info':race_info,
        'family_info':family_info,
        'question_list':question_list,
        'answer_list':answer_list,
        'qAndA': qAndA,
    })

    return render_to_response('matchmaker/candidate_page.html', variables)

def matchmaker_game(request, Race_id):
    candidates = Candidate.objects.filter(race__exact=Race_id)
    questions = Question.objects.filter(race__exact=Race_id)
    race_info = Race.objects.get(id__exact=Race_id)
    cand_info = []
    for question in questions:
        for candidate in candidates:
            try:
                a = Answer.objects.get(candidate__exact=candidate, question__exact=question)
                answer = a.answer
            except:
                answer = "No answer provided."
            cand_info.append([candidate, question, answer])

    variables = RequestContext(request, {
        'cand_info':cand_info,
        'user': request.user,
        'questions':questions,
        'race_info':race_info
        })
    return render_to_response('matchmaker/matchmaker_game.html', variables)

@login_required
def update_answers(request):
    
    user = Candidate.objects.get(user__exact=request.user)
    question_list = Question.objects.filter(race__exact=user.race)
    
    answer_list = []
    for question in question_list:
        answer, created = Answer.objects.get_or_create(question_id=question.id, candidate_id=user.id, defaults={'answer': "No response given."})
        answer_list.append([answer, created])

    if request.method == 'POST':
        form_list = []
        x = 0
        for answer, created in answer_list:
            form_list.append([answer.question, UpdateQandA(request.POST, prefix=str(x), instance=answer)])
            x += 1
        for question, form in form_list:
            if form.is_valid():
                form.save()
        return HttpResponseRedirect('/matchmaker/%d/%s/' % (user.race.id, user.id))
    else:
        form_list = []
        x = 0
        for answer, created in answer_list:
            if created==False:
                pass
            else:
                form_list.append([answer.question, UpdateQandA(prefix=str(x), instance=answer)])
            x += 1

    variables = RequestContext(request, {
        'form_list':form_list,
        'user': user,
        })
    return render_to_response('registration/UpdateAnswers.html', variables)


@login_required
def update_page(request):
    candidate = Candidate.objects.get(user__exact=request.user)
    if request.method == 'POST':
        pForm = ProfileForm(request.POST, request.FILES, instance=candidate)
        if pForm.is_valid():
            pForm.save()
            return HttpResponseRedirect('/matchmaker/%d/%s/' % (candidate.race.id, candidate.id) )
    else:
        pForm = ProfileForm(instance=candidate, label_suffix='')
    variables = RequestContext(request, {
        'pForm': pForm,
        'user': candidate,
    })

    return render_to_response('registration/UpdateCandidate.html', variables)


