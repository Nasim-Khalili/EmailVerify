from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def save_otp_to_elasticsearch(email, otp_code):
    doc = {
        "email": email,
        "otp_code": otp_code
    }
    es.index(index="otp_logs", body=doc)
