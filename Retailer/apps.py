from django.apps import AppConfig


class RetailerConfig(AppConfig):
    name = 'Retailer'
    def ready(self):
        import Retailer.mysignal
