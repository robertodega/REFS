import csv
import os

os.system('clear')

csvName = input("CSV name: ")
if csvName:
    filename = csvName+".csv"

try:
    with open(filename) as cf:
        spamreader = csv.reader(cf)
        for row in spamreader:
            print(row)
except Exception as e:
    errMsg = "CSV "+filename+" not loaded"
    print(errMsg)