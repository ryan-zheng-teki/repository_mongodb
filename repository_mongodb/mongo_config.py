import os
from typing import Optional

class MongoConfig:
    def __init__(self):
        # Just configure primary node
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = os.getenv('MONGO_PORT', '27017')
        self.database = os.getenv('MONGO_DATABASE', 'test_database')
        self.replica_set = os.getenv('MONGO_REPLICA_SET', 'rs0')

    def get_connection_uri(self) -> str:
        """
        Generate MongoDB connection URI that connects to primary node only.
        The MongoDB driver will handle replica set discovery.
        """
        uri = f"mongodb://{self.host}:{self.port}"
        
        # Only specify replica set name
        if self.replica_set:
            uri += f"/?replicaSet={self.replica_set}"
            
        return uri