from bark.business import commands
from presentation.option import Option, get_option_choice, print_options, get_additional_data

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

    options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand()),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by={'title': 'ASC'})),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand()),
        'Q': Option('Quit', commands.QuitCommand())
    }

    print_options()

    shorcut = 'Default'
    while shorcut != 'Q':
        shortcut, chosen_option = get_option_choice(options)
        chosen_option.choose(table_name, shortcut)