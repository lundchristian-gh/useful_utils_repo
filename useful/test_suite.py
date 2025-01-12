import random
from useful.common import okay, fail, Log


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
        """Initializes the test suite with all test functions.
        If you define a custom constructor, make sure to call
        super().__init__() as it will automatically find all test functions.
        """
        self._log: Log = log
        self._prefix: tuple[str, ...] = prefix
        self._random_order: bool = random_order
        self._save_artifact: bool = save_artifact

        self._test_functions: list[callable] = []
        for function in dir(self):
            if callable(getattr(self, function)) and function.startswith(self._prefix):
                self._test_functions.append(getattr(self, function))

    def _run_tests(self, tests: list[callable]) -> bool:
        """Note: Note: Intended as private method!"""
        passed: int = 0
        total: int = len(tests)
        results: list[tuple[str, bool]] = []

        for test in tests:
            result = test()
            assert int(result) in [0, 1], "Test functions must return boolean values"
            passed += int(result)
            results.append((test.__doc__, result))

        return {
            "outcomes": results,
            "passed": passed,
            "total": total,
            "percent": (passed / total) * 100,
        }

    def _process_results(self, results: dict[str, any]) -> bool:
        """Note: Intended as private method!"""
        outcomes: list[tuple[str, bool]] = results["outcomes"]
        passed: int = results["passed"]
        num_tests: int = results["total"]
        percent: float = results["percent"]
        self._log_results(outcomes, passed, num_tests, percent)
        return passed == num_tests

    def _log_results(
        self,
        outcomes: list[tuple[str, bool]],
        passed: int,
        num_tests: int,
        percent: float,
    ) -> None:
        """Note: Note: Intended as private method!"""
        for name, outcome in outcomes:
            if outcome:
                self._log.green(f"PASS\t{name}")
            else:
                self._log.red(f"FAIL\t{name}")
        self._log.plain(f"\n{passed} OF {num_tests} ({percent:.2f}%) TESTS PASSED\n")

    def run(self) -> bool:
        """Runs all the tests in the test suite.
        Returns:
            bool: True if all tests pass, otherwise False.
        """
        if not hasattr(self, "_test_functions"):
            raise RuntimeError("Do not override the constructor.")
        assert len(self._test_functions) > 0, "No tests found in test suite"

        self._log.plain("\n[~] SEQUENTIAL TEST RUN\n")
        sequential_results: dict[str, any] = self._run_tests(self._test_functions)
        sequential_outcome: bool = self._process_results(sequential_results)
        result: bool = sequential_outcome

        if self._random_order:
            if not sequential_outcome:
                self._log.plain("[~] TESTS MUST PASS IN SEQUENTIAL ORDER FIRST\n")
            else:
                self._log.plain("[~] RANDOM TEST RUN\n")
                random.shuffle(self._test_functions)
                random_results: dict[str, any] = self._run_tests(self._test_functions)
                random_outcome: bool = self._process_results(random_results)
                result = random_outcome

        self._log.print_terminal()
        if self._save_artifact:
            self._log.save_text("test_results.txt")

        return result
