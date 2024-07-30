#!/usr/bin/env python3
"""
Unittests for the utils module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests suite for access_nested_map function in utils module.

    Args:
        unittest (_type_): _description_
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_output):
        """
        Tests access_nested_map returns the expected result.
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_output)

    @parameterized.expand(
        [
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError)
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_output):
        """
        Tests access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(expected_output) as context:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Tests suite for get_json function in utils module.

    Args:
        unittest (_type_): _description_
    """
    @parameterized.expand(
        [
            ('http://example.com', {'payload': True}),
            ('http://holberton.io', {'payload': False})
        ]
    )
    def test_get_json(self, url, expected_output):
        """
        Tests get_json returns the expected result.
        """
        mock_response = Mock()
        mock_response.json.return_value = expected_output
        with patch('requests.get', return_value=mock_response):
            response = get_json(url)

            self.assertEqual(response, expected_output)


class TestMemoize(unittest.TestCase):
    """
    Tests suite for memoize decorator in utils module.

    Args:
        unittest (_type_): _description_
    """

    def test_memoize(self):
        """
        Tests memoize decorator caches the result of a method call.

        Returns:
                _type_: _description_
        """

        class TestClass:
            """
            Class with method a_method and memoized property.
            """

            def a_method(self):
                """method in class

                Returns:
                        _type_: _description_
                """
                return 42

            @memoize
            def a_property(self):
                """memoized property

                Returns:
                        _type_: _description_
                """
                return self.a_method()

        test_obj = TestClass()

        with patch.object(test_obj, 'a_method') as mock_method:
            mock_method.return_value = 42

            result1 = test_obj.a_property
            result2 = test_obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
