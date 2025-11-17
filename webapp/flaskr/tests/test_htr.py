import pytest
import os
import sys

# Add the parent directory to the path so we can import from flaskr
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from handwriting_reader.paddle_hw_reader import PaddleHandwritingReader


@pytest.fixture
def paddle_reader():
    """Create a PaddleHandwritingReader instance for testing."""
    return PaddleHandwritingReader()


@pytest.fixture
def test_image_path():
    """Path to a test image that exists in the project."""
    # Using a relative path from the test file location
    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, "static/uploads/images/pow_whiteboard.jpg")


def test_paddle_reader_initialization(paddle_reader):
    """Test that PaddleHandwritingReader initializes correctly."""
    assert paddle_reader is not None
    assert hasattr(paddle_reader, "ocr")
    assert hasattr(paddle_reader, "read_text")


def test_read_text_returns_list(paddle_reader, test_image_path):
    """Test that read_text returns a list."""
    assert os.path.exists(test_image_path), f"Test image not found at {test_image_path}"

    results = paddle_reader.read_text(test_image_path)

    assert isinstance(results, list), "read_text should return a list"


def test_read_text_contains_results(paddle_reader, test_image_path):
    """Test that read_text returns non-empty results for an image with text."""
    assert os.path.exists(test_image_path), f"Test image not found at {test_image_path}"

    results = paddle_reader.read_text(test_image_path)

    assert len(results) > 0, (
        "read_text should return at least one result for an image with text"
    )


def test_read_text_output_structure(paddle_reader, test_image_path):
    """Test that read_text output has the expected structure with text content."""
    assert os.path.exists(test_image_path), f"Test image not found at {test_image_path}"

    results = paddle_reader.read_text(test_image_path)

    # Check that results is a list
    assert isinstance(results, list), "Results should be a list"

    # Check that the list is not empty for an image with text
    assert len(results) > 0, "Results should contain at least one item"

    # Each result should have methods we can use
    for result in results:
        assert hasattr(result, "print"), "Result should have a print method"
        assert hasattr(result, "save_to_img"), "Result should have a save_to_img method"
        assert hasattr(result, "save_to_json"), (
            "Result should have a save_to_json method"
        )


def test_read_text_with_nonexistent_file(paddle_reader):
    """Test that read_text handles nonexistent files appropriately."""
    nonexistent_path = "path/to/nonexistent/image.jpg"

    with pytest.raises(
        Exception
    ):  # PaddleOCR should raise an exception for invalid paths
        paddle_reader.read_text(nonexistent_path)
