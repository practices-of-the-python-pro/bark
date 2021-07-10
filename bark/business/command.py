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
