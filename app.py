import random
from user_db import UserDB
from faker import Faker

def match_email(f_name, l_name):
    """
    Creates diffrent test email adresses using first and last name
    
    Parameters
    ----------
    f_name : string
    l_name : string
    Returns
    -------
    string
    """
    f_name = f_name.lower()
    l_name = l_name.lower()
    local_type = random.randint(1, 7)
    domain_type = random.randint(1, 11)
    adress = '@example.'
    
    if local_type == 1:
        adress = f_name + str(random.randint(1, 9999)) + adress
    elif local_type == 2:
        adress = l_name + str(random.randint(1, 9999)) + adress
    elif local_type == 3:
        adress = f_name + l_name + adress
    elif local_type == 4:
        adress = l_name + f_name + adress
    elif local_type == 5:
        adress = f_name + '.' + l_name + adress
    elif local_type == 6:
        adress = l_name + '.' + f_name + adress
    else:
        adress = f_name[0] + l_name + adress
    
    if domain_type == 1:
        adress += 'org'
    elif domain_type == 2:
        adress += 'net'
    elif domain_type == 3:
        adress += 'subdomain.com'
    elif domain_type <= 5:
        adress += 'nu'
    elif domain_type <= 8:
        adress += 'com'
    else:
        adress += 'se'
    
    return adress


def create_test_users(db, num_users):
    """
    Creates random testusers with name and email and adds them to the database
    
    Parameters
    ----------
    db : UserDB instance
        The database to add the users to
    num_users : integer
        Number off users to create
    """
    f = Faker()
    users = []
    
    for _ in range(num_users):
        f_name = f.first_name()
        l_name = f.last_name()
        if random.randint(0, 9):
            email = match_email(f_name, l_name)
        else:
            email = f.email()
        users.append((email, f_name + ' ' + l_name))
    
    db.add_users(users)


def do_db_tests(db):
    """
    Test the UserDB instance methods 
    
    Parameters
    ----------
    db : UserDB instance
        The database to add the users to
    """
    db.print_all_users()
    
    user = db.find_by_column_name('name', 'nda ama')
    print(user)
    
    db.find_by_column_name('ssn', '202501012385')


def main():
    """
    Connects to database, creates test users, tests database 
    and emptys database.
    """
    test_db = UserDB('data/test_users.db', 'users')
    users_in_db = test_db.users_in_db()
    random_users = 0
    specifik_test_users = [('amanda.amandasdotter@example.se',
                            'Amanda Amandasdotter'),
                            ('bbengtsson@example.com', 'Bengt Bengtsson')]
    
    if random_users and not users_in_db:
        create_test_users(test_db, random_users)
    elif random_users and users_in_db:
        print('Database had data. Clearing and creating test users.')
        test_db.clear_table()
        create_test_users(test_db)
    elif users_in_db:
        print('Database had data. Clearing and creating test users.')
        test_db.clear_table()
    
    test_db.add_users(specifik_test_users)
    print('Testusers created.')
    
    do_db_tests(test_db)
    test_db.clear_table()


if __name__ == '__main__':
    main()