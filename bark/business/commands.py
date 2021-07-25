import sys

from bark.persist.database import DatabaseManager, BookmarkDatabase

from datetime import datetime
import requests
from abc import ABC, abstractmethod
# db = DatabaseManager('/Users/psw/Desktop/repository/dev/app_bark/bookmarks.db')

persistance = BookmarkDatabase()


class Command(ABC):
    @abstractmethod
    def execute(self, data, timestamp):
        pass


class CreateBookmarksTableCommand(Command):
    def execute(self, data, timestamp=None):
        persistance.create(data)


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp if timestamp else datetime.now().isoformat()
        persistance.create(data)
        # db.add(table_name, data)
        return True, None


class EditBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        # db.edit(table_name, data)
        persistance.edit(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by=None, group_by=None):
        if order_by is None:
            order_by = {'date_added': 'ASC'}
        self.order_by = order_by
        self.group_by = group_by

    def execute(self, data=None, timestamp=None):
        return True, persistance.list(criterias=data, order_by=self.order_by, group_by=self.group_by)
        # return True, db.select(
        #     table_name=table_name,
        #     criterias=data,
        #     order_by=self.order_by,
        #     group_by=self.group_by
        # ).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, table_name, data, timestamp=None):
        # db.delete(
        #     table_name=table_name,
        #     criterias=data
        # )
        persistance.delete(data)


class QuitCommand(Command):
    def execute(self, table_name=None, data=None, timestamp=None):
        sys.exit()



class ImportGithubStarCommand(Command):
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['url'],
            'notes': repo['description']
        }

    def execute(self, table_name, data, timestamp=None):
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