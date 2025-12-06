import random, re
from faker import Faker

class BetterFakerSve:
    def __init__(self):
        self.fake = Faker('sv_SE')
    
    def name(self):
        """
        Normal faker name.
        
        Returns
        -------
        string
        """
        return self.fake.name()
    
    def email(self):
        """
        Normal faker email.
        
        Returns
        -------
        string
        """
        return self.fake.email()

    def __prepare_name_for_email(self, name):
        """
        Make name all lovercase, only have leters a-z and dots
        and splits it to first name and last name.
        
        Parameters
        ----------
        name : string
        Returns
        -------
        list ( string )
            List of fixed names in order
        """
        name = name.lower().replace('é', 'e').replace('å', 'a')
        name = name.replace('ä', 'a').replace('ö', 'o').replace('-', '.')
        
        # Replaces characters in name that are not spase, dot or letters
        for i in range(len(name)):
            if not re.search('[a-z. ]', name[i]):
                name.replace(name[i], 'x')
        
        names = name.split()
        
        return names

    def __create_local_part(self, name):
        """
        Turns name into lokal part of an email.\n
        Example: Karl Sjöström to karl1234,
        Anna Sjöberg Lövgren to anna.lovgren,
        or Jennifer Ahlgren-Ståhl to jahlgren.stahl.
        
        Parameters
        ----------
        name : string
        Returns
        -------
        string
        """
        names = self.__prepare_name_for_email(name)
        if len(names) > 1:
            local_type = random.randint(1, 7)
        else:
            return names[0] + str(random.randint(1, 9999))
        
        if local_type == 1:
            local_part = names[0] + str(random.randint(1, 9999))
        elif local_type == 2:
            local_part = names[-1] + str(random.randint(1, 9999))
        elif local_type == 3:
            local_part = names[0] + names[-1]
        elif local_type == 4:
            local_part = names[-1] + names[0]
        elif local_type == 5:
            local_part = names[0] + '.' + names[-1]
        elif local_type == 6:
            local_part = names[-1] + '.' + names[0]
        else:
            local_part = names[0][0] + names[-1]
        
        return local_part
    
    def match_email(self, name):
        """
        Creates diffrent test email adresses using name.\n
        Example: Karl Sjöström to karl1234@example.subdomain.com,
        Anna Sjöberg Lövgren to anna.lovgren@example.se,
        or Jennifer Ahlgren-Ståhl to jahlgren.stahl@example.net.
        
        Parameters
        ----------
        name : string
        Returns
        -------
        string
        """
        name = name.strip()
        if not name:
            return self.fake.email()
        
        local_part = self.__create_local_part(name)
        adress = local_part + '@example.'
        
        domain_type = random.randint(1, 11)
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
    
    def create_gdpr_safe_person(self):
        """
        Creates fake random people fore use in testing.
        
        Returns
        -------
        tuple ( string, string )
            A tuple where first value is an email and secound is a name
        """
        name = self.name()
        email = self.match_email(name)
        
        return email, name