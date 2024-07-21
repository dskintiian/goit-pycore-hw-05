from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    Closure function for fibonacci calculation with built-in cache
    :return: Callable[[int], int]
    """
    cache = {0: 0, 1: 1}

    def fibonacci(n: int) -> int:
        if n in cache.keys():
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Отримуємо функцію fibonacci
fib = caching_fibonacci()

# Використовуємо функцію fibonacci для обчислення чисел Фібоначчі
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
