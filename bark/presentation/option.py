from bark.business import commands


class Option:
    def __init__(self, name, command, prep_call=None, key=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.key = key

    def choose(self, table_name):
        data = self.prep_call(self.key)() if self.prep_call else None
        message = self.command.execute(table_name, data) if data else self.command.execute(table_name)
        message and print(message)

    def __str__(self):
        return self.name


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_data(key):
    def get_add_data():
        return {
            'title': get_user_input('Title'),
            'url': get_user_input('URL'),
            'notes': get_user_input('Notes', required=False)
        }

    def get_delete_data():
        return {
            'id': get_user_input('Id')
        }

    method_by_key = {
        'A': get_add_data,
        'D': get_delete_data
    }

    return method_by_key[key] if method_by_key.get(key) else None


choice_options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_data, key='A'),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by={'title': 'ASC'})),
        'G': Option('Import Github star', commands.ImportGithubStarCommand()),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_data, key='D'),
        'Q': Option('Quit', commands.QuitCommand())
    }


def generate_choice_option():
    return choice_options


def print_options():
    for shortcut, option in choice_options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Choose an option : ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option : ')
    return options[choice.upper()]

