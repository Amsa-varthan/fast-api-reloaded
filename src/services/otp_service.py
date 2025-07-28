import random

def generate_otp(length: int = 6) -> str:
    """
    Generates a random OTP of a specified length.
    """
    return "".join([str(random.randint(0, 9)) for _ in range(length)])
