# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from urlparse import urlparse
import os
import glob
import sys
import validators


class ReadingLevelTrain(object):
    clf = None
    # accepted_languages = {'en', 'es', 'de', 'fr', 'ru', 'sv', 'no', 'zh', 'zh-cn'}
    accepted_languages = {'en'}
    url_field = 'url'
    category_field = 'fk_grade'

    pairs = [{'url': 'https://en.wikipedia.org/wiki/Rhombicuboctahedron', 'score': 10},
             {'url': 'https://en.wikipedia.org/wiki/Uniform_polyhedron', 'score': 20},
             {'url': 'https://google.com/something', 'score': 5},
             {'url': 'https://yahoo.com/more', 'score': 15},
             ]

    def __init__(self):
        # tokenize the url into pieces
        def my_tokenizer(url):
            u = urlparse(url)
            token = None
            if u.query:
                token = {u.hostname, u.path, u.query}
            else:
                token = {u.hostname, u.path}

            return token

        vectorizer = TfidfVectorizer(tokenizer=my_tokenizer, use_idf=False)

        self.clf = Pipeline([
            ('vec', vectorizer),
            ('clf', Perceptron()),
        ])

        # Import all data
        self.import_all_exports()

    def test(self):
        try:
            df = self.read_dataset(os.getcwd() + '/export.csv')
            urls_train, urls_test, lang_train, lang_test = train_test_split(df[self.url_field], df[self.category_field], test_size=0.5)
            self.clf.fit(urls_train, lang_train)
            lang_predicted = self.clf.predict(urls_test)

            print(metrics.classification_report(lang_test, lang_predicted))

            cm = metrics.confusion_matrix(lang_test, lang_predicted)
            print(cm)

            # graph
            #import matplotlib.pyplot as plt
            #plt.matshow(cm, cmap=plt.cm.jet)
            #plt.show()

            self.predict_pairs(self.pairs)
        except ValueError as e:
            print "exception: {}".format(str(e))

    def read_dataset(self, filename):
        df = pd.read_csv(filename, encoding='utf-8', error_bad_lines=False)
        if self.category_field in df.columns:
            df.drop_duplicates(inplace=True)
            df = df.dropna()
            df = df[df[self.category_field].notnull() & df[self.url_field].notnull()]
            df = df[[self.url_field, self.category_field]]
            return df
        else:
            raise ValueError("Missing field")

    # Can't add just one, (too small)
    def add_two_data(self):
        print 'Add one data'
        pairs = [{'url':'https://twitter.com/elonmusk?lang=sv', 'score': 10},
                 {'url':'https://twitter.com/elonmusk?lang=de', 'score': 20}]
        urls, langs = self.get_fields(pairs)
        self.clf.fit(urls, langs)
        self.predict_pairs(pairs)

    def import_all_exports(self):
        export_files = glob.glob(os.getcwd() + "/export*.csv")
        for file in export_files:
            if self.is_non_zero_file(file):
                try:
                    df = self.read_dataset(file)
                    print "Import file: {} processing {} records".format(file, str(len(df)))
                    self.clf.fit(df[self.url_field].tolist(), df[self.category_field].tolist())
                except ValueError as e:
                    print "Unable to import file: {}, exception: {}".format(file, str(e))

    def get_fields(self, pairs):
        urls = []
        langs = []
        for pair in pairs:
            urls.append(pair['url'])
            langs.append(pair['score'])

        return urls, langs

    def predict_pairs(self, pairs):
        urls, scores = self.get_fields(pairs)
        predicted = self.clf.predict(urls)

        i = 0
        for prediction in predicted:
            result = "correct" if prediction==scores[i] else "incorrect"
            print "#{} predicted:[{}], expected:[{}], url:[{}], result: {}".format(i, prediction, scores[i], urls[i], result)
            i += 1

    def is_url_predicted_in_accepted_lang(self, url):
        predicted = self.clf.predict([url])
        return predicted[0] in self.accepted_languages

    def train_single(self, url, score):
        # Can't insert a single url/lang
        pairs = [{'url': url, 'score': score},
                 {'url': 'https://twitter.com/elonmusk?lang=de', 'score': 20}]
        urls, scores = self.get_fields(pairs)
        self.clf.fit(urls, scores)

    def is_non_zero_file(self, fpath):
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

    def predict_lang(self, *args):
        for arg in args:
            for url in arg:
                if(validators.url(url)):
                    predicted = self.clf.predict([url])
                    print "URL: {} has predicted lang of {}".format(url, predicted)


if __name__ == '__main__':
    inst = ReadingLevelTrain()
    #inst.test()
    #inst.add_two_data()
    #inst.predict_lang(sys.argv)