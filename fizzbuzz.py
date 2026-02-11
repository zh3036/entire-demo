"""A configurable FizzBuzz CLI that supports custom divisor rules."""

import argparse
import sys


def fizzbuzz(n: int, rules: list[tuple[int, str]] | None = None) -> str:
    """Return the FizzBuzz result for a single number.

    Args:
        n: The number to evaluate.
        rules: Optional list of (divisor, label) pairs. Defaults to classic FizzBuzz.
    """
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]

    result = "".join(label for divisor, label in rules if n % divisor == 0)
    return result or str(n)


def run(start: int, end: int, rules: list[tuple[int, str]] | None = None) -> list[str]:
    """Generate FizzBuzz results for a range of numbers."""
    return [fizzbuzz(n, rules) for n in range(start, end + 1)]


def parse_rule(s: str) -> tuple[int, str]:
    """Parse a rule string like '7:Woof' into (7, 'Woof')."""
    parts = s.split(":", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Rule must be in format 'divisor:label', got '{s}'")
    try:
        divisor = int(parts[0])
    except ValueError:
        raise argparse.ArgumentTypeError(f"Divisor must be an integer, got '{parts[0]}'")
    if divisor <= 0:
        raise argparse.ArgumentTypeError(f"Divisor must be positive, got {divisor}")
    return (divisor, parts[1])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Configurable FizzBuzz")
    parser.add_argument("end", type=int, help="Count up to this number")
    parser.add_argument("--start", type=int, default=1, help="Start from (default: 1)")
    parser.add_argument(
        "--rule", type=parse_rule, action="append", dest="rules",
        help="Custom rule as 'divisor:label' (e.g. 7:Woof). Can be repeated."
    )
    args = parser.parse_args(argv)

    results = run(args.start, args.end, args.rules)
    for line in results:
        print(line)


if __name__ == "__main__":
    main()
