from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

# for signals working
    def ready(self):
        import accounts.signals