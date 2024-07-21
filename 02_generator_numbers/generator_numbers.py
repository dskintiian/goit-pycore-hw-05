from typing import Callable
from re import findall
from decimal import Decimal, ROUND_HALF_UP


def generator_numbers(user_text: str) -> Decimal:
    for number in findall(r'\d+\.?\d*', user_text):
        yield Decimal(number).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)


def sum_profit(user_text: str, numbers: Callable):
    return sum(numbers(user_text))


text = """Загальний дохід працівника складається з декількох частин: 
1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."""
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
