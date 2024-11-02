import pytest
from repository_mongodb.base_repository import BaseRepository
from repository_mongodb.base_model import BaseModel
from repository_mongodb.transaction_management import transaction

class TestModel(BaseModel):
    __collection_name__ = "test_collection"
    name: str
    age: int
    email: str

class TestRepository(BaseRepository[TestModel]):
    pass

@pytest.fixture(autouse=True, scope="function")
def cleanup_collection(mongo_database):
    yield 
    mongo_database[TestModel.__collection_name__].drop()

@pytest.fixture
def repository():
    return TestRepository()

def test_create(repository):
    obj = TestModel(name="John Doe", age=25, email="john@example.com")
    created_obj = repository.create(obj)
    assert created_obj._id is not None
    assert created_obj.name == "John Doe"
    assert created_obj.age == 25
    assert created_obj.email == "john@example.com"

def test_find_by_id(repository):
    obj = TestModel(name="Jane Smith", age=30, email="jane@example.com")
    created_obj = repository.create(obj)
    found_obj = repository.find_by_id(created_obj._id)
    assert found_obj._id == created_obj._id
    assert found_obj.name == "Jane Smith"
    assert found_obj.age == 30
    assert found_obj.email == "jane@example.com"

def test_find_all(repository):
    obj1 = TestModel(name="Alice", age=35, email="alice@example.com")
    obj2 = TestModel(name="Bob", age=40, email="bob@example.com")
    repository.create(obj1)
    repository.create(obj2)
    all_objs = repository.find_all()
    assert len(all_objs) == 2
    assert {obj.name for obj in all_objs} == {"Alice", "Bob"}
    assert {obj.age for obj in all_objs} == {35, 40}
    assert {obj.email for obj in all_objs} == {"alice@example.com", "bob@example.com"}

def test_find_by_single_attribute(repository):
    obj1 = TestModel(name="Alice", age=35, email="alice@example.com")
    obj2 = TestModel(name="Bob", age=40, email="bob@example.com")
    repository.create(obj1)
    repository.create(obj2)
    found_objs = repository.find_by_attributes({"name": "Alice"})
    assert len(found_objs) == 1
    assert found_objs[0].name == "Alice"
    assert found_objs[0].age == 35
    assert found_objs[0].email == "alice@example.com"

def test_find_by_multiple_attributes(repository):
    obj1 = TestModel(name="Alice", age=35, email="alice@example.com")
    obj2 = TestModel(name="Bob", age=40, email="bob@example.com")
    repository.create(obj1)
    repository.create(obj2)
    found_objs = repository.find_by_attributes({"name": "Bob", "age": 40})
    assert len(found_objs) == 1
    assert found_objs[0].name == "Bob"
    assert found_objs[0].age == 40
    assert found_objs[0].email == "bob@example.com"

def test_find_by_attributes_no_match(repository):
    obj1 = TestModel(name="Alice", age=35, email="alice@example.com")
    obj2 = TestModel(name="Bob", age=40, email="bob@example.com")
    repository.create(obj1)
    repository.create(obj2)
    found_objs = repository.find_by_attributes({"name": "Charlie"})
    assert len(found_objs) == 0

def test_update(repository):
    obj = TestModel(name="Charlie", age=45, email="charlie@example.com")
    created_obj = repository.create(obj)
    created_obj.name = "Updated Charlie"
    created_obj.age = 50
    created_obj.email = "updated_charlie@example.com"
    updated_obj = repository.update(created_obj)
    assert updated_obj.name == "Updated Charlie"
    assert updated_obj.age == 50
    assert updated_obj.email == "updated_charlie@example.com"

def test_delete(repository):
    obj = TestModel(name="David", age=55, email="david@example.com")
    created_obj = repository.create(obj)
    repository.delete(created_obj)
    deleted_obj = repository.find_by_id(created_obj._id)
    assert deleted_obj is None

def test_update_transaction_commit(repository):
    obj = TestModel(name="Eve", age=28, email="eve@example.com")
    created_obj = repository.create(obj)
    with transaction() as session:
        created_obj.name = "Eve Updated"
        repository.update(created_obj, session=session)
    found_obj = repository.find_by_id(created_obj._id)
    assert found_obj.name == "Eve Updated"

def test_update_transaction_rollback(repository):
    obj = TestModel(name="Frank", age=32, email="frank@example.com")
    created_obj = repository.create(obj)
    try:
        with transaction() as session:
            created_obj.name = "Frank Updated"
            repository.update(created_obj, session=session)
            raise Exception("Simulated failure")
    except:
        pass
    found_obj = repository.find_by_id(created_obj._id)
    assert found_obj.name == "Frank"  # Update should have been rolled back