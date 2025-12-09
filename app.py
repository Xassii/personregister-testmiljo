import time
from user_db import UserDB
from better_faker_sve import BetterFakerSve


def gdpr_validate_test_user_db(user_db, user_table, num_users):
    """
    Validates that the correct number of users are in the database
    and that the emails have '@example.' in them.
    
    Parameters
    ----------
    user_db: string
        Name of database file with user_table in
    user_table: string
        Name of table to validate
    num_users: intiger
        Nummber of users that should be in database
    """
    db = UserDB(user_db, user_table)
    
    current_users = db.users_in_db()
    text = f'Found {current_users} in testuser database, expected {num_users}!'
    assert current_users == num_users, text
    
    wrong_email = db.find_by_column_name('email', '@example.', invert=True)
    wrong_email = len(wrong_email)
    text = f"Found {wrong_email} testusers that don't have testemails!"
    assert wrong_email == 0, text


def create_anon_db(user_db, user_table, anon_db, anon_table):
    """
    Anonymises users from user_table and saves the anonymised
    users in anon_table.
    
    Parameters
    ----------
    user_db: string
        Name of database file with user_table in
    user_table: string
        Name of table with users to anonymize
    anon_db: string
        Name of database file to save new anonymized users in
    anon_table: string
        Name of table to save new anonymized users in
    """
    user_db = UserDB(user_db, user_table)
    anon_db = UserDB(anon_db, anon_table)
    
    org_users = user_db.get_users()
    anon_users = []
    
    for i, user in enumerate(org_users):
        anon_email = f'anonym.anvandare{i}@example.com'
        anon_name = f'Anonym Användare{i}'
        other_info = user[2:]
        anon_users.append((anon_email, anon_name, *other_info))
    
    anon_db.add_users(anon_users)


def determen_and_print_message(users_in_db, num_users):
    """
    Prints diffrent messages depending on how users_in_db
    and num_users compare.
    
    Parameters
    ----------
    users_in_db: intiger
        Users currently in database
    num_users: intiger
        Nummber of users that should be in database
    """
    if users_in_db > num_users:
        text = '\nToo many users in database. '
        text += 'Clearing and creating new testusers...'
    elif users_in_db > 0 and users_in_db < num_users:
        text = '\nToo few users in database. '
        text += 'Clearing and creating new testusers...'
    elif users_in_db == 0:
        text = '\nCreating testusers...'
    else:
        text = '\nTestdatabase have an incorrect value. '
        text += 'Clearing and creating new testusers...'
    
    print(text)


def create_fake_db(user_db, user_table, num_users):
    """
    Connects to database, checks if there is the correct amount of users
    in it whith fake emails. If not, clears the database and creates new
    test users.
    
    Parameters
    ----------
    user_db : string
        Name of database file.
    user_table : string
        Name of table in database.
    num_users : intiger
        How many users that should be in the database
    """
    db = UserDB(user_db, user_table)
    users_in_db = db.users_in_db()
    wrong_email = db.find_by_column_name('email', '@example.', invert=True)
    
    if users_in_db == num_users and not wrong_email:
        print('\nDatabase allredy have users.')
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
    """
    Creates in database test_users fake users in table users and
    anonymived users in table anonusers.\nAfter checks that data in
    table users don't get changed every ten seconds. If data has been
    changed the user table is recreated.
    """
    create_fake_db('data/test_users.db', 'users', 100)
    create_anon_db('data/test_users.db', 'users',
                    'data/test_users.db', 'anonusers')
    
    # Keep the container running for testing
    try:
        while True:
            gdpr_validate_test_user_db('data/test_users.db', 'users', 100)
            print('Database validated.')
            time.sleep(10)
    except AssertionError:
        print("\nDatabase validation failed!")
        create_fake_db('data/test_users.db', 'users', 100)


if __name__ == '__main__':
    main()