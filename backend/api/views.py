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