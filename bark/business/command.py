from bark.persist.database import DatabaseManager

from datetime import datetime

db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            'bookmarks',
            {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                'url': 'text not null',
                'notes': 'text',
                'date_added': 'text not null'
            }
        )


class AddBookmarkCommand:
    def execute(self, data):
        data['date_added'] = datetime.now().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added'


class ListBookmarksCommand:
    def __init__(self, order_by='date_added', group_by=None):
        self.order_by = order_by
        self.group_by = group_by

    def execute(self, data):
        db.select(
            table_name='bookmarks',
            columns='*',
            criterias=data,
            order_by=self.order_by,
            group_by=self.group_by
        )