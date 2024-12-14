#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from utils import access_nested_map, get_json
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
    def test_access_nested_map_exception(
            self, name, nested_map, path, expected_message):
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
        """Test get_json returns expected result and makes one HTTP call."""
        with patch("utils.requests.get") as mocked_get:
            mocked_response = Mock()
            mocked_response.json.return_value = test_payload
            mocked_get.return_value = mocked_response

            result = get_json(test_url)

            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestGithubOrgClient(unittest.TestCase):

    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", "google"),
        ("abc", "abc"),
    ])
    @patch("client.get_json")
    def test_org(self, name, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the expected value."""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/mock-org/repos"}

        client = GithubOrgClient("mock-org")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/mock-org/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=Mock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test that public_repos returns the expected list of repositories."""
        mock_public_repos_url.return_value = \
            "https://api.github.com/orgs/mock-org/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        client = GithubOrgClient("mock-org")
        result = client.public_repos

        self.assertEqual(result, ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/mock-org/repos")

    @parameterized.expand([("repo_with_license",
                            {"license": {"key": "my_license"}},
                            "my_license",
                            True),
                           ("repo_without_license",
                            {"license": {"key": "other_license"}},
                            "my_license",
                            False),
                           ("repo_no_license_key",
                            {"license": {}},
                            "my_license",
                            False),
                           ])
    def test_has_license(self, name, repo, license_key, expected):
        """Test that has_license returns the correct result."""
        client = GithubOrgClient("mock-org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return Mock(json=lambda: cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
