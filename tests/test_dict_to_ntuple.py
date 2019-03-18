"""PyKBLib Test Suite.

This test suite assumes that you've got Keybase running on your system. It also
assumes that you're logged in, and that the active user is a member of the
`pykblib_dev` team. (This is an open team, so all are free to join.)
"""

import collections
from unittest import TestCase

from steffentools import dict_to_ntuple


class DictToNtupleTest(TestCase):
    """Test the dict_to_ntuple function."""

    def setUp(self):
        """Create a namedtuple from a demonstration dict."""
        # Create our demo dict.
        self.demo_dict = {
            # Test string input.
            "result": "success",
            # Test a list input.
            "demo_list": [
                # The list will have namedtuples within it.
                {"id": 1, "msg": "message 1"},
                {"id": 2, "msg": "message 2"},
            ],
            "nested_list": [
                # Lists inside dicts inside lists inside lists.
                [{"value": ["a", "b", "c"]}, {"value": ["d", "e", "f"]}],
                [{"value": ["g", "h", "i"]}, {"value": ["j", "k", "l"]}],
            ],
            "nested_ntuple": {
                # Dicts inside dicts.
                "first": {"number": 1, "boolean": True},
                "second": {"number": 2, "boolean": False},
                "oddball": {
                    # This one's different from the rest, containing odd cases.
                    "empty_dict": dict(),
                    "empty_list": list(),
                    "none": None,
                },
            },
        }
        # Convert the demo dict into a nested namedtuple.
        self.demo = dict_to_ntuple(self.demo_dict)

    def test_dict_to_ntuple(self):
        """Ensure that dict_to_ntuple is working as expected."""
        self.assertEqual(self.demo.result, self.demo_dict["result"])
        self.assertIsInstance(self.demo.demo_list, list)
        for index in range(len(self.demo_dict["demo_list"])):
            self.assertEqual(
                self.demo.demo_list[index].id,
                self.demo_dict["demo_list"][index]["id"],
            )
            self.assertEqual(
                self.demo.demo_list[index].msg,
                self.demo_dict["demo_list"][index]["msg"],
            )
        self.assertIsInstance(self.demo.nested_list, list)
        for index in range(len(self.demo_dict["nested_list"])):
            for index2 in range(len(self.demo_dict["nested_list"][index])):
                for index3 in range(
                    len(self.demo_dict["nested_list"][index][index2]["value"])
                ):
                    self.assertEqual(
                        self.demo.nested_list[index][index2].value[index3],
                        self.demo_dict["nested_list"][index][index2]["value"][
                            index3
                        ],
                    )
        self.assertEqual(
            self.demo.nested_ntuple.first.number,
            self.demo_dict["nested_ntuple"]["first"]["number"],
        )
        self.assertEqual(
            self.demo.nested_ntuple.first.boolean,
            self.demo_dict["nested_ntuple"]["first"]["boolean"],
        )
        self.assertEqual(
            self.demo.nested_ntuple.second.number,
            self.demo_dict["nested_ntuple"]["second"]["number"],
        )
        self.assertEqual(
            self.demo.nested_ntuple.second.boolean,
            self.demo_dict["nested_ntuple"]["second"]["boolean"],
        )
        self.assertIsInstance(self.demo.nested_ntuple.oddball.empty_dict, dict)
        self.assertEqual(
            self.demo.nested_ntuple.oddball.empty_dict,
            self.demo_dict["nested_ntuple"]["oddball"]["empty_dict"],
        )
        self.assertIsInstance(self.demo.nested_ntuple.oddball.empty_list, list)
        self.assertEqual(
            self.demo.nested_ntuple.oddball.empty_list,
            self.demo_dict["nested_ntuple"]["oddball"]["empty_list"],
        )
        self.assertIsInstance(self.demo.nested_ntuple.oddball.none, type(None))
        self.assertEqual(
            self.demo.nested_ntuple.oddball.none,
            self.demo_dict["nested_ntuple"]["oddball"]["none"],
        )
