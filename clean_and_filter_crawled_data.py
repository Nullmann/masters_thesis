# This script cleans the data and then applies a keyword search to it.

import csv
import sys
import string
from textblob import TextBlob
import matplotlib.pyplot as plt

from spellchecker import SpellChecker  # See https://github.com/barrust/pyspellchecker
spell = SpellChecker(distance=1)  # The standard distance of 2 is way too slow for our needs.

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

# Keywords taken from reading hundreds of the most viewed forum posts.
keywords = ["guideline", "guidelines", "reject", "rejected", "rejecting", "rejection", "review", "waiting for review",
            "reviewed", "review", "submit", "submitting", "submission", "upload", "developer certificate",
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

subforums_to_search = ["App Store", "App Submission and Review", "App Store Connect", "App Analytics"]

with open('crawling_results/posts_and_threads_unspellchecked_rows.csv', 'r', newline='', encoding="utf-8", errors='ignore') as read_file:
#with open('crawling_results/testing.csv', 'r', newline='', encoding="utf-8", errors='ignore') as read_file:
    csv_reader = csv.reader(read_file, delimiter=';')

    # Initialize variables.
    total_post_count = 0
    filtered_post_count = 0
    sentiment_sum = 0
    sum_positive_sentiment = 0
    sum_negative_sentiment = 0
    count_positive_posts = 0
    count_negative_posts = 0
    count_neutral_posts = 0
    #all_sentiments = []

    with open("filtered_messages_subforum_and_keyword_with_spellcheck3.csv", 'w', newline='', encoding="utf-8", errors='ignore') as write_file:
        writer = csv.writer(write_file, delimiter=';')
        writer.writerow(["post_id", "text", "sentiment", "link to post", "this helped me"])

        for row in csv_reader:
            # Assign needed rows to variables.
            # post_id;thread_id;username;creation_time;plain_text;number_of_this_helped_me;reply_to_postid;number_of_views;number_of_replies;tags_list;forum;subforum;title
            post_id = row[0]
            thread_id = row[1]
            link_to_post = "https://forums.developer.apple.com/thread/" + thread_id + "#" + post_id

            text = row[4]
            text = text.replace('\n', '')  # Remove new lines for easier analysis.
            text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation from the text like , and ()
            spellchecked_text = ""  # Spell Check every word in the text before filtering for specific words.
            if len(text) < 50000:  # Do not spell check on large posts like code dumps, e.g. https://forums.developer.apple.com/thread/14406#41113
                for word in text.split():  # Split on whitespaces
                    # Better approach would have been to use regular expression: re.findall(r'\w+', text)
                    spellchecked_text += spell.correction(word) + " "  # Get the `most likely` answer
                text = spellchecked_text.lower()

            this_helped_me = row[5]
            reply_to_postid = row[6]
            subforum = row[11]
            title = row[12]
            title = title.lower()

            total_post_count += 1
            print("-- Count: " + str(total_post_count) + " and post id: " + post_id)  # Verbose output because this script takes really long (hours) with spell checker.

            if subforum in subforums_to_search:  # Filter for subforum.
                for keyword in keywords:
                    # Add the text if the text or the title contains the keyword. Title only for thread starters.
                    if text.find(keyword) != -1 or (title.find(keyword) != -1 and reply_to_postid == str(0)):
                        sentiment = TextBlob(text).sentiment.polarity  # Analyze the content with NLP.
                        sentiment_sum += sentiment
                        #all_sentiments.append(sentiment)  # Array with all sentiments (numbers), used for plotting.
                        filtered_post_count += 1

                        writer.writerow([post_id, text, str(sentiment).replace(".", ","), link_to_post, this_helped_me])  # Add to resulting csv

                        if sentiment > 0:
                            count_positive_posts += 1
                            sum_positive_sentiment += sentiment
                        elif sentiment == 0:
                            count_neutral_posts += 1
                        else:
                            count_negative_posts += 1
                            sum_negative_sentiment += sentiment

                    break  # Don't add the same message twice if there is more than one keyword in it.

print("\n")
print("Amount of analyzed posts: " + str(total_post_count))
print("Amount of filtered messages: " + str(filtered_post_count))
print("Sentiment sum: " + str(sentiment_sum))
if filtered_post_count >= 1:  # Be wary of division by zero.
    print("Total sentiment divided by amount: " + str(sentiment_sum/filtered_post_count))
print("\n")
print("count_positive_posts: " + str(count_positive_posts))
print("count_neutral_posts: " + str(count_neutral_posts))
print("count_negative_posts: " + str(count_negative_posts))
print("\n")
print("sum_positive_sentiment: " + str(sum_positive_sentiment))
print("sum_negative_sentiment: " + str(sum_negative_sentiment))

'''
#bins = [-0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
num_bins = 20
#n, bins, patches = plt.hist(all_sentiments, bins=num_bins, histtype="bar", density="true")
n, bins, patches = plt.hist(x=all_sentiments, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
plt.xlabel('Sentiment Polarity')
plt.ylabel('Amount')
plt.grid(True)
plt.title(r'Sentiments of filtered messages of the apple developer forum ')
plt.show()
'''

'''
x = [21,22,23,4,5,6,77,8,9,10,31,32,33,34,35,36,37,18,49,50,100]
num_bins = 5
n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
plt.show()
'''
