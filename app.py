from user_db import UserDB
from better_faker_sve import BetterFakerSve


def create_test_users(db, num_users):
    """
    Creates random testusers with name and email and adds them to the
    database table
    
    Parameters
    ----------
    db : UserDB instance
        The database table to add the users to
    num_users : integer
        Number off users to create
    """
    fake = BetterFakerSve()
    users = []
    
    for _ in range(num_users):
        users.append(fake.create_gdpr_safe_person())
    
    db.add_users(users)


def do_db_tests(db):
    """
    Test the UserDB instance methods 
    
    Parameters
    ----------
    db : UserDB instance
        The database table to do the tests on
    """
    print('\nCurrent users in database')
    db.print_all_users()
    
    user = db.find_by_column_name('name', 'nda ama')
    print('\nFound user Amanda Amandasdotter:')
    print(user)
    
    db.del_user(int(user[0][0]))
    print('\nUsers in database after deleting Amanda Amandasdotter:')
    db.print_all_users()
    
    print("\nTrying too search column ssn that don't exist:")
    db.find_by_column_name('ssn', '202501012385')


def main():
    """
    Connects to database, creates test users, tests database table
    and emptys database table.
    """
    print('\nCreating testusers...')
    test_db = UserDB('data/test_users.db', 'users')
    users_in_db = test_db.users_in_db()
    random_users = 2
    specifik_test_users = [('amanda.amandasdotter@example.se',
                            'Amanda Amandasdotter'),
                            ('bbengtsson@example.com', 'Bengt Bengtsson')]
    
    if random_users and not users_in_db:
        create_test_users(test_db, random_users)
    elif random_users and users_in_db:
        print('Database had data. Clearing and creating test users.')
        test_db.clear_table()
        create_test_users(test_db, random_users)
    elif users_in_db:
        print('Database had data. Clearing and creating test users.')
        test_db.clear_table()
    
    test_db.add_users(specifik_test_users)
    print('Testusers created')
    
    do_db_tests(test_db)
    
    print('\nClearing table...')
    test_db.clear_table()
    print('Table cleared off all users\n')


if __name__ == '__main__':
    main()