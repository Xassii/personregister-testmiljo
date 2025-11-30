import sqlite3

class UserDB:
    """
    Handles user database tables.\n
    Tables have columns id, email and name.
    """
    def __init__(self, db_name, table_name):
        self.__table = table_name
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        
        create_statement = f'CREATE TABLE IF NOT EXISTS {table_name}'
        self.__cursor.execute(create_statement + """ (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              email STRING NOT NULL,
                              name STRING NOT NULL
                              )""")
        self.__conn.commit()
        #print(f'Created {table_name} in {db_name}.')
    
    def get_users(self):
        self.__cursor.execute('SELECT * FROM users')
        result = self.__cursor.fetchall()
        
        return result
    
    def find_by_column_name(self, column_name, serch_term, exakt=False):
        """
        column_name : string
        serch_term : string
        exakt : bool, standard value False.
            If True does exact string comparison.
        Serch any column for a value. Case insensitive.
        """
        result = []
        select_statment = f'SELECT * FROM {self.__table} WHERE '
        if exakt:
            select_statment += f'{column_name} LIKE "{serch_term}"'
        else:
            select_statment += f'{column_name} LIKE "%{serch_term}%"'
        
        try:
            self.__cursor.execute(select_statment)
            result = self.__cursor.fetchall()
        except sqlite3.OperationalError:
            print(f'Column "{column_name}" not in table {self.__table}')
        
        return result
    
    def add_user(self, costumer_info):
        insert_statment = f'INSERT INTO {self.__table}(email, name) '
        insert_statment += 'VALUES(?,?)'
        
        self.__cursor.execute(insert_statment, costumer_info)
        self.__conn.commit()
    
    def del_user(self, id):
        self.__cursor.execute(f'DELETE FROM {self.__table} WHERE id = {id}')
        self.__conn.commit()
        
    def __del__(self):
        #print(f'Closing connection to {self.__table}.')
        self.__conn.close()