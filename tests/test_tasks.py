# tests/test_tasks.py
from unittest.mock import patch
from accounts.tasks import send_otp_email

@patch("accounts.tasks.send_mail")
def test_send_otp_email_task(mock_send_mail):
    
    test_email = "nasim@example.com"
    test_otp = "123456"

    send_otp_email(test_email, test_otp)
    
    mock_send_mail.assert_called_once_with(
        "کد تایید شما",
        f"کد تایید شما: {test_otp}",
        "your_email@gmail.com",
        [test_email]
    )
