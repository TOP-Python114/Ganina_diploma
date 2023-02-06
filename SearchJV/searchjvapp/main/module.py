from django.conf import settings
import nltk
import os
import pandas as pd
import sqlite3
import string
from sklearn.feature_extraction.text import TfidfVectorizer


def stem_tokens(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=normalize)
    tfidf = vectorizer.fit_transform([text1, text2])
    return (tfidf * tfidf.T).A[0, 1]


def rate_result_df(df, text2):
    results = pd.DataFrame(columns=['name', 'descr', 'alternate_url', 'rate'])
    for i in range(len(df)):
        rate = cosine_sim(df.loc[i]['descr'], text2)
        results.loc[i] = df.loc[i]['name'], df.loc[i]['descr'], df.loc[i]['alternate_url'], str(rate)

    results.sort_values('rate', ascending=False, inplace=True)
    return results[:10]


def run(text2):
    file_path = os.path.join(settings.BASE_DIR, 'vacancy.db')
    con = sqlite3.connect(file_path)
    df = pd.read_sql_query("SELECT * FROM vacancies", con)
    printed_val_to = rate_result_df(df, text2)
    list_link = []
    for i in printed_val_to['alternate_url']:
        list_link.append(i)
    return list_link
