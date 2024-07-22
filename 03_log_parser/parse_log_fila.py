import sys
from re import match
from collections import Counter
from colorama import Fore, Back, Style
from typing import Generator, Iterable


def main():
    try:
        file_path = sys.argv[1]

        logs = list(map(parse_log_line, load_logs(file_path)))
        display_log_counts(count_logs_by_level(logs))

        if len(sys.argv) > 2:
            level = sys.argv[2]
            print(f'\nДеталі логів для рівня \'{level.upper()}\':')

            print(*map(lambda log: f'{log['date']} - {log["message"]}', filter_logs_by_level(logs, level)), sep='\n')

    except IndexError:
        print(f'{Fore.LIGHTWHITE_EX}{Back.RED}Бракує шляху до файла логів{Style.RESET_ALL}')
    except FileNotFoundError:
        print(f'{Fore.LIGHTWHITE_EX}{Back.RED}Файлу {file_path} не існує{Style.RESET_ALL}')
    except PermissionError:
        print(f'{Fore.LIGHTWHITE_EX}{Back.RED}Бракує прав на читання файлу {file_path}{Style.RESET_ALL}')


def parse_log_line(line: str) -> dict:
    date, level, message = match(r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s([A-Z]+)\s(.+)$', line).groups()

    return {'date': date, 'level': level, 'message': message}


def load_logs(file_path: str) -> Generator[str, None, None]:
    with open(file_path, 'r') as fh:
        for line in fh:
            yield line.strip()


def filter_logs_by_level(logs: list, level: str) -> list:
    return filter(lambda log: log['level'].lower() == level.lower(), logs)


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(map(lambda log: log['level'], logs)))


def display_log_counts(counts: dict):
    print('Рівень логування | Кількість')
    print('-----------------|----------')
    for level, number in counts.items():
        print(f'{level:<17}| {number:<9}')


if __name__ == '__main__':
    main()
