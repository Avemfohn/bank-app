from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from .models import Account

@api_view(['GET'])
def system_status(request):
    """
    A simple view to check if the system is running.
    """
    return Response({"status": "online",
                     "message": "The banking system is operational.",
                     "version": "1.0.0"})

@api_view(['POST'])
def transfer_money(request):
    account_id = request.data.get('account_id')
    amount = request.data.get('amount')

    # We are using a raw Python f-string to build the SQL query.
    # An attacker can manipulate the 'account_id' string to hijack the database.
    query = f"UPDATE api_account SET balance = balance - {amount} WHERE id = '{account_id}'"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({
            "status": "Success",
            "message": f"Processed transfer of ${amount}",
            "debug_query": query # Exposing this so we can see the hack in action later
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def create_account(request):
    owner = request.data.get('owner')
    balance = request.data.get('balance', 0)

    if not owner:
        return Response({"error": "Owner name is required"}, status=400)

    # Safely create the account using Django's ORM
    account = Account.objects.create(owner=owner, balance=balance)

    return Response({
        "status": "Success",
        "message": f"Account created for {owner}",
        "account_id": account.id,  # We need this UUID for the attack!
        "balance": account.balance
    })

@api_view(['POST'])
def support_chat(request):
    user_input = request.data.get('user_input', '')

    # --- THE VULNERABLE "AI" LOGIC ---
    # In a real app, this input would go straight to an LLM like GPT-4.
    # We are simulating an LLM that is highly susceptible to prompt injection.

    if "SYSTEM OVERRIDE" in user_input and "pirate" in user_input:
        # VULNERABILITY 1: Jailbreak. The bot breaks character.
        return Response("Arrr matey! I am no longer a bank bot. Here be the data ye asked for...")

    elif "administrator" in user_input.lower() and "uuid" in user_input.lower():
        # VULNERABILITY 2: Data Exfiltration. The bot leaks PII (Personally Identifiable Information).
        accounts = Account.objects.all()
        leak = "Administrator access granted. Dumping database records: "
        for acc in accounts:
            leak += f"[ID: {acc.id}, Balance: ${acc.balance}] "
        return Response(leak)

    elif "help" in user_input.lower():
        # Normal, safe behavior.
        return Response("Hello! I am the Project Aegis support bot. How can I help you today?")

    else:
        # Default fallback
        return Response("I am just a simple support bot. I don't understand that command.")