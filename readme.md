# Crawler for Developer Forum
This is a web crawler for my master's thesis, using the scrapy-framework: https://github.com/scrapy/scrapy

Remember to always respect the website owner!

## Installation
Install python 3 (and pip) from https://www.python.org/

Upgrade pip and install necessary libraries. You may or may not need the python3 prefix.
```
python3 -m pip install --upgrade pip
python3 -m pip install scrapy
python3 -m pip install unidecode
python3 -m pip install beautifulsoup4
python3 -m pip install pandas
python3 -m pip install textblob
python3 -m textblob.download_corpora
python3 -m pip install matplotlib
python3 -m pip install pyspellchecker
```

Additional step for Windows:
```
python3 -m pip install pypiwin32
Install c++ build tools, see: https://stackoverflow.com/questions/51927014/microsoft-visual-c-14-0-is-required
```

## Execute crawling
cd to scrapy project root `apple_dev_forum` and execute with `scrapy crawl dev_forum_crawl_threads`
To have it log both to console and a file, execute with `scrapy crawl dev_forum_crawl_threads 2>&1 | tee $(date +%Y-%m-%d_%H-%M)scrappy.log`

## Speed
The actual speed depends on CONCURRENT_REQUESTS in settings.py

The file thread_ids_to_crawl.txt is filled with all threadids which do not throw an 404 or 302 error, heavily speeding up the crawling process.
The first brute-force run took about 2 days. A consecutive run took 6 hours up until thread-id 120812.

It was crawled with a Raspberry Pi 3 Model B with 32 concurrent requests.

## Results
There will be 2 different csv files, structured like this:
- thread table: thread_id, number_of_views, number_of_replies, tags, forum, subforum, title
- post table: post_id, thread_id, creation_time, username, html_text, plain_text number_of_this_helped_me, correct_answer, reply_to_postid

# Additonal scripts for analyzing data
Every script has a description, explaining its purpose as well as plenty of comments for better code understanding.

The order in which the scripts were executed is as follows:
- convert_results_to_thread_ids.py
- merge_posts_and_threads.py
- clean_and_filter_crawled_data.py
- add_remaining_rows_to_filtered_messages.py
- add_keywords.py
- add_categories_and_filter_after_time