# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from urlparse import urlparse
import os


class LanguageTrain(object):
    clf = None
    accepted_languages = {'en', 'es', 'de', 'fr', 'ru', 'sv', 'no', 'zh', 'zh-cn'}
    language_field = 'declared_language'
    url_field = 'url'

    pairs = [{'url':'https://en.wikipedia.org/wiki/Rhombicuboctahedron', 'lang':'en'},
             {'url':'https://en.wikipedia.org/wiki/Uniform_polyhedron', 'lang':'en'},
             {'url':'https://sv.wikipedia.org/wiki/Geometri', 'lang':'sv'},
             {'url':'https://es.wikipedia.org/wiki/Geometr%C3%ADa', 'lang':'es'},
             {'url':'https://de.wikipedia.org/wiki/Geometrie', 'lang':'de'},
             {'url':'https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D1%8F', 'lang':'ru'},
             {'url':'https://twitter.com/elonmusk', 'lang':'en'},
             {'url':'https://twitter.com/elonmusk?lang=sv', 'lang':'sv'},
             {'url':'https://twitter.com/something?lang=zh-cn', 'lang':'zh-cn'},
             ]


    def __init__(self):
        df = self.read_dataset(os.getcwd() + '/export.csv')
        urls_train, urls_test, lang_train, lang_test = train_test_split(df[self.url_field], df[self.language_field], test_size=0.5)

        # tokenize the url into pieces
        def my_tokenizer(url):
            u = urlparse(url)
            return {u.hostname, u.path, u.query}

        vectorizer = TfidfVectorizer(tokenizer=my_tokenizer, use_idf=False)

        self.clf = Pipeline([
            ('vec', vectorizer),
            ('clf', Perceptron()),
        ])

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

    def read_dataset(self, filename):
        df = pd.read_csv(filename, encoding='utf-8')
        df.drop_duplicates(inplace=True)
        df = df[df[self.language_field].isin(self.accepted_languages)]
        df = df[[self.url_field, self.language_field]]
        return df

    def add_more_data(self):
        print("ADDING MORE DATA")
        df = self.read_dataset(os.getcwd() + '/export-all-seeds.csv')
        docs_train, docs_test, y_train, y_test = train_test_split(df[self.url_field], df[self.language_field], test_size=0.0)
        self.clf.fit(docs_train, y_train)
        self.predict_pairs(self.pairs)

    def add_two_data(self):
        print 'Add one data'
        pairs = [{'url':'https://twitter.com/elonmusk?lang=sv', 'lang':'sv'},
                 {'url':'https://twitter.com/elonmusk?lang=de', 'lang':'de'}]
        urls, langs = self.get_fields(pairs)
        self.clf.fit(urls, langs)
        self.predict_pairs(pairs)

    def get_fields(self, pairs):
        urls = []
        langs = []
        for pair in pairs:
            urls.append(pair['url'])
            langs.append(pair['lang'])

        return urls, langs

    def predict_pairs(self, pairs):
        urls, langs = self.get_fields(pairs)
        predicted = self.clf.predict(urls)

        i = 0
        for prediction in predicted:
            result = "correct" if prediction==langs[i] else "incorrect"
            print "#{} predicted:[{}], expected:[{}], url:[{}], result: {}".format(i, prediction, langs[i], urls[i], result)
            i += 1


if __name__ == '__main__':
    inst = LanguageTrain()

    inst.add_two_data()
    inst.add_more_data()