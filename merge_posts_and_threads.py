# This script combines posts and threads into one file.
# Makes data redundant and takes up more space, but is easier for analysis.

import pandas as pd

df_a = pd.read_csv("crawling_results/posts.csv", encoding="utf-8", sep=';')
df_b = pd.read_csv("crawling_results/threads.csv", encoding="utf-8", sep=';')

merged = pd.merge(df_a, df_b, on='thread_id', how='inner')
merged.to_csv("crawling_results/posts_and_threads_all.csv", index=False, sep=";", encoding="utf-8")
