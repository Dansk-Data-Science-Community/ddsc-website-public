from django.core.signing import Signer


def sign_ticket_data(ticket_data: dict):
    signer = Signer()
    return signer.sign_object(ticket_data)


def unsign_ticket_data(ticket_data: dict):
    signer = Signer()
    return signer.unsign_object(ticket_data)
