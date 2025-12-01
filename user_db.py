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
        """
        Returns a list with all information off all curently saved users.
        
        Returns
        -------
        list ( Tuple ( id, email, name ) )
        """
        self.__cursor.execute('SELECT * FROM users')
        result = self.__cursor.fetchall()
        
        return result
    
    def print_all_users(self):
        """
        Prints id, email and name off all curently saved users.
        """
        users = self.get_users()
        print('\nCurrent users in database')
        
        for user in users:
            print(f'ID: {user[0]}, email: {user[1]}, name: {user[2]}.')
    
    def users_in_db(self):
        """
        Returns how many users are curently saved in database.
        
        Returns
        -------
        integer
            The number of curently saved users.
        """
        self.__cursor.execute('SELECT COUNT(*) FROM users')
        result = self.__cursor.fetchone()[0]
        
        return result
    
    def find_by_column_name(self, column_name, serch_term, exakt=False):
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
        Returns
        -------
        list ( Tuple ( id, email, name ) )
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
        """
        Insert a new user into the database.
        
        Parameters
        ----------
        costumer_info : tuple ( string, string )
            Tuple whith two strings. First is email and second is name.
        """
        insert_statment = f'INSERT INTO {self.__table}(email, name) '
        insert_statment += 'VALUES(?,?)'
        
        self.__cursor.execute(insert_statment, costumer_info)
        self.__conn.commit()
    
    def del_user(self, id):
        """
        removes a user from database.
        
        Parameters
        ----------
        id : integer
            The id off the user that should be removed
        """
        self.__cursor.execute(f'DELETE FROM {self.__table} WHERE id = {id}')
        self.__conn.commit()
        
    def __del__(self):
        #print(f'Closing connection to {self.__table}.')
        self.__conn.close()