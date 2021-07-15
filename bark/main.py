from business import commands
from presentation.option import print_options, get_option_choice, generate_choice_option

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

    while True:
        chosen_option = get_option_choice(generate_choice_option())
        chosen_option.choose(table_name)
