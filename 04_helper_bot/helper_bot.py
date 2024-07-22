from colorama import Fore, Back, Style
from typing import Callable
from functools import wraps


def input_error(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):

        print(func.__name__)
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            # return format_error('Invalid command.')
            return format_error(f'Invalid command. [KeyError {e}]')
        except ValueError as e:
            return format_error(f'Enter the argument for the command [ValueError {e}]')
        except IndexError as e:
            return format_error(f'Enter the argument for the command [IndexError {e}]')
        except TypeError as e:
            return format_error(f'Enter the argument for the command [TypeError {e}]')

    return wrapper


@input_error
def parse_command(input_sting: str):
    command, *arguments = input_sting.split()
    if len(arguments) > 2:
        last_arg = arguments.pop()
        return [command, ' '.join(arguments), last_arg]

    return command, *arguments


def main():
    contacts = {}

    print(hello_handler())
    print(help_handler())
    try:
        while True:
            command, *arguments = parse_command(input('>>'))

            if command in ['exit', 'close']:
                print(format_success('Good bye!'))
                break

            print(arguments)

            print(contacts_handlers(command, contacts, *arguments))

    except KeyboardInterrupt:
        print(format_success('\nGood bye!'))


@input_error
def contacts_handlers(command, contacts, *arguments):
    no_args_handlers_map = {
        'hello': hello_handler,
        'help': help_handler,
    }

    handlers_map = {
        'add': add_contact_handler,
        'change': change_contact_handler,
        'phone': get_contact_handler,
        'all': get_all_contacts_handler,
    }

    if command in no_args_handlers_map:
        return no_args_handlers_map[command]()

    return handlers_map[command](contacts, *arguments)


def hello_handler():
    return 'Hello, how can I help you?'


def help_handler():
    return f'''Possible commands:
{Fore.LIGHTWHITE_EX}{Back.BLUE}help{Style.RESET_ALL} - prints list of available commands
{Fore.LIGHTWHITE_EX}{Back.BLUE}hello{Style.RESET_ALL} - prints a greeting 
{Fore.LIGHTWHITE_EX}{Back.BLUE}add [name] [phone number]{Style.RESET_ALL} - create a contact with a phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}change [name] [phone number]{Style.RESET_ALL} - changes a contact phone number 
{Fore.LIGHTWHITE_EX}{Back.BLUE}phone [name]{Style.RESET_ALL} - prints contacts phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}all{Style.RESET_ALL} - prints all contacts
{Fore.LIGHTWHITE_EX}{Back.BLUE}close{Style.RESET_ALL} або {Fore.YELLOW}{Back.BLUE}exit{Style.RESET_ALL} - terminates a program    
    '''


@input_error
def add_contact_handler(contacts: dict, name: str, phone: str):
    name = name.lower().capitalize()
    contacts[name] = phone
    return format_success('Contact added')


@input_error
def change_contact_handler(contacts: dict, name: str, phone: str):
    name = name.lower().capitalize()
    if name in contacts.keys():
        contacts[name] = phone
        return format_success('Contact updated.')

    return format_error('Contact not found.')


@input_error
def get_contact_handler(contacts: dict, name: str, *args):
    name = name.lower().capitalize()
    if name in contacts.keys():
        return contacts[name]

    return format_error('Contact not found.')


def get_all_contacts_handler(contacts: dict, *args):
    return '\n'.join(map(lambda name: f'{name}: {contacts[name]}', contacts.keys()))


def format_error(error: str):
    return f'{Fore.LIGHTWHITE_EX}{Back.RED}{error}{Style.RESET_ALL}'


def format_success(message: str):
    return f'{Fore.GREEN}{message}{Style.RESET_ALL}'


if __name__ == '__main__':
    main()
