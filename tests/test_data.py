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
    
def test_delete_stream(small_annotation):
    old_id = [s.ID for _,s in small_annotation.get_streams().items()]
    small_annotation.delete_stream(2)
    new_id = [s.ID for _,s in small_annotation.get_streams().items()]
    assert 2 in old_id
    assert 2 not in new_id
    assert len(old_id) - len(new_id) == 1
    
    
def test_edit_behavior(small_annotation):
    streams = small_annotation.get_streams()
    # Change a middle frame of 'other' epoch to attack
    # The rest of this epoch should form a new epoch, positioned 3rd in the list
    epochs_1 = streams[1].get_epochs()
    assert len(epochs_1) == 3
    streams[1].set_behavior(400,"a")
    assert len(epochs_1) == 4
    assert verify_epochs(epochs_1, True)
    assert epochs_1[2].name == "attack"
    assert epochs_1[2].start == 401
    assert epochs_1[2].end == 589
    assert epochs_1[1].end == 400
    # Change a middle frame of an epoch and causing automatic merging with the next epoch
    # There should not be any new epochs
    epochs_2 = streams[2].get_epochs()
    assert len(epochs_2) == 4
    streams[2].set_behavior(453, "o")
    assert len(epochs_2) == 4
    assert epochs_2[3].start == 454
    assert epochs_2[3].end == 598
    assert epochs_2[3].name == "other"
    assert epochs_2[2].end == 453
    assert epochs_2[2].name == "general-sniffing"
    assert verify_epochs(epochs_2,True)
    # Change behavior at the beginning of an epoch and not causing any merge
    epochs_3 = streams[3].get_epochs()
    assert len(epochs_3) == 3
    streams[3].set_behavior(0, "c")
    assert epochs_3[0].name == "climb"
    assert epochs_3[0].start == 1
    assert epochs_3[0].end == 375
    assert verify_epochs(epochs_3, True)
    # Change behavior at the first frame of an epoch and causing merge on both sides
    streams[2].set_behavior(448,"o")
    assert len(epochs_2) == 2
    assert epochs_2[1].name == "other"
    assert epochs_2[1].start == 306
    assert epochs_2[1].end == 598
    assert verify_epochs(epochs_2, True)
        
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