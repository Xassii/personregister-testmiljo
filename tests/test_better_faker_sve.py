import pytest, re
from better_faker_sve import BetterFakerSve

class TestBetterFakerSve:
    def test_name(self):
        fake = BetterFakerSve()
        name = fake.name()
        
        assert len(name) > 4
        assert ' ' in name
        assert not re.search('[^-a-zA-ZéÉåÅäÄöÖ ]', name)
    
    def test_email(self):
        fake = BetterFakerSve()
        email = fake.email()
        
        assert len(email) > 14
        assert re.search('^[-0-9a-z.]+@example.((com)|(net)|(org))$', email)
    
    def test_match_email(self):
        fake = BetterFakerSve()
        email = fake.match_email('A B')
        email_start, email_end = email.split('@')
        
        email_pattern = '^example.((com)|(net)|(org)|(nu)|'
        email_pattern += '(se)|(subdomain.com))$'
        
        assert len(email) > 12
        assert re.search(email_pattern, email_end)
        if email_start[-1].isdigit():
            assert re.search('^(a|b)[0-9]+$', email_start)
        else:
            assert email_start in ['ab', 'ba', 'a.b', 'b.a']
    
    def test_match_email_no_name(self):
        fake = BetterFakerSve()
        
        email = fake.match_email('')
        assert re.search('^[-0-9a-z.]+@example.((com)|(net)|(org))$', email)
        
        email = fake.match_email(' \n\t\n  \n')
        assert re.search('^[-0-9a-z.]+@example.((com)|(net)|(org))$', email)
    
    def test_match_email_no_space(self):
        fake = BetterFakerSve()
        email = fake.match_email('a')
        
        email_pattern = '^a[0-9]+@example.((com)|(net)|(org)|'
        email_pattern += '(nu)|(se)|(subdomain.com))$'
        assert re.search(email_pattern, email)
    
    def test_match_email_special_characters(self):
        fake = BetterFakerSve()
        email = fake.match_email('019¨^*<!@#/]&§½"\t®中文')
        
        email_pattern = '^x{20}[0-9]+@example.((com)|(net)|(org)|'
        email_pattern += '(nu)|(se)|(subdomain.com))$'
    
    def test_create_gdpr_safe_person(self):
        fake = BetterFakerSve()
        person = fake.create_gdpr_safe_person()
        email_start, email_end = person[0].split('@')
        
        email_pattern = '^example.((com)|(net)|(org)|(nu)|'
        email_pattern += '(se)|(subdomain.com))$'
        
        assert re.search(email_pattern, email_end)
        assert re.search('^[0-9a-z.]+$', email_start)