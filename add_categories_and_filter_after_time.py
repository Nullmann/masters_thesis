# This script filters the posts after time, omitting posts done during the old guidelines

import csv
import sys
import datetime

# Iteratively find out the max csv field size to not run into field limit problems.
# See https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072.
maxInt = sys.maxsize
while True:
    # Decrease the maxInt value by factor 10 as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)
# print("maxInt: " + str(maxInt))  # 922337203 on this laptop and PC.

# ------------ Actual reading of the file --------------

# Keywords taken from reading hundreds of the most viewed forum posts. No duplicates. "review" already matches "reviews".
categories = ["container",
            "duplicate",
            "sign-in with apple",
            "html5",  # 4.7
            "kids category",  # 1.3 and 5.1.4
            "Data harvesting",  # 5.1.2 Data use and sharing
            "VPN",  # 5.4
            "cryptocurrency",
            "loot boxes",
            "privacy policy",
            "steam link",
            "emoji",
            "template",
            "trading",  # 3.2.1(iii)
            "financial",
            "minimum functionality",
            "mpm",  # 5.5 parental control apps
            "in-app purchase",  # 3.1.1
            "gambling",
            "bugs",  # 2.1 App completeness
            "user generated content",  # 1.2
            "georestriction",
            "vague",
            "hidden or undocumented",
            "intellectual property",  # 5.2.1
            "goods and services outside",  # 3.1.5(a) physical goods
            "vaping",  # 1.4.3 No promoting of tobacco or vaping
            "subscriptions",
            "facebook login"  # Login
            ]

with open('fitlered_messages_all_rows_with_keywords.csv', 'r', newline='', encoding="utf-8", errors='ignore') as read_file:
    csv_reader = csv.reader(read_file, delimiter=';')
    next(csv_reader)  # Skip header row

    with open("fitlered_messages_all_rows_with_keywords_and_categories_after_Jul_2016.csv", 'w', newline='', encoding="utf-8", errors='ignore') as write_file:
        # with open("testing_result.csv", 'w', newline='', encoding="utf-8",errors='ignore') as write_file:
        writer = csv.writer(write_file, delimiter=';')
        writer.writerow(['post_id', 'text', 'sentiment', 'link_to_post', 'this_helped_me', 'thread_id', 'username', 'creation_time', 'plain_text', 'number_of_this_helped_me', 'reply_to_postid', 'number_of_views', 'number_of_replies', 'tags_list', 'forum', 'subforum', 'title', 'keywords', 'categories'])

        for row in csv_reader:
            text = row[1]
            plain_text = row[8]
            reply_to_postid = row[10]
            title = row[16]
            title = title.lower()
            creation_time = row[7]

            found_categories = []  # Refresh for each row

            time = datetime.datetime.strptime(creation_time, '%Y-%m-%d %H:%M:%S')
            if time > datetime.datetime(2016, 6, 14):  # Filter for posts which were created after the new guidelines

                for category in categories:
                    # Add a found category. Use title only for thread starters.
                    if text.find(category) != -1 or plain_text.find(category) != -1 or (reply_to_postid == str(0) and title.find(category) != -1):
                        found_categories.append(category)  # It may fit multiple categories

                found_categories = ', '.join(map(str, found_categories))  # Nice, comma-separated output
                row.append(found_categories)
                writer.writerow(row)  # Add to resulting csv

