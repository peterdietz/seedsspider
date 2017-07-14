
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from urlparse import urlparse
import os

crawled_items = os.getcwd()+'/export.csv'
df = pd.read_csv(crawled_items, encoding='utf-8')
df.drop_duplicates(inplace=True)

accepted_languages = {'en', 'es', 'de', 'fr', 'ru', 'sv', 'no', 'zh', 'zh-cn'}
language_field = 'declared_language'

df = df[df[language_field].isin(accepted_languages)]
df = df[['url', language_field]]

# Split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split(df['url'], df[language_field], test_size=0.5)


#Vectorizer will tokenize the url into pieces
def my_tokenizer(url):
    u = urlparse(url)
    return {u.hostname, u.path, u.query}

vectorizer = TfidfVectorizer(tokenizer=my_tokenizer, use_idf=False)

clf = Pipeline([
    ('vec', vectorizer),
    ('clf', Perceptron()),
])

# TASK: Fit the pipeline on the training set
clf.fit(docs_train, y_train)

# TASK: Predict the outcome on the testing set in a variable named y_predicted
y_predicted = clf.predict(docs_test)

# Print the classification report
print(metrics.classification_report(y_test, y_predicted))

# Plot the confusion matrix
cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)

# Show the graph
#import matplotlib.pyplot as plt
#plt.matshow(cm, cmap=plt.cm.jet)
#plt.show()

# Predict the result of urls:
sentences = [
    'https://en.wikipedia.org/wiki/Rhombicuboctahedron',
    'https://en.wikipedia.org/wiki/Uniform_polyhedron',
    'https://sv.wikipedia.org/wiki/Geometri',
    'https://es.wikipedia.org/wiki/Geometr%C3%ADa',
    'https://de.wikipedia.org/wiki/Geometrie',
    'https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D1%8F',
    'https://twitter.com/elonmusk',
    'https://twitter.com/elonmusk?lang=sv',
    'https://twitter.com/something?lang=zh-cn'
]
predicted = clf.predict(sentences)

for s, p in zip(sentences, predicted):
    print(u'The language of "%s" is "%s"' % (s, p))

