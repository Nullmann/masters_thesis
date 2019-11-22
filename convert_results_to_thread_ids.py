# This script is used to extract the thread ids of an existing document
# Reduces 303 and 404 failures, less brute-forcing

import csv

thread_ids = []
with open('Ergebnisse/threads.csv', 'r', newline='', encoding="utf-8", errors='ignore') as csvfile:
    next(csvfile)  # Skip header row
    csvreader = csv.reader(csvfile, delimiter=';', skipinitialspace=True)
    for row in csvreader:
        thread_ids.append(row[0])

thread_ids = [int(x) for x in thread_ids]
thread_ids.sort()

with open('thread_ids_to_crawl.txt', 'w') as filehandle:
    for listitem in thread_ids:
        filehandle.write('%s\n' % listitem)