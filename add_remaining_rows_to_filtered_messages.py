# With this script, previosuly omitted rows are added again (my bad).
# post_id is a 1 to 1 connection because they are unique.

import pandas as pd

df_a = pd.read_csv("filtered_messages_subforum_and_keyword_with_spellcheck_all.csv", encoding="utf-8", sep=';')
df_b = pd.read_csv("crawling_results/posts_and_threads_all.csv", encoding="utf-8", sep=';')

merged = pd.merge(df_a, df_b, on='post_id', how='inner')
merged.to_csv("fitlered_messages_all_rows.csv", index=False, sep=";", encoding="utf-8")