from user_db import UserDB

if __name__ == '__main__':
    test_db = UserDB('test_users.db', 'users')
    test_db.add_user(('amanda.amandasdotter@test.com', 'Amanda Amandasdotter'))
    test_db.add_user(('bengt.bengtsson@test.com', 'Bengt Begntsson'))
    
    test_db.print_all_users()
    
    user_amanda = test_db.find_by_column_name('name', 'nda a')
    print(user_amanda)
    
    test_db.del_user(user_amanda[0][0])
    all_users = test_db.get_users()
    print(all_users)
    
    test_db.find_by_column_name('ssn', '202501012385')