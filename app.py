from user_db import UserDB
from better_faker_sve import BetterFakerSve


def main():
    """
    Connects to database, checks if there is 100 users in it and 
    creates 100 test users if not.
    """
    test_db = UserDB('data/test_users.db', 'users')
    users_in_db = test_db.users_in_db()
    
    if users_in_db == 100:
        print('Database allredy have users.')
        return None
    
    if users_in_db > 100:
        text = 'Too many users in database. '
        text += 'Clearing and creating new testusers.'
        
        print(text)
        test_db.clear_table()
    
    if users_in_db > 0 and users_in_db < 100:
        text = 'Too few users in database. '
        text += 'Clearing and creating new testusers.'
        
        print(text)
        test_db.clear_table()
    
    fake = BetterFakerSve()
    users = []
    
    for _ in range(100):
        users.append(fake.create_gdpr_safe_person())
    
    test_db.add_users(users)


if __name__ == '__main__':
    main()