from business import commands
from presentation.option import get_option_choice, print_options, generate_choice_option

if __name__ == '__main__':
    db_name = 'bookmarks'
    table_name = 'bookmarks'
    commands.CreateBookmarksTableCommand().execute(
        f'{table_name}',
        {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null'
        }
    )

    print_options()

    choice_option = generate_choice_option()

    shortcut = 'Default'
    while shortcut != 'Q':
        shortcut, chosen_option = get_option_choice(choice_option)
        chosen_option.choose(table_name, shortcut)