from abc import ABC, abstractmethod
import sqlite3


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError('Persistence layers must implement a create method!')

    @abstractmethod
    def list(self, data):
        raise NotImplementedError('Persistence layers must implement a list method!')

    @abstractmethod
    def edit(self, data):
        raise NotImplementedError('Persistence layers must implement an edit method!')

    @abstractmethod
    def delete(self, data):
        raise NotImplementedError('Persistence layers must implement a delete method!')


class BookmarkDatabase(PersistenceLayer):
    def __init__(self):
        self.table_name = 'bookmarks'
        self.db = DatabaseManager('/Users/psw/Desktop/repository/dev/app_bark/bookmarks.db')

        self.db.create_table(self.table_name,
                             {
                                 'id': 'integer primary key autoincrement',
                                 'title': 'text not null',
                                 'url': 'text not null',
                                 'notes': 'text',
                                 'date_added': 'text not null'
                             }
                             )

    def create(self, data):
        self.db.add(self.table_name, data)

    def list(self, criterias, order_by='date_added', group_by=None):
        return self.db.select(self.table_name, order_by=order_by, group_by=group_by).fetchall()

    def edit(self, data):
        self.db.edit(self.table_name, data)

    def delete(self, data):
        self.db.delete(self.table_name, data)


class DatabaseManager:
    def __init__(self, file_path):
        self.connection = sqlite3.connect(file_path)

    def __del__(self):
        self.connection.close()

    def _execute(self, sql, values=None):
        with self.connection:  # one transaction
            cursor = self.connection.cursor()
            cursor.execute(sql, values or [])
            return cursor

    def generate_criterias_to_values(self, criterias):
        return ', '.join(criterias)

    def create_table(self, table_name, columns_info):
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns_info.items()
        ]

        create_sql = f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)})
            '''

        self._execute(
            create_sql
        )

    def add(self, table_name, columns_info):
        '''
        columns_info e.g
        {
        'title': 'hello bark!',
        'url': 'www.bark.com',
        'notes': 'bark application',
        'date_added': '2019-02-01T18:46:32.111111'
        }
        '''

        placeholders = ', '.join('?' * len(columns_info))
        columns = [k for k in columns_info.keys()]
        values = [v for v in columns_info.values()]

        add_sql = f'''
            INSERT INTO {table_name} 
            ({', '.join(columns)})
            VALUES ({placeholders})
        '''

        '''
        add_sql e.g
        INSERT INTO table ('name', 'id') VALUES (?, ?)
        '''

        self._execute(
            add_sql,
            values
        )

    def delete(self, table_name, criterias):
        placeholders = [f'{column} = ?' for column in criterias.keys()]
        delete_criterias = ' AND '.join(placeholders)
        values = ', '.join(criterias.values())

        delete_sql = f'''
            DELETE FROM {table_name}
            WHERE {delete_criterias}
        '''

        self._execute(
            delete_sql,
            values
        )

        return True, None

    def edit(self, table_name, criterias):
        set_criterias = [f'{column} = "{value}"' for column, value in criterias.items() if
                         (column not in ['id']) and value]
        where_criterias = [f'{column} = ?' for column in criterias.keys() if column in ['id']]

        set_criterias = self.generate_criterias_to_values(set_criterias)
        where_criterias = self.generate_criterias_to_values(where_criterias)

        where_values = [value for column, value in criterias.items() if column in ['id']]

        edit_sql = f'''
            UPDATE {table_name} 
            SET {set_criterias}
            WHERE {where_criterias} 
        '''

        print(f'====edit sql : {edit_sql}')
        print(where_values)
        self._execute(
            edit_sql,
            where_values
        )

        return True, None

    def select(self, table_name, criterias=None, order_by=None, group_by=None):
        select_sql = f'''
            SELECT * FROM {table_name}
        '''
        values = [v for v in criterias.values()] if criterias else []

        if criterias:
            placeholders = [f'{column} = ?' for column in criterias.keys()]
            select_creteria = ' AND '.join(placeholders)
            select_sql += select_creteria

        if order_by:
            order_by_criteria = ' '.join(
                [f'{column} {order_condition}' for column, order_condition in order_by.items()])
            select_sql += f'ORDER BY {order_by_criteria}'

        if group_by:
            group_by_criteria = ', '.join(group_by)
            select_sql += f'GROUP BY {group_by_criteria}'

        return self._execute(select_sql, values)
