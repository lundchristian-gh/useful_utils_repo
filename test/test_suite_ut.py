import os
import sys
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(1, project_root)

from useful import TestSuite


class TestTestSuite(unittest.TestCase):
    def test_no_functions(self) -> bool:
        """Test that no functions will result in a failure"""
        uut = TestSuite()
        with self.assertRaises(AssertionError):
            uut.run()


if __name__ == "__main__":
    unittest.main()
