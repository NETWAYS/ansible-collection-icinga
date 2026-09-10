import unittest

from ansible.errors import AnsibleFilterError
from plugins.filter.items2dict import items2dict


class TestItems2Dict(unittest.TestCase):
    test_list = [
        {
            'name': 'first_element',
            'param1': 'value1',
            'param2': 'value2',
        },
        {
            'name': 'second_element',
            'param1': 'other_value1',
            'param2': 'other_value2',
            'extra_param3': 'other_value3',
        },
    ]

    def test_default(self):
        expected = {
            'first_element': {
                'name': 'first_element',
                'param1': 'value1',
                'param2': 'value2',
            },
            'second_element': {
                'name': 'second_element',
                'param1': 'other_value1',
                'param2': 'other_value2',
                'extra_param3': 'other_value3',
            },
        }
        result = items2dict(
            self.test_list,
        )
        self.assertEqual(result, expected)

    def test_omit_key(self):
        expected = {
            'first_element': {
                'param1': 'value1',
                'param2': 'value2',
            },
            'second_element': {
                'param1': 'other_value1',
                'param2': 'other_value2',
                'extra_param3': 'other_value3',
            },
        }
        result = items2dict(
            self.test_list,
            keep_key=False,
        )
        self.assertEqual(result, expected)

    def test_custom_key(self):
        expected = {
            'value1': {
                'name': 'first_element',
                'param1': 'value1',
                'param2': 'value2',
            },
            'other_value1': {
                'name': 'second_element',
                'param1': 'other_value1',
                'param2': 'other_value2',
                'extra_param3': 'other_value3',
            },
        }
        result = items2dict(
            self.test_list,
            key='param1',
        )
        self.assertEqual(result, expected)

    def test_non_unique_key(self):
        # Add another element with a shared value for the 'name' key
        test_list = self.test_list + [
            {
                'name': 'first_element',
                'param1': 'something1',
                'param2': 'something2',
            },
        ]
        with self.assertRaises(AnsibleFilterError):
            items2dict(
                test_list,
            )


if __name__ == '__main__':
    unittest.main()
