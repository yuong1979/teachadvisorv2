from django.dispatch import Signal

notify = Signal(providing_args=['sender', 'recipient', 'action', 'message'])