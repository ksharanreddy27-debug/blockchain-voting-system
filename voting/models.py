from django.conf import settings
from django.db import models
from django.utils import timezone
import hashlib, json

class VoterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=40, unique=True)
    approved = models.BooleanField(default=False)
    # Demo-only OTP flag. Do not use this as real identity verification.
    otp_verified = models.BooleanField(default=False)
    def __str__(self): return f'{self.user.username} ({self.voter_id})'

class Election(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_open(self):
        now=timezone.now()
        return self.is_published and self.starts_at <= now <= self.ends_at
    def __str__(self): return self.title

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=120)
    party = models.CharField(max_length=120, blank=True)
    manifesto = models.TextField(blank=True)
    def __str__(self): return f'{self.name} — {self.election.title}'

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.PROTECT, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='votes')
    voter = models.ForeignKey(VoterProfile, on_delete=models.PROTECT, related_name='votes')
    # A vote's candidate choice is kept in this academic demo database; this is NOT a secret-ballot production design.
    cast_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['election','voter'], name='one_vote_per_voter_per_election')]

class LedgerEntry(models.Model):
    index = models.PositiveIntegerField(unique=True)
    election_id_ref = models.PositiveIntegerField()
    vote_count = models.PositiveIntegerField(default=1)
    previous_hash = models.CharField(max_length=64)
    entry_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp_payload = models.CharField(max_length=40)
    tx_hash = models.CharField(max_length=100, blank=True)
    @staticmethod
    def digest(index, election_id, count, previous_hash, created_at):
        payload=json.dumps({'index':index,'election_id':election_id,'count':count,'previous_hash':previous_hash,'created_at':created_at},sort_keys=True,separators=(',',':'))
        return hashlib.sha256(payload.encode()).hexdigest()
