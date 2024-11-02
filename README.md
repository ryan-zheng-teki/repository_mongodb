# Repository MongoDB

A robust MongoDB repository pattern implementation featuring automated transaction management, type-safe operations, and comprehensive replica set support.

## Features

- **Type-Safe Repository Pattern**: Generic repository implementation with strong typing support
- **Automated Transaction Management**: Declarative transaction handling using metaclasses
- **Replica Set Support**: Built-in support for MongoDB replica sets with automated setup
- **Robust Error Handling**: Comprehensive error handling and logging throughout the stack
- **Clean Architecture**: Follows SOLID principles and clean architecture patterns

## Prerequisites

- Docker and Docker Compose
- Python 3.10 or higher
- pip (Python package manager)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/repository_mongodb.git
cd repository_mongodb
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup MongoDB Replica Set:
```bash
chmod +x deployment/scripts/setup-mongodb.sh
sudo ./deployment/scripts/setup-mongodb.sh
```

## Project Structure

```
repository_mongodb/
├── repository_mongodb/
│   ├── base_model.py          # Base model with MongoDB integration
│   ├── base_repository.py     # Generic repository implementation
│   ├── mongo_client.py        # MongoDB client configuration
│   ├── mongo_config.py        # MongoDB connection settings
│   ├── transaction_management.py  # Transaction context managers
│   └── transaction_metaclass.py   # Automated transaction handling
├── deployment/
│   ├── docker/
│   │   ├── docker-compose.yml    # MongoDB replica set configuration
│   │   └── mongodb/              # MongoDB data directory
│   └── scripts/
│       └── setup-mongodb.sh      # Automated setup script
├── tests/
│   ├── test_base_repository.py   # Repository tests
│   └── conftest.py              # Pytest fixtures
└── README.md
```

## Architecture

### Repository Pattern

The implementation uses a generic repository pattern with built-in transaction support:

```python
class MyRepository(BaseRepository[MyModel]):
    def find_by_name(self, name: str) -> Optional[MyModel]:
        return self.find_by_attributes({"name": name})
```

### Transaction Management

Transactions are automatically handled using metaclasses:

```python
@transactional
def transfer_funds(from_account: Account, to_account: Account, amount: float):
    from_account.balance -= amount
    to_account.balance += amount
    account_repo.update(from_account)
    account_repo.update(to_account)
```

### MongoDB Configuration

The system supports flexible MongoDB configuration through environment variables:

- `MONGO_HOST`: MongoDB host (default: localhost)
- `MONGO_PORT`: MongoDB port (default: 27017)
- `MONGO_DATABASE`: Database name (default: test_database)
- `MONGO_REPLICA_SET`: Replica set name (default: rs0)

## Development

### Running Tests

```bash
pytest tests/
```

### MongoDB Management

Start MongoDB cluster:
```bash
cd deployment/docker
docker-compose up -d
```

Stop MongoDB cluster:
```bash
cd deployment/docker
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

## Error Handling

The implementation includes comprehensive error handling:

- Connection failures
- Transaction conflicts
- Replica set issues
- Network timeouts

All errors are properly logged with detailed information for debugging.

## Best Practices

1. Always use the repository pattern for database operations
2. Let the transaction decorator handle transaction management
3. Use type hints for better code safety
4. Follow the provided error handling patterns
5. Use the logging system for debugging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License

## Support

For issues and feature requests, please use the GitHub issue tracker.