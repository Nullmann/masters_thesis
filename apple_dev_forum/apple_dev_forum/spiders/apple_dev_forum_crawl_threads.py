import scrapy
import re
from datetime import datetime
import csv
from unidecode import unidecode
from bs4 import BeautifulSoup

# Can be looked up with https://forums.developer.apple.com/content?sortKey=all~creationDateDesc&sortOrder=0
last_thread_id = 120835  # As of 2019-08-02
file_name_for_threads = str(datetime.now().strftime("%Y-%m-%d_%H-%M")) + "threads.csv"
file_name_for_posts = str(datetime.now().strftime("%Y-%m-%d_%H-%M")) + "posts.csv"


def init_csv_files():
    with open(file_name_for_threads, mode='w', newline='', encoding="utf-8") as threads_file:
        csv_writer = csv.writer(threads_file, delimiter=';')
        csv_writer.writerow(['thread_id', 'number_of_views', 'number_of_replies', 'tags_list', 'forum', 'subforum', 'title'])

    with open(file_name_for_posts, mode='w', newline='', encoding="utf-8") as posts_file:
        csv_writer = csv.writer(posts_file, delimiter=';')
        csv_writer.writerow(['post_id', 'thread_id', 'username', 'creation_time', 'plain_text', 'number_of_this_helped_me', 'reply_to_postid'])


