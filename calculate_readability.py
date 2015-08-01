import sys
import os
import codecs
from glob import iglob
import csv
import string
from readcalc import readcalc

## ========================================= ##
## ---------------Main---------------------- ##
## ========================================= ##

if len(sys.argv) <= 2:
    print "USAGE: python calculate_readability.py [-f] <PATH_TO_DATA> <OUT_CSV_FILE>"
    sys.exit(0)
#Continuos is used to define if the LONG or SHORT variant should be generated
continuos = False

path_to_data = sys.argv[1]
outfile = sys.argv[2]

if path_to_data == "-f":
    files = [outfile]
    outfile = sys.argv[3]
else:
    #files = iglob(path_to_data + "/part*/*")
    files = iglob(path_to_data + "/*")

def get_list_of_readability(calc):
    return [calc.get_flesch_reading_ease(), calc.get_flesch_kincaid_grade_level(), calc.get_coleman_liau_index(),\
            calc.get_gunning_fog_index(), calc.get_smog_index(), calc.get_ari_index(), calc.get_lix_index(),\
            calc.get_dale_chall_score()]

appendMode = False
#check if file exists:
if not os.path.isfile(outfile):
    csv_file = open(outfile, 'wb')
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["filename", "part", "flesch_reading_ease", "flesch_kincaid_grade_level", "coleman_liau_index",\
                     "gunning_fog_index", "smog_index", "ari_index", "lix_index", "dale_chall_score","perc","loga"])

#if file exists, find the last register there:
else:
    appendMode = True
    with open(outfile, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        lastline = reader.next()
        for line in reader:
            lastline = line
    csv_file = open(outfile, 'ab')
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

for filename in files:
    with codecs.open(filename, encoding="utf-8", mode="r") as f: # read the file in unicode mode
    #with open(filename, mode="r") as f:
        rows = []
        lines = f.readlines()

        if appendMode:
            if lines[0].strip() == lastline[0]:
                appendMode = False
                print "Found last register....."
            continue

        print "Processing", filename
        filepath = lines[2]
        ignorelist = [".pdf", ".doc", ".docx", ".ppt", "rtf"]
        if any(ending for ending in ignorelist if filepath.strip().endswith(ending)):
            continue

        #The first 3 rows are only metadata
        for row in lines[3:]:
            row = row.strip()
            if len(row) == 0:
                continue
            if row[-1] in string.punctuation:
                rows.append(row)
            elif continuos:
                rows.append(row)
            else:
                rows.append(row + ". ")

        content = ' '.join(rows)

    calc = readcalc.ReadCalc(content)

    part = ""
    if "/part" in filename:
        part = filename.rsplit("/",2)[1]

    if "/" in filename:
        filename = filename.rsplit("/",1)[1]

    readability_row = [filename, part]
    readability_row.extend( get_list_of_readability(calc) )

    csv_writer.writerow(readability_row)

csv_file.close()

