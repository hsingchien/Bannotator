import pytest
import os
from bannotator.data import Annotation

TEST_ANNOTATION_FILE_LARGE = os.path.join("tests", "annotation", "annotation.txt")
TEST_ANNOTATION_FILE_SMALL = os.path.join("tests", "annotation", "annotation_small.txt")
TEST_CONFIG_FILE = os.path.join("tests", "annotation", "config.txt")
TEST_ANNOTATION_FILE_ERROR = os.path.join(
    "tests", "annotation", "annotation_small_err.txt"
)


@pytest.fixture
def large_annotation():
    annot = Annotation({})
    annot.read_from_file(txt_path=TEST_ANNOTATION_FILE_LARGE)
    return annot


@pytest.fixture
def small_annotation():
    annot = Annotation({})
    annot.read_from_file(txt_path=TEST_ANNOTATION_FILE_SMALL)
    return annot


@pytest.fixture
def config_file():
    annot = Annotation({})
    annot.read_config_from_file(config_path=TEST_CONFIG_FILE)
    return annot


def test_annotation_load_from_txt(large_annotation, small_annotation, config_file):
    assert len(large_annotation.get_streams()) == 2
    assert len(config_file.get_streams()) == 2
    assert len(small_annotation.get_streams()) == 3
    assert large_annotation.get_stream(1).ID == 1
    assert large_annotation._validate_stream()
    with pytest.raises(Exception):
        annot = Annotation({})
        annot.read_from_file(txt_path=TEST_ANNOTATION_FILE_ERROR)

def test_add_behavior(small_annotation):
    original_behav = [b.name for b in small_annotation.get_behaviors()[0]]
    small_annotation.add_behavior("jump", "q")
    behaviors = small_annotation.get_behaviors()
    # Test jump-q is added into all streams
    for bs in behaviors:
        new_behav = [b.name for b in bs]
        new_key = [b.keybind for b in bs]
        assert len(new_behav)-len(original_behav) == 1
        assert "jump" in new_behav
        assert new_key[new_behav.index("jump")] == "q"
    after_adding_jump = [b.name for b in small_annotation.get_behaviors()[0]]
    # Test adding behavior denies name reuse
    small_annotation.add_behavior("jump","z")
    for bs in behaviors:
        new_behav = [b.name for b in bs]
        new_key = [b.keybind for b in bs]
        assert len(new_behav) == len(after_adding_jump)
        assert new_key[new_behav.index("jump")] == "q"
    # Test adding behavior denies keybind reuse
    small_annotation.add_behavior("fly","q")
    for bs in behaviors:
        new_behav = [b.name for b in bs]
        new_key = [b.keybind for b in bs]
        assert len(new_behav) == len(after_adding_jump)
        assert "fly" not in new_behav
        assert new_key[new_behav.index("jump")] == "q"

def test_delete_behavior(large_annotation):
    original_behav = [b.name for b in small_annotation.get_behaviors()[0]]
    assert "dig" in original_behav
    
    large_annotation.delete_behavior("dig", "other")
    behaviors = large_annotation.get_behaviors()
    # Test if the target behavior is removed
    for bs in behaviors:
        new_behav= [b.name for b in bs]
        assert "dig" not in new_behav
        assert len(original_behav) - len(new_behav) == 1
    # Verify the epochs of dig are merged into others
        
        