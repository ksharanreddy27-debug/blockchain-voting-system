import random
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm
from .models import VoterProfile, Election, Candidate, Vote, LedgerEntry
from .blockchain import append_vote_anchor, verify_chain

def home(request):
    elections=Election.objects.filter(is_published=True).order_by('-created_at')
    return render(request,'voting/home.html',{'elections':elections})
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request,'Account created. Ask the administrator to approve your demo voter ID.'); return redirect('login')
    else: form=RegisterForm()
    return render(request,'voting/form.html',{'form':form,'title':'Voter registration'})
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid(): login(request,form.get_user()); return redirect('home')
    else: form=AuthenticationForm(request)
    return render(request,'voting/form.html',{'form':form,'title':'Sign in'})
def logout_view(request):
    logout(request); return redirect('home')
@login_required
def demo_otp(request):
    profile=getattr(request.user,'voterprofile',None)
    if not profile: return redirect('register')
    if request.method=='POST':
        # Demo only: fixed display-and-confirm OTP, not sent to a phone.
        if request.POST.get('otp')=='123456': profile.otp_verified=True; profile.save(); messages.success(request,'Demo OTP verified.'); return redirect('home')
        messages.error(request,'Incorrect demo OTP. Use 123456.')
    return render(request,'voting/otp.html')
@login_required
def cast_vote(request,election_id):
    profile=getattr(request.user,'voterprofile',None)
    if not profile or not profile.approved or not profile.otp_verified:
        messages.error(request,'Your demo voter account must be approved by an admin and OTP-verified before voting.'); return redirect('home')
    election=get_object_or_404(Election,id=election_id)
    if not election.is_open(): messages.error(request,'This election is not currently open.'); return redirect('home')
    if Vote.objects.filter(election=election,voter=profile).exists(): messages.warning(request,'You have already voted in this election.'); return redirect('home')
    candidates=election.candidates.all()
    if request.method=='POST':
        candidate=get_object_or_404(Candidate,id=request.POST.get('candidate'),election=election)
        try:
            with transaction.atomic():
                Vote.objects.create(election=election,candidate=candidate,voter=profile)
                append_vote_anchor(election.id)
            messages.success(request,'Vote recorded. Your vote receipt is anchored in the local tamper-evident ledger.')
            return redirect('home')
        except IntegrityError:
            messages.error(request,'A vote for this election was already recorded for your account.')
    return render(request,'voting/cast_vote.html',{'election':election,'candidates':candidates})
def results(request,election_id):
    election=get_object_or_404(Election,id=election_id)
    total=election.votes.count()
    rows=[{'candidate':c,'count':c.votes.count(),'percentage':round((c.votes.count()/total)*100) if total else 0} for c in election.candidates.all()]
    return render(request,'voting/results.html',{'election':election,'rows':rows,'total':total,'chain_ok':verify_chain()})
@user_passes_test(lambda u:u.is_staff)
def ledger(request):
    return render(request,'voting/ledger.html',{'entries':LedgerEntry.objects.order_by('-index')[:100],'chain_ok':verify_chain()})