class ThreadSpider(scrapy.Spider):
    name = 'dev_forum_crawl_threads'

    def start_requests(self):

        # Initialize csv files with headers.
        init_csv_files()

        # Crawl threads we know exist from previous runs. Speeds up the crawling because it does not run into 404 or 302.
        with open('thread_ids_to_crawl.txt', 'r', newline="", encoding="utf-8", errors='ignore') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', skipinitialspace=True)
            for row in csvreader:
                response = scrapy.Request('https://forums.developer.apple.com/thread/' + row[0])
                response.meta['dont_redirect'] = True
                yield response

        # Crawl the new threads, brute force style.
        for current_thread_id in range(120813, last_thread_id):
            response = scrapy.Request('https://forums.developer.apple.com/thread/' + str(current_thread_id))

            # Do not follow redirects. If we are redirected, the thread is not accessable.
            # E.g. we are redirected to the login page here: https://forums.developer.apple.com/thread/89736
            response.meta['dont_redirect'] = True
            yield response

    def parse(self, response):
        thread_id = response.url.split("/")[-1]  # Get the element after the last slash.

        # Skip the thread if it does not exist. Failsafe because 404 errors are ignored anyways.
        possible_error = response.css('div.jive-box-body.jive-standard-formblock').get()
        if possible_error is not None and ('The item does not exist. It may have been deleted.' in possible_error):
            print("Skipping - Thread does not exist")
        else:
            # -------------------------------------- Save data for this thread --------------------------------------
            number_of_views = response.css('span.jive-content-footer-item::text').get()
            number_of_views = re.findall(r'\d+', number_of_views)[0]  # Extract number with regular expression.

            forum = response.xpath("//div[@id='jive-breadcrumb']//a[2]/text()").get()
            subforum = response.xpath('//a[@class="j-last"]/text()').get()
            title = response.xpath('//h1[@class="apple-thread-header"]/text()').get()
            title = title.strip()  # Remove leading and trailing white spaces.
            title = unidecode(str(title))  # Clean non-uft8 characters like https://forums.developer.apple.com/thread/14180

            tags_span = response.css('span.jive-content-footer-tags')
            tags_list = []
            for tag in tags_span.css('a span::text'):
                tags_list.append(unidecode(str(tag.get())))  # Clean non-uft8 characters like https://forums.developer.apple.com/thread/14180
            tags_string = str(tags_list)[1:-1]  # Strip the list of its square brackets.

            number_of_replies = response.css('strong.reply-inhead::text').get()
            number_of_replies = re.findall(r'\d+', number_of_replies)[0]  # Extract number with regular expression.

            with open(file_name_for_threads, mode='a', newline='', encoding="utf-8") as threads_file:
                csv_writer = csv.writer(threads_file, delimiter=';')
                csv_writer.writerow([thread_id, number_of_views, number_of_replies, tags_string, forum, subforum, title])

            # -------------------------------------- Save data for first post --------------------------------------
            post = response.css('div.j-thread-post')
            post_id = response.css('a.j-anchor-target::attr(id)').getall()[1]
            username = post.css('a.j-avatar::attr(data-username)').get()
            username = unidecode(str(username))  # Clean non-uft8 characters

            text = post.css('div.jive-rendered-content').get()
            text = BeautifulSoup(text, "lxml").get_text().strip()  # Extract text only. E.g. throws away links and html stuff.
            text = unidecode(str(text))    # Remove weird characters
            text = text.replace('\n', ' ')  # Everything in one line for csv compatibility

            creation_time = post.css('span.j-post-author::text').getall()[1]
            # Extract exact time string. Times are stored like "Jul 14, 2019 10:53 PM" or "Jul 5, 2019 1:37 PM"
            creation_time = re.search(r'.{3}\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s..', creation_time)
            # Transform weird english time (see above) to nice, formatted datetime like "2019-06-14 13:37:00"
            creation_time = datetime.strptime(creation_time.group(), '%b %d, %Y %I:%M %p')

            '''
            yield {
                'post_id': post_id,
                'thread_id': thread_id,  # External key in thread table.
                'username': username,
                'creation_time': creation_time,
                'html_text': html_text,
                'plain_text': plain_text,
                # These 3 are not applicable to the first post.
                'number_of_this_helped_me': 0,
                'correct_answer': False,
                'reply_to_postid': 0,
            }
            '''

            with open(file_name_for_posts, mode='a', newline='', encoding="utf-8") as posts_file:
                csv_writer = csv.writer(posts_file, delimiter=';')
                csv_writer.writerow([post_id, thread_id, username, creation_time, text, 0, 0])

            # -------------------------------------- Save data for all replies --------------------------------------
            posts = response.css('div.jive-thread-message')
            for post in posts:
                post_id = post.css('div.j-thread-post::attr(id)').get()

                if post_id is not None:
                    # Skip hidden posts like https://forums.developer.apple.com/thread/104941
                    continue
                post_id = post_id[12:]  # Extract id from string like "thread-post-373912".

                creation_time = post.css('span.j-post-author::text').getall()[1]
                # Extract exact time string. Times are stored like "Jul 14, 2019 10:53 PM" or "Jul 5, 2019 1:37 PM"
                creation_time = re.search(r'.{3}\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s..', creation_time)
                # Transform weird english time (see above) to nice, formatted datetime
                creation_time = datetime.strptime(creation_time.group(), '%b %d, %Y %I:%M %p')

                author_span = post.css('span.j-post-author')
                username = author_span.css('a::attr(data-username)').get()

                reply_to_postid = author_span.css('span.j-thread-replyto a::attr(href)')
                reply_to_postid = reply_to_postid.get()[1:]  # Remove hashtag from beginning of html anchor.

                text = post.css('div.jive-rendered-content').get()
                text = BeautifulSoup(text, "lxml").get_text().strip()  # Extract text only
                text = unidecode(str(text))  # Remove weird characters
                text = text.replace('\n', ' ')  # Everything in one line for csv compatibility

                number_of_this_helped_me = post.css('span.j-social-action a.jive-acclaim-likedlink::text')
                # Remove brackets around number (first and last character).
                number_of_this_helped_me = number_of_this_helped_me.get()[1:][:-1]

                # Is only loaded afterwards with javascript and cannot be side-loaded.
                # correct_answer = post.css('div.j-correct')
                # correct_answer = isinstance(correct_answer, str)

                '''
                yield {
                    'post_id': post_id,
                    'thread_id': thread_id,  # External key in thread table.
                    'username': username,
                    'creation_time': creation_time,
                    'html_text': html_text,
                    'plain_text': plain_text,
                    # These 3 are not applicable to the first post.
                    'number_of_this_helped_me': number_of_this_helped_me,
                    'correct_answer': correct_answer,
                    'reply_to_postid': reply_to_postid,
                }
                '''

                with open(file_name_for_posts, mode='a', newline='', encoding="utf-8") as posts_file:
                    csv_writer = csv.writer(posts_file, delimiter=';')
                    csv_writer.writerow([post_id, thread_id, username, creation_time, text, number_of_this_helped_me, reply_to_postid])
