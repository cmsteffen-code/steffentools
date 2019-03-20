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
            "demo_tuple": (
                # We'll just demonstrate a tuple here.
                "first",
                "second",
                "third",
            ),
            "demo_set": {"a","b","c"},
            "nested_list": [
                # Lists inside dicts inside lists inside lists.
                [{"value": ["a", "b", "c"]}, {"value": ["d", "e", "f"]}],
                [{"value": ["g", "h", "i"]}, {"value": ["j", "k", "l"]}],
            ],
            "nested_tuple": (
                # We'll put some dicts into a tuple.
                {"test": "success"},
                {"test": "success"},
                {"test": "success"},
            ),
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
            "bad_dict": {
                # Create a dict that couldn't be properly parsed into a ntuple.
                # Integers can't be field names, so this can't become a ntuple.
                1: "one",
                # However, the elements of this dictionary could still be
                # converted.
                2: {"test": "success"},
                3: {"test": {"two": "success"}},
            }
        }
        # Convert the demo dict into a nested namedtuple.
        self.demo = dict_to_ntuple(self.demo_dict)

    def test_dict_to_ntuple(self):
        """Ensure that dict_to_ntuple is working as expected."""
        # Ensure that the result value matches.
        self.assertEqual(self.demo.result, self.demo_dict["result"])
        # Ensure that the demo list is a list.
        self.assertIsInstance(self.demo.demo_list, list)
        # Ensure that the demo list translated properly.
        for index in range(len(self.demo_dict["demo_list"])):
            # Check the id value of each element in the list.
            self.assertEqual(
                self.demo.demo_list[index].id,
                self.demo_dict["demo_list"][index]["id"],
            )
            # Check the msg value of each element in the list.
            self.assertEqual(
                self.demo.demo_list[index].msg,
                self.demo_dict["demo_list"][index]["msg"],
            )
        # Ensure that the demo_tuple translated properly.
        self.assertTrue(
            all(
                item in self.demo.demo_tuple
                for item in ["first", "second", "third"]
            )
        )
        # Ensure that the nested_list is a list.
        self.assertIsInstance(self.demo.nested_list, list)
        # Ensure that the nested_list translated properly.
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
        # Ensure that the nested_tuple is a tuple.
        self.assertIsInstance(self.demo.nested_tuple, tuple)
        # Ensure that the nested_tuple translated properly.
        self.assertTrue(
            all(
                [item.test == "success" for item in self.demo.nested_tuple]
            )
        )
        # Ensure that the nested_ntuple translated properly.
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
        # Ensure that dicts that can't be converted don't crash the system, but
        # that their contents are still iterated.
        self.assertIsInstance(self.demo.bad_dict, dict)
        # Ensure that the bad_dict was properly translated.
        self.assertEqual(self.demo.bad_dict[1], "one")
        self.assertEqual(self.demo.bad_dict[2].test, "success")
        self.assertEqual(self.demo.bad_dict[3].test.two, "success")
        # Ensure that the demo_set is a set.
        self.assertIsInstance(self.demo.demo_set, set)
        # Ensure that the demo_set translated properly.
        self.assertEqual(self.demo.demo_set, self.demo_dict["demo_set"])
