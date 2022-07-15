from kink import inject

from repositories.account import AccountRepository
class AccountService:
    @inject(account_repository=AccountRepository)
    def __init__(self,account_repository):
        self.account_repository:AccountRepository =account_repository
        print("OK")
    def __call__(self, *args, **kwargs):
        print(args)
