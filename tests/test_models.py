import pytest
from django.contrib.auth import get_user_model
from accounts.models import EmailOTP, Post

User = get_user_model()

@pytest.mark.django_db
def test_email_otp_model_creation():
    user = User.objects.create_user(username="nasim", email="nasim@example.com", password="testpass123")
    otp = EmailOTP.objects.create(user=user, otp_code="123456")

    assert otp.user == user
    assert otp.otp_code == "123456"
    assert str(otp) == "nasim@example.com - 123456"


@pytest.mark.django_db
def test_post_model_creation():
    user = User.objects.create_user(username="hasti", email="hasti@example.com", password="hastipass")
    post = Post.objects.create(owner=user, title="اولین پست", content="سلام! این محتوای پست منه.")

    assert post.owner == user
    assert post.title == "اولین پست"
    assert post.content.startswith("سلام")
    assert post.created_at is not None