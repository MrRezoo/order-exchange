from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import Wallet
from django.contrib.auth.models import User
from transactions.models.transaction import Transaction
from decimal import Decimal

class TransactionE2ETestCase(APITestCase):

    def setUp(self):
        # Create test user, wallet, and a few transactions
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.wallet = Wallet.objects.create(user=self.user, balance=Decimal('100.00'))
        self.transaction1 = Transaction.objects.create(wallet=self.wallet, amount=Decimal('10.00'), type='DEPOSIT')
        self.transaction2 = Transaction.objects.create(wallet=self.wallet, amount=Decimal('50.00'), type='WITHDRAWAL')
        self.client.login(username='testuser', password='12345')

    def test_list_transactions(self):
        # Test the listing of all transactions
        url = reverse('api-v1:transactions:transaction-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We created 2 transactions

    def test_view_single_transaction(self):
        # Test fetching a single transaction by ID
        url = reverse('api-v1:transactions:transaction-detail', args=[self.transaction1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '10.00')
        self.assertEqual(response.data['type'], 'DEPOSIT')