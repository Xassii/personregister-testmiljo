import pytest
from user_db import UserDB

class TestUserDB:
    @pytest.fixture
    def create_database(self):
        self.users = [('amanda.amandasdotter@example.se',
                       'Amanda Amandasdotter'),
                       ('bbengtsson@example.com', 'Bengt Bengtsson')]
        self.num_users = len(self.users)
        
        db = UserDB('data/test_users.db', 'unittests')
        db.add_users(self.users)
        
        yield db
        
        db.clear_table()
    
    def test_initialising_db_wrong_filename(self):
        with pytest.raises(ValueError):
            UserDB('', 'unittests')
            UserDB('        ', 'unittests')
            UserDB('.db', 'unittests')
            UserDB('        .db', 'unittests')
            UserDB('data/test_usersdb', 'unittests')
            UserDB('data/test_users_db', 'unittests')
    
    def test_initialising_db_no_tablename(self):
        with pytest.raises(ValueError):
            UserDB('data/test_users.db', '')
    
    def test_get_users(self, create_database):
        users = create_database.get_users()
        
        assert len(users) == self.num_users
        assert users[0][1] == self.users[0][0]
        assert users[0][2] == self.users[0][1]
        assert users[1][1] == self.users[1][0]
        assert users[1][2] == self.users[1][1]
    
    def test_users_in_db(self, create_database):
        len_users = len(create_database.get_users())
        num_users = create_database.db_len()
        
        assert num_users == self.num_users
        assert len_users == num_users
    
    def test_find_by_column_name(self, create_database):
        assert not create_database.find_by_column_name('id', 'a')
        
        user = create_database.find_by_column_name('NAME', 'a a')
        assert user[0][2] == self.users[0][1]
        
        user = create_database.find_by_column_name('name', 'TS')
        assert user[0][2] == self.users[1][1]
        
        user = create_database.find_by_column_name('EmaIl', 'E.C')
        assert user[0][1] == self.users[1][0]
    
    def test_find_by_column_name_exakt(self, create_database):
        assert not create_database.find_by_column_name('id', 0, True)
        assert not create_database.find_by_column_name('name', 'a a', True)
        assert not create_database.find_by_column_name('name', 'TS', True)
        
        values = ('nAme', 'AMANDA amandasdotter', True)
        user = create_database.find_by_column_name(*values)
        assert user[0][2] == self.users[0][1]
        
        values = ('namE', 'bengt BENGTSSON', True)
        user = create_database.find_by_column_name(*values)
        assert user[0][2] == self.users[1][1]
    
    def test_find_by_column_name_column_dont_exist(self, create_database):
        assert not create_database.find_by_column_name('', 'a')
        assert not create_database.find_by_column_name('finsej', 'a')
        assert not create_database.find_by_column_name(100, 'a')
        assert not create_database.find_by_column_name([], 'a')
    
    def test_find_by_column_name_empty_search(self, create_database):
        users = create_database.find_by_column_name('name', '')
        
        assert len(users) == self.num_users
        assert not create_database.find_by_column_name('name', '', True)
    
    def test_add_users(self, create_database):
        start_users = create_database.get_users()
        start_num_users = create_database.users_in_db()
        
        create_database.add_users([('carro23@example.net',
                                    'Carro Carrosdotter')])
        users = create_database.get_users()
        num_users = create_database.users_in_db()
        
        assert num_users == start_num_users + 1
        assert len(users) == num_users
        assert users[0] == start_users[0]
        assert users[1] == start_users[1]
        assert users[-1][1] == 'carro23@example.net'
        assert users[-1][2] == 'Carro Carrosdotter'
    
    def test_add_users_empty_list(self, create_database):
        start_users = create_database.get_users()
        start_num_users = create_database.users_in_db()
        
        create_database.add_users([])
        users = create_database.get_users()
        num_users = create_database.users_in_db()
        
        assert num_users == start_num_users
        assert len(users) == num_users
        assert users[0] == start_users[0]
        assert users[1] == start_users[1]
    
    def test_add_users_empty_strings(self, create_database):
        with pytest.raises(ValueError):
            create_database.add_users([('carro23@example.net', '')])
            create_database.add_users([('', 'Carro Carrosdotter')])
        
        assert create_database.users_in_db() == self.num_users
    
    def test_del_user(self, create_database):
        id = create_database.find_by_column_name('name', 'Amanda')[0][0]
        create_database.del_user(id)
        
        users = create_database.get_users()
        num_users = create_database.users_in_db()
        
        assert num_users == self.num_users - 1
        assert len(users) == num_users
        assert users[0][1] == self.users[1][0]
        assert users[0][2] == self.users[1][1]
    
    def test_del_user_too_small_id(self, create_database):
        with pytest.raises(ValueError):
            create_database.del_user(set())
            create_database.del_user(tuple())
            create_database.del_user({})
            create_database.del_user([])
            create_database.del_user('')
            create_database.del_user('0')
            create_database.del_user('-1')
            create_database.del_user(0)
            create_database.del_user(-1)
    
    def test_clear_table(self, create_database):
        create_database.clear_table()
        
        assert len(create_database.get_users()) == 0
        assert create_database.users_in_db() == 0