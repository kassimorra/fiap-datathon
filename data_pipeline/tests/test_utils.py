import pytest
from unittest.mock import MagicMock, patch
from utils._utils import print_status, load_all

class ProcessMock:
    def run(self):
        pass

@pytest.fixture
def process_classes():
    # Return a list of mock process classes
    return [ProcessMock, ProcessMock]

@patch.object(ProcessMock, 'run')
def test_load_all(mock_run, process_classes):
    # Call the load_all function with mock classes
    load_all(*process_classes)

    # Check that run was called for each ProcessClass
    assert mock_run.call_count == 2  # Two mock classes, so run should be called twice

def test_print_status(capfd):
    # Call the print_status function
    print_status("Test Status")

    # Capture the output
    captured = capfd.readouterr()

    # Assert that the printed output is as expected
    assert captured.out == "\n--- Test Status ---\n"
