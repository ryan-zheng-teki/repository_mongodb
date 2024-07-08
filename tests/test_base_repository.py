import pytest
from repository_mongodb.base_repository import BaseRepository
from repository_mongodb.base_model import BaseModel

class TestModel(BaseModel):
    __collection_name__ = "test_collection"
    name: str
    age: int
    email: str

class TestRepository(BaseRepository[TestModel]):
    pass

@pytest.fixture
def repository():
    return TestRepository()
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