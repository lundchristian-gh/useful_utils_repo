import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(1, project_root)

from useful import TestSuite


class TestTestSuite(TestSuite):
    """Testing the TestSuite using the TestSuite"""

    def test_no_functions(self) -> bool:
        """Tests must be implemented in order to run."""
        uut = TestSuite()
        try:
            uut.run()
            return False
        except AssertionError:
            return True

    def test_override_ctor(self) -> bool:
        """Forbidden to override the constructor."""

        class TestSuiteUUT(TestSuite):
            def __init__(self):
                pass

            def test_dummy(self):
                return True

        uut = TestSuiteUUT()
        try:
            uut.run()
            return False
        except RuntimeError:
            return True

    def test_invalid_return_value(self) -> bool:
        """Test functions must return true or false."""

        class TestSuiteUUT(TestSuite):

            def test_invalid_return(self):
                return 3

        uut = TestSuiteUUT()
        try:
            uut.run()
            return False
        except AssertionError:
            return True


def main() -> None:
    suite = TestTestSuite()
    sys.exit(not suite.run())


if __name__ == "__main__":
    main()
