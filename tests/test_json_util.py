from pathlib import Path
import pytest
from dp_json_util import JsonSchemaRetriever, UnsetJsonLocationException, \
    InvalidJsonLocationDirPathException


@pytest.fixture(scope="module")
def test_data_path():
    return Path(__file__).parent.joinpath("testdata")


@pytest.fixture(scope="module")
def json_retriever():
    from dp_json_util import JsonRetriever
    json_retriever = JsonRetriever()
    return json_retriever

@pytest.mark.parametrize(
    "given_schema_name", ([
        "test",
        "test_schema",
        "test.json",
        "test_schema.json"
    ])
)
def test_safe_schema_name(given_schema_name):
    assert JsonSchemaRetriever._safe_schema_name(given_schema_name) == "test_schema.json"

def test_json_retriever_raises_unset_path_exception(json_retriever):
    with pytest.raises(UnsetJsonLocationException):
        json_retriever.load_json("some.json")


@pytest.mark.parametrize(
    "invalid_dir", ([
        Path(__file__),
        "somestring"
    ])
)
def test_json_retriever_raises_invalid_path_dir_exeception(invalid_dir, json_retriever):
    with pytest.raises(InvalidJsonLocationDirPathException):
        json_retriever.set_json_location_dir(invalid_dir)

def test_json_retriever_can_load_json_data_given_valid_path(json_retriever, test_data_path):
    json_retriever.set_json_location_dir(test_data_path)
    data = json_retriever.load_json("valid.json")
    assert data["overall_level"] == 12
