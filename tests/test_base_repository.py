import pytest
from repository_mongodb.base_repository import BaseRepository
from repository_mongodb.base_model import BaseModel

class TestModel(BaseModel):
    __collection_name__ = "test_collection"

class TestRepository(BaseRepository[TestModel]):
    pass

@pytest.fixture
def repository():
    return TestRepository()

def test_create(repository):
    obj = TestModel()
    created_obj = repository.create(obj)
    assert created_obj._id is not None

def test_find_by_id(repository):
    obj = TestModel()
    created_obj = repository.create(obj)
    found_obj = repository.find_by_id(created_obj._id)
    assert found_obj._id == created_obj._id


def test_find_all(repository):
    obj1 = TestModel()
    obj2 = TestModel()
    repository.create(obj1)
    repository.create(obj2)
    all_objs = repository.find_all()
    assert len(all_objs) == 2

def test_update(repository):
    obj = TestModel()
    created_obj = repository.create(obj)
    created_obj.field = "updated"
    updated_obj = repository.update(created_obj)
    assert updated_obj.field == "updated"

def test_delete(repository):
    obj = TestModel()
    created_obj = repository.create(obj)
    repository.delete(created_obj)
    deleted_obj = repository.find_by_id(created_obj._id)
    assert deleted_obj is None