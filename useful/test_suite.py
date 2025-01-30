import random
from useful.common import Log


class TestSuite:
    """
    TestSuite enables simple testing of your code.
    Inherit from the class, and name all your test functions with the prefixes.
    Make sure to return true or false depending on the output.
    NB: Do not override the constructor.
    """

    def __init__(
        self,
        log: Log = Log(),
        random_order: bool = False,
        save_artifact: bool = False,
        prefix: tuple[str, ...] = ("test_",),
    ) -> None:
        """Initializes the test suite with all test functions, do not override!"""
        self._log: Log = log
        self._prefix: tuple[str, ...] = prefix
        self._random_order: bool = random_order
        self._save_artifact: bool = save_artifact

        self._test_functions: list[callable] = []
        for function in dir(self):
            if callable(getattr(self, function)) and function.startswith(self._prefix):
                self._test_functions.append(getattr(self, function))

    def _run_tests(self, tests: list[callable]) -> bool:
        """Note: Private method!"""
        passed: int = 0
        num_tests: int = len(tests)
        results: list[tuple[str, bool]] = []

        for test in tests:
            result = test()
            assert int(result) in [0, 1], "Test functions must return boolean values"
            passed += int(result)
            results.append((test.__doc__, result))

        return {
            "outcomes": results,
            "passed": passed,
            "num_tests": num_tests,
            "percent": (passed / num_tests) * 100,
        }

    def _log_results(self, order: str, results: dict[str, any]) -> None:
        """Note: Private method!"""
        self._log.write(f"\n[~] {order.upper()} ORDER TEST RUN\n")
        for name, outcome in results["outcomes"]:
            if outcome:
                self._log.write(f"PASS\t{name}", "green")
            else:
                self._log.write(f"FAIL\t{name}", "red")
        self._log.write(
            f"\n{results['passed']} OF {results['num_tests']} ({results['percent']:.2f}%) TESTS PASSED\n"
        )

    def run(self) -> bool:
        """Runs all the tests in the test suite.
        Returns:
            bool: True if all tests pass, otherwise False.
        """
        if not hasattr(self, "_test_functions"):
            raise RuntimeError("Do not override the constructor.")

        assert len(self._test_functions) > 0, "No tests found in test suite"

        # type(self).__name__}

        seq_results: dict[str, any] = self._run_tests(self._test_functions)
        seq_outcome: bool = seq_results["passed"] == seq_results["num_tests"]
        self._log_results("sequential", seq_results)
        result: bool = seq_outcome

        if self._random_order:
            if not seq_outcome:
                self._log.write("[~] TESTS MUST PASS IN SEQUENTIAL ORDER FIRST\n")
            else:
                random.shuffle(self._test_functions)
                rand_results: dict[str, any] = self._run_tests(self._test_functions)
                rand_outcome: bool = rand_results["passed"] == rand_results["num_tests"]
                self._log_results("random", rand_results)
                result = rand_outcome

        self._log.print_terminal()
        if self._save_artifact:
            self._log.save_text("test_results.txt")

        return result
