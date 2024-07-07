# repository-mongodb

repository-mongodb is a small library that simplifies MongoDB usage by providing a base repository pattern implementation. It offers automatic collection management and easy-to-use CRUD operations for MongoDB models.

## Features

- Base repository pattern for common MongoDB operations
- Automatic collection management based on model definitions
- Support for custom repository methods
- Metaclass-based approach for setting the `model` attribute automatically
- Configuration using environment variables
- Lazy creation of MongoDB client and database connections

## Installation

You can install repository-mongodb using pip:

```bash
pip install repository-mongodb
```

## Usage

### Environment Setup

Before using the library, set up the following environment variables:

```bash
export MONGO_HOST=your_host
export MONGO_PORT=your_port
export MONGO_USERNAME=your_username
export MONGO_PASSWORD=your_password
export MONGO_DATABASE=your_database_name
```

### Example Usage

Here's an example demonstrating how to use the repository-mongodb library:

```python
from dataclasses import dataclass
from typing import List
from repository_mongodb import BaseModel, BaseRepository

@dataclass
class UserModel(BaseModel):
    username: str
    email: str
    __collection_name__ = "users"

@dataclass
class PostModel(BaseModel):
    title: str
    content: str
    user_id: str
    __collection_name__ = "posts"

class UserRepository(BaseRepository[UserModel]):
    def find_by_username(self, username: str) -> UserModel:
        return self.collection.find_one({"username": username})

class PostRepository(BaseRepository[PostModel]):
    def find_by_user_id(self, user_id: str) -> List[PostModel]:
        return [PostModel(**post) for post in self.collection.find({"user_id": user_id})]

# Usage
user_repo = UserRepository()
post_repo = PostRepository()

# Create user
user = UserModel(username="john_doe", email="john@example.com")
created_user = user_repo.create(user)
print(f"Created user: {created_user.username}")

# Create posts for the user
post1 = PostModel(title="First Post", content="Hello, world!", user_id=str(created_user._id))
post2 = PostModel(title="Second Post", content="This is my second post.", user_id=str(created_user._id))
post_repo.create(post1)
post_repo.create(post2)

# Find user by username
found_user = user_repo.find_by_username("john_doe")
print(f"Found user: {found_user.username}, {found_user.email}")

# Find posts by user ID
user_posts = post_repo.find_by_user_id(str(created_user._id))
print(f"User posts: {len(user_posts)} posts")
```

This example demonstrates:

1. Defining MongoDB models (`UserModel` and `PostModel`) using the `BaseModel` class.
2. Specifying the collection name using the `__collection_name__` attribute in the models.
3. Creating custom repositories (`UserRepository` and `PostRepository`) by inheriting from the `BaseRepository` class.
4. Using the repository methods for creating and querying data.
5. Automatic collection management based on the `__collection_name__` attribute defined in the models.

## Running Tests

To run the tests for repository-mongodb, use the following command:

```bash
pytest /path/to/repository-mongodb/tests
```

Make sure you have pytest installed in your Python environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
