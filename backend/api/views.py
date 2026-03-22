from django.forms import ValidationError
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

    try:
        # The ORM automatically sanitizes the input, blocking SQLi
        account = Account.objects.get(id=account_id)

        # F() expression handles the math safely at the database level
        account.balance = F('balance') - amount
        account.save()

        account.refresh_from_db()

        return Response({
            "status": "Success",
            "message": "Secure transfer processed.",
            "new_balance": account.balance
        })

    except Account.DoesNotExist:
        return Response({"error": "Account not found."}, status=404)
    except ValidationError:
        return Response({"error": "Invalid Account ID format."}, status=403)
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