import sqlite3


class DatabaseManager:
    def __init__(self, file_path):
        self.connection = sqlite3.connect(file_path)

    def __del__(self):
        self.connection.close()

    def _execute(self, sql, values=None):
        with self.connection():  # one transaction
            cursor = self.connection.cursor()
            cursor.execute(sql, values or [])
            return cursor

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
            VALUES {placeholders}
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

    def select(self, table_name, columns, criterias, order_by=None, group_by=None):
        placeholders = [f'{column} = ?' for column in criterias.keys()]
        select_creterias = ' AND '.join(placeholders)
        select_columns = ', '.join(columns)

        select_sql = f'''
            SELECT {select_columns} FROM {table_name}
            WHERE {select_creterias}
        '''

        if order_by:
            order_by_criteria = ' '.join([f'{column} {order_condition}' for column, order_condition in order_by.items()])
            select_sql += f'ORDER BY {order_by_criteria}'

        if group_by:
            group_by_criteria = ', '.join(group_by)
            select_sql += f'GROUP BY {group_by_criteria}'

        return self._execute(select_sql, select_creterias)
