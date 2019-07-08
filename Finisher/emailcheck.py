# Author Janine Prukop
# Date last modified 7/2/2019


from tqdm import tqdm
import validateBundle
import random
import time


def checker(emails, runs):
    results = list(str(' ') * len(emails))
    # print(len(emails))
    index = random.sample(range(len(emails)), len(emails))
    count = 0
    while count < runs:
        print(count)
        result = ['']
        result[0] = ('error, line 52', 'error, line 52')
        newIndex = []
        for i in tqdm(index, desc='Checking Emails'):
            output = []
            output.append(emails[i])
            result[0] = ('error, line 51', 'error, line 51')
            if len(emails[i]) > 0:
                email = emails[i]
                result = list(validateBundle.validate(email))
                if result[0][1] == 'Bad Email':
                    newIndex.append(i)
                else:
                    if count == 0:
                        results[i] = result[0][1]
                    else:
                        results[i] = 'Soft Bounce'
                time.sleep(.5)
            else:
                results[i] = 'No email provided'
        index = newIndex
        count += 1
    if len(index) > 0:
        for num in index:
            output[0] = emails[num]
            results[num] = 'Hard Bounce'
    return results
