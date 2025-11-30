def divide_numbers(a: float, b: float) -> float:
    """Divides two numbers and returns the result.

    Args:
        a: The dividend
        b: The divisor

    Returns:
        The result of a divided by b
    """
    return a / b


def main() -> None:
    """Main function to demonstrate the division operation."""
    x: float = 10.0
    y: float = 0.0
    result: float = divide_numbers(x, y)


if __name__ == "__main__":
    main()
