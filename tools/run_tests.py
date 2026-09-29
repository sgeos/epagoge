"""The full gate requires all tests, including the training dependency group."""

import sys
import unittest


def main() -> int:
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if result.skipped:
        print(
            f"Full verification refuses {len(result.skipped)} skipped tests",
            file=sys.stderr,
        )
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
