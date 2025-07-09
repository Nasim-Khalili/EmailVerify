from elasticsearch import Elasticsearch
from django.utils import timezone

es = Elasticsearch("http://localhost:9200")

def save_otp_to_elasticsearch(email, otp_code):
    doc = {
        "email": email,
        "otp_code": otp_code
    }
    es.index(index="otp_logs", body=doc)
    

def log_post_action(user, post, action):
    doc = {
        "user_id": user.id if user.is_authenticated else None,
        "username": user.username if user.is_authenticated else "Anonymous",
        "post_id": post.id,
        "post_title": post.title,
        "action": action,
        "timestamp": timezone.now().isoformat()
    }
    es.index(index="post_logs", body=doc)
