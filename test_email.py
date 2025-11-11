"""
Quick test script to verify SMTP email configuration.
Run this after setting up your .env file to test email sending.

Usage:
    python test_email.py your-email@example.com
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import after loading .env
from app import send_email

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_email.py your-email@example.com")
        sys.exit(1)
    
    recipient = sys.argv[1]
    
    print(f"Testing email send to: {recipient}")
    print(f"SMTP Host: {os.environ.get('SMTP_HOST', 'NOT SET')}")
    print(f"SMTP User: {os.environ.get('SMTP_USER', 'NOT SET')}")
    print(f"SMTP From: {os.environ.get('SMTP_FROM', 'NOT SET')}")
    print("-" * 50)
    
    # Try sending test email
    success = send_email(
        subject="CannaSpot Email Test",
        to=recipient,
        text_body="This is a test email from CannaSpot.\n\nIf you received this, your SMTP configuration is working correctly!",
        html_body="""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #4CAF50;">✅ Email Test Successful!</h1>
            <p>This is a test email from CannaSpot.</p>
            <p>If you received this, your SMTP configuration is working correctly!</p>
            <hr>
            <p style="color: #888; font-size: 12px;">
                Sent from CannaSpot v3.6<br>
                Email System Test
            </p>
        </body>
        </html>
        """
    )
    
    if success:
        print("\n✅ Email sent successfully!")
        print(f"Check {recipient} for the test email.")
        print("If you don't see it, check your spam folder.")
    else:
        print("\n❌ Email failed to send.")
        print("Check the error messages above.")
        print("\nCommon issues:")
        print("- SMTP credentials not set in .env file")
        print("- Wrong password (Gmail needs App Password, not regular password)")
        print("- Firewall blocking port 587")
        print("- 2-Factor Authentication not enabled (required for Gmail)")

if __name__ == "__main__":
    main()
