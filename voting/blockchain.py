"""Tamper-evident local hash chain + optional Ethereum contract adapter."""
import os
from django.utils import timezone
from .models import LedgerEntry

def append_vote_anchor(election_id):
    last=LedgerEntry.objects.order_by('-index').first()
    index=(last.index+1) if last else 1
    previous=last.entry_hash if last else '0'*64
    created=timezone.now().isoformat()
    digest=LedgerEntry.digest(index,election_id,1,previous,created)
    entry=LedgerEntry.objects.create(index=index,election_id_ref=election_id,vote_count=1,previous_hash=previous,entry_hash=digest,timestamp_payload=created)
    # On-chain submission is optional; the local app remains runnable without a node.
    uri=os.getenv('WEB3_PROVIDER_URI'); address=os.getenv('VOTING_CONTRACT_ADDRESS'); sender=os.getenv('WEB3_FROM_ADDRESS')
    if uri and address and sender:
        try:
            from web3 import Web3
            w3=Web3(Web3.HTTPProvider(uri, request_kwargs={'timeout':3}))
            abi=[{'inputs':[{'internalType':'bytes32','name':'receiptHash','type':'bytes32'},{'internalType':'uint256','name':'electionId','type':'uint256'}],'name':'anchorReceipt','outputs':[],'stateMutability':'nonpayable','type':'function'}]
            contract=w3.eth.contract(address=Web3.to_checksum_address(address),abi=abi)
            tx=contract.functions.anchorReceipt(bytes.fromhex(digest),election_id).transact({'from':Web3.to_checksum_address(sender)})
            receipt=w3.eth.wait_for_transaction_receipt(tx,timeout=30)
            if receipt.status == 1:
                entry.tx_hash=tx.hex(); entry.save(update_fields=['tx_hash'])
        except Exception:
            # Local ledger remains available if the optional chain is offline or misconfigured.
            pass
    return entry

def verify_chain():
    previous='0'*64
    for expected,entry in enumerate(LedgerEntry.objects.order_by('index'),start=1):
        if entry.index != expected or entry.previous_hash != previous: return False
        expected_hash=LedgerEntry.digest(entry.index,entry.election_id_ref,entry.vote_count,entry.previous_hash,entry.timestamp_payload)
        if expected_hash != entry.entry_hash: return False
        previous=entry.entry_hash
    return True
