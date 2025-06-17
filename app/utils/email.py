# app/utils/email.py
from pydantic import EmailStr

async def send_email(recipient: EmailStr, subject: str, body: str) -> None:
    print("\n=== EMAIL SENT ===")
    print(f"To     : {recipient}")
    print(f"Subject: {subject}")
    print("Body   :")
    print(body)
    print("=================\n")
