import pytest
import os
from bannotator.data import Annotation
import numpy as np

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
    for _,stream in large_annotation.get_streams().items():
        assert verify_epochs(stream.get_epochs(), True)
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
    original_behav = [b.name for b in large_annotation.get_behaviors()[0]]
    assert "dig" in original_behav
    # Get dig epoch list
    vect_before_rmv = np.ones((large_annotation.get_length(),large_annotation.num_stream()))
    i = 0
    for _, stream in large_annotation.get_streams().items():
        epochs = stream.get_behavior_dict()["dig"].get_epochs()
        digID = stream.get_behavior_dict()["dig"].ID
        otherID = stream.get_behavior_dict()["other"].ID
        vect_before_rmv[:,i] = stream.get_stream_vect()
        i+=1
        for epoch in epochs:
            assert epoch.name == "dig"
            assert epoch.get_behavior() is stream.get_behavior_dict()["dig"]
    large_annotation.delete_behavior("dig", "other")
    behaviors = large_annotation.get_behaviors()
    # Test if the target behavior is removed
    for bs in behaviors:
        new_behav= [b.name for b in bs]
        assert "dig" not in new_behav
        assert len(original_behav) - len(new_behav) == 1
    # Verify the epochs of dig are merged into others
    vect_after_rmv = np.ones((large_annotation.get_length(),large_annotation.num_stream()))
    i = 0
    for _,stream in large_annotation.get_streams().items():
        other = stream.get_behavior_dict()["other"]
        # Test if there is no faulty epochs in other
        assert verify_epochs(other.get_epochs(), False)
        assert verify_epochs(stream.get_epochs(), True)
        vect_after_rmv[:,i] = stream.get_stream_vect()
        i+=1
    # Test if indices of dig OR other before removal is the same with indices of other after remvoval
    for i in range(large_annotation.num_stream()):
        before_rmv = vect_before_rmv[:,i]
        after_rmv = vect_after_rmv[:,i]
        bf_idcs = np.argwhere(np.isin(before_rmv, (digID, otherID)))
        aft_idcs = np.argwhere(after_rmv == otherID)
        assert np.setdiff1d(bf_idcs, aft_idcs).size == 0 and np.setdiff1d(aft_idcs, bf_idcs).size == 0
            
def test_add_stream(small_annotation):
    new_stream = small_annotation.add_stream("other")
    assert small_annotation.num_stream() == 4
    assert len(new_stream.get_epochs()) == 1
    epoch = new_stream.get_epochs()[0]
    assert epoch.name == "other"
        
def verify_epochs(epochs, continuous = False):
    epochs.sort(reverse=False)
    if continuous and epochs[0].start != 1:
        return False
    for i in range(len(epochs)-1):
        if epochs[i].end >= epochs[i+1].start:
            return False
        if not continuous:
            # Verify epochs of a Behavior
            # No adjacent epochs with same behavior
            if epochs[i+1].start - epochs[i].end == 1:
                return False
        if continuous:
            # Verify epochs of a Stream
            # Must have no blanks and no adjacent epochs with same Behavior
            if epochs[i+1].name == epochs[i].name:
                return False
            if epochs[i+1].start - epochs[i].end != 1:
                return False
    return True

def verify_behaviors(annotation):
    blist = []
    for _,stream in annotation.get_streams().items():
        blist.append([b.name for b in stream.get_behavior_list()])