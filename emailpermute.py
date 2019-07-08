# Original Author Kaleb Moore
# Edits by Janine Prukop
# Date last modified 4/17/2019

import csv
from tqdm import tqdm
import validateBundle
import time

startTime = time.perf_counter()

inFile = input("What file are we reading from? ") + '.csv'
outFile = "output_" + inFile

if __name__ == '__main__':

    with open(inFile, 'r') as in_file:
        readCSV = csv.reader(in_file, delimiter=',')
        em = -1
        fn = -1
        ln = -1
        header = next(readCSV)
        header.append('Final email')
        header.append('Email result')
        # print(header)
        for i in range(len(header)):
            if (header[i].lower() == 'email') | (header[i].lower() == 'e-mail'):
                em = i
                # print(em)
            elif (header[i].lower() == 'first name') | (header[i].lower() == 'first_name'):
                fn = i
                # print(fn)
            elif (header[i].lower() == 'last name') | (header[i].lower() == 'last_name'):
                ln = i
                # print(ln)
        if (em == -1) | (fn == -1) | (ln == -1):
            print("header incomplete or in wrong format")
            exit()

        with open(outFile, 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerows([header])
            for row in tqdm(readCSV, desc='Checking Emails'):
                output = row
                # print(row)
                print(output)
                if len(row) > 0:
                    first = row[fn]
                    last = row[ln]
                    email = row[em]
                    print(first, last, email)
                    result = list(validateBundle.permute(first, last, email))
                    if result[1] == 'Bad Email':
                        result = list(validateBundle.permute(first, last, email))
                        if result[1] == 'Bad Email':
                            result = list(validateBundle.permute(first, last, email))
                            if result[1] == 'Bad Email':
                                result[1] = "Hard bounce"
                            else:
                                result[1] = "Soft bounce"
                        else:
                            result[1] = "Soft bounce"
                    # print(result)
                    output.append(result[0])
                    output.append(result[1])
                    # print(output)
                    writer.writerows([output])
                else: break
        out_file.close()
    in_file.close()

endTime = time.perf_counter()
totalTime = endTime - startTime
# timeSecs = totalTime/1000000000
print("Time executed = %f seconds", totalTime)