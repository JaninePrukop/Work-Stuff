"""
# Original Author Kaleb Moore
# Edits by Janine Prukop
# Date last modified 7-15-2019

This program does not run on its own, it is required for emailcheck.py
"""

from validate_email import validate_email
import re
import time


def permute(first_name, last_name, domain):
    # Permutes potential email addresses
    # print(domain)
    emails = [first_name + '_' + last_name + domain, first_name + '.' + last_name + domain,
              last_name + '.' + first_name + domain, last_name + first_name + domain,
              last_name + '_' + first_name + domain, first_name + last_name + domain,
              first_name + '-' + last_name + domain, first_name[:1] + '.' + last_name + domain,
              first_name + last_name[:1] + domain, last_name + domain, first_name + '.' + last_name[:1] + domain,
              first_name[:1] + last_name + domain, first_name + domain, last_name[:1] + first_name + domain,
              first_name[:1] + '_' + last_name + domain, first_name + '_' + last_name[:1] + domain,
              last_name + first_name[:1] + domain, first_name[:1] + last_name[:1] + domain,
              last_name + '.' + first_name[:1] + domain, first_name[:1] + '.' + last_name[:1] + domain]
              # first_name[:1] + '.' + last_name[:1] + domain,
              # last_name[:1] + '_' + first_name + domain, last_name[:1] + '.' + first_name + domain,
              # last_name + '_' + first_name[:1] + domain, last_name + '-' + first_name + domain,
              # first_name[:1] + '-' + last_name[:1] + domain, first_name[:1] + '-' + last_name + domain,
              # last_name[:1] + '-' + first_name + domain, last_name + '-' + first_name[:1] + domain,
              # first_name + '-' + last_name[:1] + domain, last_name[:1] + first_name[:1] + domain,
              # first_name[:1] + '_' + last_name[:1] + domain,
              # last_name[:1] + '.' + first_name[:1] + domain, last_name[:1] + '-' + first_name[:1] + domain,
              # last_name[:1] + '_' + first_name[:1] + domain
    # print(emails)
    # try:
    for i in range(0, len(emails)):
        try:
            temp = validate_email(emails[i], verify=True)
        except:
            temp = 'error'
        if temp is True:
            time.sleep(1)
            return emails[i], 'Good Email'
    return 'ERROR', 'No Valid Email Found'

    '''
    if validate_email(domain, check_mx=True, smtp_timeout=10) is True:
        for i in range(0, len(emails)):
            time.sleep(1)
            if validate_email(emails[i], verify=True) is True:
                time.sleep(1)
                return emails[i], 'Good Email'
    return 'No Valid Email', 'No Valid Email'
    '''
    # except:
    #     return 'error', 'could not permute'


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

    splitEmail = email.split("@")
    domain = splitEmail[-1]
    junkemail = "askdjh23@" + domain
    # print(junkemail)

    try: verify = validate_email(junkemail, verify=True)
    except:
        results = 'timeout'
    if verify is True:
        results = 'Maybe'
    else:

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
    # vprint(email)
    # print(results)
    valid = zip([str(email)], [str(results)])
    valid = set(valid)
    # print(valid)
    return valid



