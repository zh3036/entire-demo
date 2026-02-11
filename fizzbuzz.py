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


def histogram(start: int, end: int, rules: list[tuple[int, str]] | None = None) -> dict[str, int]:
    """Count frequency of each label in the FizzBuzz run."""
    results = run(start, end, rules)
    counts: dict[str, int] = {}
    for r in results:
        key = r if not r.isdigit() else "(number)"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def format_chart(counts: dict[str, int], width: int = 40) -> str:
    """Render a horizontal bar chart from label counts."""
    if not counts:
        return ""
    max_val = max(counts.values())
    max_label = max(len(k) for k in counts)
    lines = []
    for label, count in counts.items():
        bar_len = int(count / max_val * width)
        lines.append(f"{label:>{max_label}} | {'█' * bar_len} {count}")
    return "\n".join(lines)


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
    parser.add_argument("--chart", action="store_true", help="Show frequency bar chart")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args(argv)

    if args.chart:
        counts = histogram(args.start, args.end, args.rules)
        if args.as_json:
            print(json.dumps(counts))
        else:
            print(format_chart(counts))
        return

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
