from django.contrib import admin
from .models import VoterProfile,Election,Candidate,Vote,LedgerEntry
@admin.register(VoterProfile)
class VoterProfileAdmin(admin.ModelAdmin): list_display=('user','voter_id','approved','otp_verified'); list_editable=('approved','otp_verified'); search_fields=('user__username','voter_id')
class CandidateInline(admin.TabularInline): model=Candidate; extra=1
@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin): list_display=('title','starts_at','ends_at','is_published'); list_editable=('is_published',); inlines=[CandidateInline]
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin): list_display=('election','candidate','voter','cast_at'); readonly_fields=('election','candidate','voter','cast_at')
@admin.register(LedgerEntry)
class LedgerAdmin(admin.ModelAdmin): list_display=('index','election_id_ref','entry_hash','created_at'); readonly_fields=('index','election_id_ref','vote_count','previous_hash','entry_hash','created_at','timestamp_payload','tx_hash')
