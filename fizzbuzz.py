"""A configurable FizzBuzz CLI that supports custom divisor rules."""

import argparse
import json
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


def stats(start: int, end: int, rules: list[tuple[int, str]] | None = None) -> dict:
    """Return statistics about the FizzBuzz run."""
    results = run(start, end, rules)
    total = len(results)
    numeric = sum(1 for r in results if r.isdigit())
    return {
        "total": total,
        "numeric": numeric,
        "replaced": total - numeric,
        "replacement_rate": round((total - numeric) / total * 100, 1),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Configurable FizzBuzz")
    parser.add_argument("end", type=int, help="Count up to this number")
    parser.add_argument("--start", type=int, default=1, help="Start from (default: 1)")
    parser.add_argument(
        "--rule", type=parse_rule, action="append", dest="rules",
        help="Custom rule as 'divisor:label' (e.g. 7:Woof). Can be repeated."
    )
    parser.add_argument("--stats", action="store_true", help="Show statistics instead of results")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args(argv)

    if args.stats:
        s = stats(args.start, args.end, args.rules)
        if args.as_json:
            print(json.dumps(s))
        else:
            print(f"Total: {s['total']}, Replaced: {s['replaced']} ({s['replacement_rate']}%)")
        return

    results = run(args.start, args.end, args.rules)
    if args.as_json:
        print(json.dumps(results))
    else:
        for line in results:
            print(line)


if __name__ == "__main__":
    main()
