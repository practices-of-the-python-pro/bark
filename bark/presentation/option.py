from bark.business import commands


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self, table_name, chosen_option):
        data = get_additional_data(chosen_option) if chosen_option in additional_options else None
        message = self.command.execute(table_name, data) if data else self.command.execute(table_name)
        message and print(message)

    def __str__(self):
        return self.name

choice_options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand()),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by={'title': 'ASC'})),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand()),
        'Q': Option('Quit', commands.QuitCommand())
    }


additional_options = {
    'A': {
        'title': ['not null'],
        'url': ['not null'],
        'notes': []
    },
    'D': {
        'id': ['int', 'not null']
    }
}


def generate_choice_option():
    return choice_options

def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options
    # 대소문자 구분없이 options 안에 choice가 있을 경우 True


def get_option_choice(options):
    choice = input('Choose a option : ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose a option : ')
    return choice, options[choice.upper()]


def print_options():
    for shortcut, option in choice_options.items():
        print(f'({shortcut}) {option}')
    print()


def validate_input_value(value, options):

    def not_null_validate(value, options):
        if 'not null' in options:
            return True if value else False
        return True

    if not not_null_validate(value, options):
        return False
    return True


def get_additional_data(chosen_option):
    if chosen_option not in additional_options:
        return None

    additional_data = {}
    for column, options in additional_options[chosen_option].items():
        value = input(f'{column} 입력 : ')
        if validate_input_value(value, options):
            additional_data[column] = value
    return additional_data



