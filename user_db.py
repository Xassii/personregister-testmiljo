import sqlite3

class UserDB:
    def __init__(self, db_name, table_name):
        """
        Handles user database tables. Tables have columns id, email and name.
        
        Parameters
        ----------
        db_name : string
            Name of database file.
        table_name : string
            Name of table in database.
        """
        db_name = db_name.strip()
        table_name = table_name.strip()
        self.__conn = None
        
        if len(db_name) < 4:
            raise ValueError('Variable db_name is too short/empty')
        if len(table_name) < 1:
            raise ValueError('Variabe table_name is empty')
        if not db_name[-3:] == '.db':
            raise ValueError("Variable db_name don't end in .db")
        
        self.__db_name = db_name
        self.__table = table_name
        self.__conn = sqlite3.connect(self.__db_name)
        self.__cursor = self.__conn.cursor()
        
        create_statement = f'CREATE TABLE IF NOT EXISTS {self.__table}'
        self.__cursor.execute(create_statement + """ (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email STRING NOT NULL,
                            name STRING NOT NULL
                            )""")
        self.__conn.commit()
        #print(f'Opend {table_name} in {db_name}.')
    
    def get_users(self):
        """
        Returns a list with all information off all curently saved users.
        
        Returns
        -------
        list ( Tuple ( id, email, name ) )
        """
        self.__cursor.execute(f'SELECT * FROM {self.__table}')
        result = self.__cursor.fetchall()
        
        return result
    
    def print_all_users(self):
        """
        Prints id, email and name off all curently saved users.
        """
        users = self.get_users()
        
        for user in users:
            print(f'- ID: {user[0]}, email: {user[1]}, name: {user[2]}')
    
    def db_len(self):
        """
        Returns how many users are curently saved in database.
        
        Returns
        -------
        integer
            The number of curently saved users.
        """
        self.__cursor.execute(f'SELECT COUNT(*) FROM {self.__table}')
        result = self.__cursor.fetchone()[0]
        
        return result
    
    def find_by_column_name(self, column_name, serch_term,
                            exakt=False, invert=False):
        """
        Serch any column for a value. Case insensitive.
        
        Parameters
        ----------
        column_name : string
            Wich colomn you whant to search.
        serch_term : string
            What you whant to find.
        exakt : bool, standard value False.
            If True does exact string comparison.
        invert : bool, standard value False.
            If True returns values that don't match the search term.
        Returns
        -------
        list ( Tuple ( id, email, name ) )
        """
        result = []
        select_statment = f'SELECT * FROM {self.__table} WHERE '
        select_statment += f'{column_name} '
        
        if invert:
            select_statment += 'NOT '
        
        if exakt:
            select_statment += f'LIKE "{serch_term}"'
        else:
            select_statment += f'LIKE "%{serch_term}%"'
        
        try:
            self.__cursor.execute(select_statment)
            result = self.__cursor.fetchall()
        except sqlite3.OperationalError as e:
            if str(e) == f'no such column: {column_name}':
                print(f'Column "{column_name}" not in table {self.__table}')
            else:
                text = 'An error occurred when trying to find value in '
                text += f'database: {e}'
                print(text)
        
        return result
    
    def add_users(self, custumer_info):
        """
        Insert new users into the database.
        
        Parameters
        ----------
        custumer_info : Iterable ( tuple ( string, string ) )
            An iterable off tuples whith two strings. 
            First string is email and second is name.
        """
        if not custumer_info:
            return None
        
        for customer in custumer_info:
            if not customer[0] or not customer[1]:
                raise ValueError("Can't add empty values to user database.")
        
        insert_statment = f'INSERT INTO {self.__table}(email, name) '
        insert_statment += 'VALUES(?,?)'
        
        self.__cursor.executemany(insert_statment, custumer_info)
        self.__conn.commit()
    
    def del_user(self, id):
        """
        removes a user from database.
        
        Parameters
        ----------
        id : integer
            The id off the user that should be removed
        """
        if not id or int(id) <= 0:
            text = 'Id to delete user from table must be a positive integer.'
            raise ValueError(text)
        
        try:
            self.__cursor.execute(f'DELETE FROM {self.__table} WHERE id = {id}')
            self.__conn.commit()
        except sqlite3.OperationalError as e:
            print(f'An error occured when trying to delete user {id}: {e}')
    
    def clear_table(self):
        """
        Deletes all data from table.
        """
        self.__cursor.execute(f'DELETE FROM {self.__table}')
        self.__conn.commit()
    
    def __del__(self):
        #print(f'Closing connection to {self.__table}.')
        if self.__conn:
            self.__conn.close()