from api_clients.api_client import APIClient

class AccountsAPI(APIClient):
    """
    API client for accounts endpoints
    """
    
    def __init__(self, base_url=None, token=None):
        super().__init__(base_url, token)
    
    def get_accounts(self, params=None):
        """
        Get all accounts for the authenticated user
        
        :param params: Optional query parameters (e.g. status, type)
        :return: API response
        """
        return self.get('accounts', params=params)
    
    def get_account(self, account_id):
        """
        Get details for a specific account
        
        :param account_id: Account ID
        :return: API response
        """
        return self.get(f'accounts/{account_id}')
    
    def get_account_transactions(self, account_id, params=None):
        """
        Get transactions for a specific account
        
        :param account_id: Account ID
        :param params: Optional query parameters (e.g. fromDate, toDate, type)
        :return: API response
        """
        return self.get(f'accounts/{account_id}/transactions', params=params)
    
    def get_account_balance(self, account_id):
        """
        Get balance for a specific account
        
        :param account_id: Account ID
        :return: API response
        """
        return self.get(f'accounts/{account_id}/balance')
    
    def transfer_funds(self, from_account_id, to_account_id, amount, memo=None):
        """
        Transfer funds between accounts
        
        :param from_account_id: Source account ID
        :param to_account_id: Destination account ID
        :param amount: Amount to transfer
        :param memo: Optional memo
        :return: API response
        """
        payload = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": str(amount)
        }
        
        if memo:
            payload["memo"] = memo
        
        return self.post('transfers', json_data=payload)
    
    def external_transfer(self, from_account_id, recipient_data, amount, memo=None):
        """
        Transfer funds to an external account
        
        :param from_account_id: Source account ID
        :param recipient_data: Recipient data (account number, routing number, etc.)
        :param amount: Amount to transfer
        :param memo: Optional memo
        :return: API response
        """
        payload = {
            "fromAccountId": from_account_id,
            "recipientData": recipient_data,
            "amount": str(amount)
        }
        
        if memo:
            payload["memo"] = memo
        
        return self.post('external-transfers', json_data=payload)
    
    def get_account_statements(self, account_id, params=None):
        """
        Get statements for a specific account
        
        :param account_id: Account ID
        :param params: Optional query parameters (e.g. fromDate, toDate)
        :return: API response
        """
        return self.get(f'accounts/{account_id}/statements', params=params)
    
    def get_statement_pdf(self, statement_id):
        """
        Get PDF for a specific statement
        
        :param statement_id: Statement ID
        :return: API response with PDF content
        """
        return self.get(f'statements/{statement_id}/pdf')
