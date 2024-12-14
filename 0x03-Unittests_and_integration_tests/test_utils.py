import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ("single_key", {"a": 1}, ("a",), 1),
        ("nested_key", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_nested_key", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test access_nested_map with different inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("empty_map", {}, ("a",), "'a'"),
        ("missing_nested_key", {"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, expected_message):
        """Test access_nested_map raises KeyError with appropriate message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)

class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand([
        ("example_url", "http://example.com", {"payload": True}),
        ("holberton_url", "http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, name, test_url, test_payload):
        """Test that get_json returns the expected result and makes one HTTP call."""
        with patch("utils.requests.get") as mocked_get:
            mocked_response = Mock()
            mocked_response.json.return_value = test_payload
            mocked_get.return_value = mocked_response

            result = get_json(test_url)

            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

if __name__ == "__main__":
    unittest.main()
