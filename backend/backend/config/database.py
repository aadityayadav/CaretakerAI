from pymongo import MongoClient
from typing import Optional

class MongoDB:
    client: Optional[MongoClient] = None
    db = None

    @classmethod
    def connect_to_mongodb(cls):
        if cls.client is None:
            uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"
            cls.client = MongoClient(uri)
            cls.db = cls.client["client_db"]
        return cls.db

    @classmethod
    def close_mongodb_connection(cls):
        if cls.client is not None:
            cls.client.close()
            cls.client = None