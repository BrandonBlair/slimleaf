from uuid import uuid1


def unique_email():
    """Generates a unique email address"""
    email = f"unique_email_{uuid1()}@doesnotexist.com"
    return email
