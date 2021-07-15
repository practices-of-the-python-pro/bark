import sys

from bark.persist.database import DatabaseManager

from datetime import datetime
import requests

db = DatabaseManager('/Users/psw/Desktop/repository/dev/app_bark/bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self, table_name, data):
        db.create_table(
            table_name,
            data
        )


class AddBookmarkCommand:
    def execute(self, table_name, data, timestamp=None):
        data['date_added'] = timestamp if timestamp else datetime.now().isoformat()
        db.add(table_name, data)
        return 'Bookmark added'


class ListBookmarksCommand:
    def __init__(self, order_by=None, group_by=None):
        if order_by is None:
            order_by = {'date_added': 'ASC'}
        self.order_by = order_by
        self.group_by = group_by

    def execute(self, table_name, data=None):
        return db.select(
            table_name=table_name,
            criterias=data,
            order_by=self.order_by,
            group_by=self.group_by
        ).fetchall()


class DeleteBookmarkCommand:
    def execute(self, table_name, data):
        db.delete(
            table_name=table_name,
            criterias=data
        )


class QuitCommand:
    def execute(self):
        sys.exit()


class ImportGithubStarCommand:
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['url'],
            'notes': repo['description']
        }

    def execute(self, table_name, data):
        bookmarks_imported = 0

        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'

        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={
                    'Accept': 'application/vnd.github.v3.star+json'
                }
            )

            next_page_of_results = stars_response.links.get('next', {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info['repo']
                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    table_name=table_name,
                    data=self._extract_bookmark_info(repo),
                    timestamp=timestamp
                )

        return f'Inported {bookmarks_imported} bookmarks from starred repos!'