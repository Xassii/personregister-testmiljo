import time
from user_db import UserDB
from better_faker_sve import BetterFakerSve


def gdpr_validate_test_user_db(user_db, user_table, num_users):#TODO
    db = UserDB(user_db, user_table)
    
    current_users = db.users_in_db()
    text = f'Found {current_users} in testuser database, expected {num_users}!'
    assert current_users == num_users, text
    
    wrong_email = db.find_by_column_name('email', '@example.', invert=True)
    wrong_email = len(wrong_email)
    text = f"Found {wrong_email} testusers that don't have testemails!"
    assert wrong_email == 0, text


def create_annon_db(user_db, user_table, annon_db, annon_table):#TODO
    #TODO ask teacher
    user_db = UserDB(user_db, user_table)
    annon_db = UserDB(annon_db, annon_table)
    
    num_org_users = user_db.users_in_db()
    annon_users = []
    
    for i in range(num_org_users):
        annon_email = f'anonym.anvandare{i}@example.com'
        annon_users.append((annon_email, f'Anonym Användare{i}'))
    
    annon_db.add_users(annon_users)


def determen_and_print_message(users_in_db, num_users):
    if users_in_db > num_users:
        text = 'Too many users in database. '
        text += 'Clearing and creating new testusers...'
    elif users_in_db > 0 and users_in_db < num_users:
        text = 'Too few users in database. '
        text += 'Clearing and creating new testusers...'
    elif users_in_db == 0:
        text = 'Creating testusers...'
    else:
        text = 'Testdatabase have an incorrect value. '
        text += 'Clearing and creating new testusers...'
    
    print(text)


def create_fake_db(user_db, user_table, num_users):
    """
    Connects to database, checks if there is the correct amount of users
    in it and creates the test users if not.
    """#TODO Uppdate dockstring
    db = UserDB(user_db, user_table)
    users_in_db = db.users_in_db()
    wrong_email = db.count_in_collumn('email', '@example.', invert=True)
    no_email = db.count_in_collumn('email', 'None')
    no_name = db.count_in_collumn('name', 'None')
    
    validate = users_in_db == num_users and not wrong_email
    validate = validate and not no_email and not no_name
    if validate:
        print('Database allredy have users.')
        return None
    
    determen_and_print_message(users_in_db, num_users)
    db.clear_table()
    fake = BetterFakerSve()
    users = []
    
    for _ in range(num_users):
        users.append(fake.create_gdpr_safe_person())
    
    db.add_users(users)
    print('Fake testusers created successfully!')


def main():
    create_fake_db('data/test_users.db', 'users', 100)
    create_annon_db('data/test_users.db', 'users',
                    'data/test_users.db', 'annonusers')
    
    # Keep the container running for testing
    print("\nContainer is running. Press Ctrl+C to exit.")
    try:
        while True:
            gdpr_validate_test_user_db('data/test_users.db', 'users', 100)
            print('Database validated.')
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == '__main__':
    main()