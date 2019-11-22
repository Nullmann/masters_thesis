# This script adds the found keywords as a row to the data.
# The earlier filtering script stopped when it had found one keyword (to not add the row several times).
# Could have been done nice, but this is an iterative process.

import csv
import sys

# Iteratively find out the max csv field size to not run into field limit problems.
# See https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072.
maxInt = sys.maxsize
while True:
    # Decrease the maxInt value by factor 10 as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)
#print("maxInt: " + str(maxInt))  # 922337203 on this laptop and PC.

# ------------ Actual reading of the file --------------

'''
keywords = ["guideline", "guidelines", "reject", "rejected", "rejecting", "rejection", "review", "waiting for review",
            "reviewed", "review", "submit", "submitting", "submission", "upload", "developer certificate",
            "developer program", "apple developer account", "section", "paragraph", "processing"]
'''

# Keywords taken from reading hundreds of the most viewed forum posts. No duplicates. "review" already matches "reviews".
keywords = ["guideline", "reject", "review", "submit", "submission", "upload", "developer certificate",
            "developer program", "apple developer account", "section", "paragraph", "processing"]

# Apple Developer Review Guidelines; table of contents.
keywords += ["1. safety",
                 "1.1 objectionable content",
                 "1.2 user generated content",
                 "1.3 kids category",
                 "1.4 physical harm",
                 "1.5 developer information",
                 "1.6 data security",
             "2. performance",
                 "2.1 app completeness",
                 "2.2 beta testing",
                 "2.3 accurate metadata",
                 "2.4 hardware compatibility",
                 "2.5 software requirements",
             "3. business",
                 "3.1 payments",
                 "3.1.1 in-app purchase",
                 "3.1.2 subscriptions",
                 "3.1.3(a) “reader” apps",
                 "3.1.3(b) multiplatform services",
                 "3.1.4 hardware-specific content",
                 "3.1.5(a) goods and Services Outside of the App",
                 "3.1.5(b) cryptocurrencies",
                 "3.1.6 apple Pay",
                 "3.1.7 advertising",
                 "3.2 other business model issues",
                 "3.2.1 acceptable",
                 "3.2.2 unacceptable",
             "4. design",
                 "4.1 copycats",
                 "4.2 minimum functionality",
                 "4.3 spam",
                 "4.4 extensions",
                 "4.5 apple sites and services",
                 "4.6 alternate app icons",
                 "4.7 html5 games, bots, etc.",
                 "4.8 sign in with apple",
             "5. legal",
                 "5.1 privacy",
                 "5.1.1 data collection and storage",
                 "5.1.2 data use and sharing",
                 "5.1.3 health and health research",
                 "5.1.4 kids",
                 "5.1.5 location services",
                 "5.2 intellectual property",
                 "5.3 gaming, gambling, and lotteries",
                 "5.4 vpn Apps",
                 "5.5 mobile device management",
                 "5.6 developer code of conduct"
             ]

# These numbers also include sub-numbering without titles. Use spaces around to not match unwanted numbers.
# E.g. that the string "1.1" does not match "3.1.1", being totally unrelated.
keywords += [
             " 1.1 ",
             " 1.1.1 ",
                " 1.1.2 ",
                " 1.1.3 ",
                " 1.1.4 ",
                " 1.1.5 ",
                " 1.1.6 ",
                " 1.1.7 ",
             " 1.2 ",
             " 1.3 ",
             " 1.4 ",
                " 1.4.1 ",
                " 1.4.2 ",
                " 1.4.3 ",
                " 1.4.4 ",
                " 1.4.5 ",
             " 1.5 ",
             " 1.6 ",

             " 2.1 ",
             " 2.2 ",
             " 2.3 ",
                " 2.3.1 ",
                " 2.3.2 ",
                " 2.3.3 ",
                " 2.3.4 ",
                " 2.3.5 ",
                " 2.3.6 ",
                " 2.3.7 ",
                " 2.3.8 ",
                " 2.3.9 ",
                " 2.3.10 ",
                " 2.3.11 ",
                " 2.3.12 ",
             " 2.4 ",
                " 2.4.1 ",
                " 2.4.2 ",
                " 2.4.3 ",
                " 2.4.4 ",
                " 2.4.5 ",
             " 2.5 ",
                " 2.5.1 ",
                " 2.5.2 ",
                " 2.5.3 ",
                " 2.5.4 ",
                " 2.5.5 ",
                " 2.5.6 ",
                " 2.5.7 ",
                " 2.5.8 ",
                " 2.5.9 ",
                " 2.5.10 ",
                " 2.5.11 ",
                " 2.5.12 ",
                " 2.5.13 ",
                " 2.5.14 ",
                " 2.5.15 ",

             " 3.1 ",
             " 3.1.1 ",
             " 3.1.2 ",
             " 3.1.3(a) ",
             " 3.1.3(b) ",
             " 3.1.4 ",
             " 3.1.5(a) ",
             " 3.1.5(b) ",
             " 3.1.6 ",
             " 3.1.7 ",
             " 3.2 ",
             " 3.2.1 ",
             " 3.2.2 ",

             " 4.1 ",
             " 4.2 ",
                " 4.2.1 ",
                " 4.2.2 ",
                " 4.2.3 ",
                " 4.2.4 ",
                " 4.2.5 ",
                " 4.2.6 ",
                " 4.2.7 ",
             " 4.3 ",
             " 4.4 ",
                " 4.4.1 ",
                " 4.4.2 ",
                " 4.4.3 ",
             " 4.5 ",
                " 4.5.1 ",
                " 4.5.2 ",
                " 4.5.3 ",
                " 4.5.4 ",
                " 4.5.5 ",
                " 4.5.6 ",
             " 4.6 ",
             " 4.7 ",
             " 4.8 ",

             " 5.1 ",
             " 5.1.1 ",
             " 5.1.2 ",
             " 5.1.3 ",
             " 5.1.4 ",
             " 5.1.5 ",
             " 5.2 ",
                " 5.2.1 ",
                " 5.2.2 ",
                " 5.2.3 ",
                " 5.2.4 ",
                " 5.2.5 ",
             " 5.3 ",
             " 5.4 ",
             " 5.5 ",
             " 5.6 "
             ]

subforums_to_search = ["App Store", "App Submission and Review", "App Store Connect", "App Analytics"]

with open('fitlered_messages_all_rows.csv', 'r', newline='', encoding="utf-8", errors='ignore') as read_file:
#with open('testing.csv', 'r', newline='', encoding="utf-8", errors='ignore') as read_file:
    csv_reader = csv.reader(read_file, delimiter=';')

    with open("fitlered_messages_all_rows_with_keywords.csv", 'w', newline='', encoding="utf-8", errors='ignore') as write_file:
    #with open("testing_result.csv", 'w', newline='', encoding="utf-8",errors='ignore') as write_file:
        writer = csv.writer(write_file, delimiter=';')

        for row in csv_reader:
            text = row[1]
            plain_text = row[8]
            reply_to_postid = row[10]
            title = row[16]
            title = title.lower()

            found_keywords = []

            for keyword in keywords:
                # Add the text if the text or the title contains the keyword. Title only for thread starters.
                if text.find(keyword) != -1 or plain_text.find(keyword) != -1 or (reply_to_postid == str(0) and title.find(keyword) != -1):
                    found_keywords.append(keyword)

            found_keywords = ', '.join(map(str, found_keywords))
            row.append(found_keywords)
            writer.writerow(row)  # Add to resulting csv
