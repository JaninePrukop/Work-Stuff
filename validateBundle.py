# Original Author Kaleb Moore
# Edits by Janine Prukop
# Date last modified 4/17/2019

from tqdm import tqdm
from validate_email import validate_email
import re
import time


def permute(first_name, last_name, email):
    # Permutes potential email addresses
    regex_pattern = r'^\S+(@{1}\w+\.\w+.+)'
    domain = (str(re.findall(regex_pattern, email)).lower()).strip("[ ' ] '")
    emails = (email, first_name[:1] + last_name + domain, first_name + '.' + last_name + domain,
              first_name + last_name + domain, first_name + domain, first_name[:1] + '.' + last_name + domain,
              first_name + last_name[:1] + domain, last_name + domain, first_name + '.' + last_name[:1] + domain,
              first_name + '_' + last_name + domain,
              last_name + '.' + first_name + domain, last_name + first_name + domain,
              first_name[:1] + '_' + last_name + domain, first_name + '_' + last_name[:1] + domain,
              first_name + '-' + last_name + domain, last_name + '_' + first_name + domain,
              last_name + first_name[:1] + domain, first_name[:1] + last_name[:1] + domain,
              last_name[:1] + first_name + domain, last_name + '.' + first_name[:1] + domain)
              # first_name[:1] + '.' + last_name[:1] + domain,
              # last_name[:1] + '_' + first_name + domain, last_name[:1] + '.' + first_name + domain,
              # last_name + '_' + first_name[:1] + domain, last_name + '-' + first_name + domain,
              # first_name[:1] + '-' + last_name[:1] + domain, first_name[:1] + '-' + last_name + domain,
              # last_name[:1] + '-' + first_name + domain, last_name + '-' + first_name[:1] + domain,
              # first_name + '-' + last_name[:1] + domain, last_name[:1] + first_name[:1] + domain,
              # first_name[:1] + '_' + last_name[:1] + domain,
              # last_name[:1] + '.' + first_name[:1] + domain, last_name[:1] + '-' + first_name[:1] + domain,
              # last_name[:1] + '_' + first_name[:1] + domain

    if validate_email(email, check_mx=True, smtp_timeout=10) is True:
        for i in tqdm(range(0, len(emails)), desc='Permutations'):
            if validate_email(emails[i], verify=True) is True:
                time.sleep(1)
                return emails[i], 'Good Email'
    return email, 'No Valid Email'


def validatep(first_name, last_name, emails):
    email = emails.strip('"').strip("\n").strip('"')
    try:
        verify = validate_email(email, verify=True)
        if verify is True:
            results = 'Good Email'
        else:
            email, results = permute(first_name.lower(), last_name.lower(), email)
    except:
        results = 'Timeout'
    valid = zip([str(email)], [str(results)])
    valid = set(valid)
    return valid


def validate(emails):
    verify = False
    email = emails.strip('"').strip("\n").strip('"')
    '''
    splitEmail = email.split("@")
    domain = splitEmail[-1]
    junkemail = "askdjh23@" + domain
    print(junkemail)
    
    try: verify = validate_email(junkemail, verify=True)
    except:
        results = 'timeout'
    if verify is True:
        results = 'Maybe'
    else:
    '''

    if len(email) == 0:
        results = 'No email provided'
    else:
        try:
            verify = validate_email(email, verify=True)
        except:
            results = 'timeout'
        if verify is True:
            results = 'Good Email'
        else:
            results = 'Bad Email'

    valid = zip([str(email)], [str(results)])
    valid = set(valid)
    return valid



