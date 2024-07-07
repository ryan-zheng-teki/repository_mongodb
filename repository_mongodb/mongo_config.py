import os

class MongoConfig:
    def __init__(self):
        self.host = os.environ.get('MONGO_HOST', 'localhost')
        self.port = int(os.environ.get('MONGO_PORT', '27017'))
        self.username = os.environ.get('MONGO_USERNAME', '')
        self.password = os.environ.get('MONGO_PASSWORD', '')
        self.database = os.environ.get('MONGO_DATABASE', 'autobyteus')

    def get_connection_uri(self):
        if self.username and self.password:
            return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            return f"mongodb://{self.host}:{self.port}/{self.database}"