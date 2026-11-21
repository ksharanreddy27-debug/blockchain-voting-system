# Decentralized Online Voting System Using Blockchain — Academic Demo

A runnable Django web application based on the uploaded project report's modules: voter registration/authentication, election and candidate management, voting, result display, and blockchain-inspired audit records. The report specifies Python, Django ORM, HTML/CSS/JavaScript and MySQL; this implementation uses Django with SQLite by default for easy Windows setup, and optional MySQL configuration.

## Requirements
- Windows 10/11
- Python 3.11 or newer
- Internet connection for first-time package installation

## Run on Windows (PowerShell)
1. Extract this ZIP to a folder such as `C:\Projects\blockchain_voting`.
2. Open PowerShell in that folder.
3. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If script activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell window, then activate again.

4. Install packages and create the local environment file:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

5. Create database tables and an admin account:

```powershell
python manage.py makemigrations voting
python manage.py migrate
python manage.py createsuperuser
```

6. Start the website:

```powershell
python manage.py runserver
```

7. Open **http://127.0.0.1:8000/** in your browser. Admin panel: **http://127.0.0.1:8000/admin/**.

## First demo walkthrough
1. Sign in to `/admin/` using the superuser account.
2. Create an Election with a start time in the past and end time in the future. Add at least two candidates inline and tick **is published**.
3. Register a normal voter at `/register/` with a demo voter ID.
4. In admin, open **Voter profiles** and approve that voter (tick `approved`).
5. Log in as that voter, open **Demo OTP**, and enter `123456`.
6. Return to Elections, open the election, select one candidate and submit.
7. Visit Results. For the admin audit ledger, visit `/ledger/` while signed in as staff.
8. Try to vote a second time: the application blocks it, and the database enforces a unique voter/election pair.

## Database
SQLite is enabled by default. To use MySQL, create a database and fill `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env`. On Windows, install a compatible MySQL client wheel before using the MySQL backend; otherwise use SQLite for the demo.

## Blockchain details
Every accepted vote creates a SHA-256 hash-linked audit entry in the local database. `contracts/VotingLedger.sol` is a Solidity contract that can anchor receipt hashes on a local Ethereum development chain. Set `WEB3_PROVIDER_URI`, `VOTING_CONTRACT_ADDRESS`, and `WEB3_FROM_ADDRESS` in `.env` after deploying it to a local chain with an unlocked test account. The Django app then attempts to submit the receipt hash and stores the transaction hash when successful. If the chain is offline or unconfigured, voting still works and the local ledger remains active. See `scripts/deploy_instructions.md`.

## Important security and scope limitations
- This is an educational prototype, not a production election platform.
- OTP is a visible fixed demo code (`123456`), not SMS delivery.
- Voter approval is manual; there is no Aadhaar, UIDAI, fingerprint or face-recognition integration.
- The demo database links a ballot choice to a voter account; it is not a privacy-preserving secret ballot.
- Local hash chaining is tamper-evident only if the database and application environment are protected; it is not a distributed consensus network.
- Do not use this application for real public, governmental, organizational or high-stakes elections.

## Project structure
- `voting/models.py` — voter, election, candidate, vote and ledger models
- `voting/views.py` — registration, login, demo OTP, voting, results
- `voting/admin.py` — administrator management
- `voting/blockchain.py` — local audit hash chain and Web3 adapter placeholder
- `contracts/VotingLedger.sol` — optional Ethereum receipt contract
- `voting/templates/` — user interface

## Troubleshooting
- `py` not found: install Python from python.org and select **Add Python to PATH**.
- Port busy: run `python manage.py runserver 8001` and open port 8001.
- Cannot log in to admin: rerun `python manage.py createsuperuser`.
- Vote button says not eligible: approve the profile in admin and complete demo OTP.
