import pytest

from tracker import Tracker, NoSilentTracker, SilentTracker
from tracker.exceptions import InvalidOperation


class TestTracker:
    @pytest.fixture
    def tracker(self):
        return Tracker()

    def test_allocate_server(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("ui") == "ui1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("ui") == "ui2"

    def test_allocate_and_deallocate(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api4"
        tracker.deallocate("api3")
        tracker.deallocate("api2")
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api5"

    def test_deallocate_not_allocated_server(self, tracker):
        with pytest.raises(InvalidOperation):
            tracker.deallocate("notexists1000")


class TestNoSilentTracker:
    @pytest.fixture
    def tracker(self):
        return NoSilentTracker()

    def test_allocate_server(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("ui") == "ui1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("ui") == "ui2"

    def test_allocate_and_deallocate(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api4"
        assert tracker.deallocate("api3") is None
        assert tracker.deallocate("api2") is None
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api5"

    def test_deallocate_not_allocated_server(self, tracker):
        assert tracker.deallocate("notexists1000") == "Invalid operation."


class TestSilentTracker:
    @pytest.fixture
    def tracker(self):
        return SilentTracker()

    def test_allocate_server(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("ui") == "ui1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("ui") == "ui2"

    def test_allocate_and_deallocate(self, tracker):
        assert tracker.allocate("api") == "api1"
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api4"
        assert tracker.deallocate("api3") is None
        assert tracker.deallocate("api2") is None
        assert tracker.allocate("api") == "api2"
        assert tracker.allocate("api") == "api3"
        assert tracker.allocate("api") == "api5"

    def test_deallocate_not_allocated_server(self, tracker):
        assert tracker.deallocate("notexists1000") is None
