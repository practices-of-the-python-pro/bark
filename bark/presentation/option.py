from bark.business import commands


class Option:
    def __init__(self, name, command, prep_call=None, key=None, success_message='{result}'):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.key = key
        self.success_message = success_message

    def choose(self):
        data = self.prep_call(self.key)() if self.prep_call else None
        success, result = self.command.execute(data=data)

        formatted_result = ''
        if isinstance(result, list):
            for bookmark in result:
                formatted_result += '\n' + format_bookmark(bookmark)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    def __str__(self):
        return self.name


def format_bookmark(bookmark):
    return '\t'.join(
        str(field) if field else ''
        for field in bookmark
    )


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

    def get_import_github_start_data():
        return {
            'github_username': get_user_input('Github username'),
            'preserve_timestamps': get_user_input(
                'Preserve timestamps [Y/n]', required=False
            ) in {'Y', 'y', None}

        }

    def get_edit_data():
        return {
            'id': get_user_input('Id', required=True),
            'title': get_user_input('Title', required=False),
            'url': get_user_input('URL', required=False),
            'notes': get_user_input('Notes', required=False)
        }

    method_by_key = {
        'A': get_add_data,
        'D': get_delete_data,
        'G': get_import_github_start_data,
        'E': get_edit_data
    }

    return method_by_key[key] if method_by_key.get(key) else None


choice_options = {
        'A': Option(
            'Add a bookmark',
            commands.AddBookmarkCommand(),
            prep_call=get_data,
            key='A',
            success_message='Bookmark Added!'),
        'B': Option(
            'List bookmarks by date',
            commands.ListBookmarksCommand()),
        'T': Option(
            'List bookmarks by title',
            commands.ListBookmarksCommand(order_by={'title': 'ASC'})),
        'G': Option(
            'Import Github star',
            commands.ImportGithubStarCommand(),
            prep_call=get_data,
            key='G',
            success_message='Imported {result} bookmarks fromn starred repos!'),
        'E': Option(
            'Edit a Bookmark',
            commands.EditBookmarkCommand(),
            prep_call=get_data,
            key='E',
            success_message='Bookmark Edited!'
        ),
        'D': Option(
            'Delete a bookmark',
            commands.DeleteBookmarkCommand(),
            prep_call=get_data,
            key='D',
            success_message='Bookmark deleted!'),
        'Q': Option(
            'Quit',
            commands.QuitCommand())
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

