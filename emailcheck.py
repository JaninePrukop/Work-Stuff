# Original Author Kaleb Moore
# Edits by Janine Prukop
# Date last modified 4/17/2019

import csv
from tqdm import tqdm
import validateBundle
import os

inFile = "temp"


if __name__ == '__main__':
    directory = os.listdir()
    print(directory)
    for i in range(len(directory)):
        if directory[i].startswith("Output"):
            continue
        elif directory[i].endswith('csv'):
            inFile = directory[i]
        else: continue
        outFile = "Output_" + inFile
        with open(inFile, 'r') as in_file:
            readCSV = csv.reader(in_file, delimiter=',')
            em = -1
            fn = -1
            ln = -1
            header = next(readCSV)
            header.append('Email result')
            # print(header)
            for i in range(len(header)):
                # print(header[i].lower())
                if (header[i].lower() == 'email') | (header[i].lower() == 'e-mail'):
                    em = i
                    # print(em)
                elif (header[i].lower() == 'first name') | (header[i].lower() == 'first_name') | (header[i].strip().lower == 'first'):
                    fn = i
                    # print(fn)
                elif (header[i].lower() == 'last name') | (header[i].lower() == 'last_name') | (header[i].strip().lower == 'last'):
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
                    # print(output)
                    if len(row) > 0:
                        # first = row[fn]
                        # last = row[ln]
                        email = row[em]
                        result = list(validateBundle.validate(email))
                        # print(result)
                        output.append(result[0][1])
                        # print(output)
                        writer.writerows([output])
                    else: break
            out_file.close()
    in_file.close()
