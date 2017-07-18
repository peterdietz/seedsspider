# Scrapy Spider

(demo) To parse items out of hackernews
```
scrapy crawl HackerNews -o results.csv -t csv
```

To crawl the web from seeds.
```
scrapy crawl SeedsSpider
```

Reads seeds from `seeds.txt`, which has one url per line:
```
https://en.wikipedia.org/wiki/Rhombicuboctahedron
https://martinfowler.com/articles/viticulture-gallerist.html
```
Writes output scraped items (intermediate look at the data) to `export.csv`
```
detected_language,url,response_code,num_links,response_type,declared_language
en,https://en.wikipedia.org/wiki/Anne_Bradstreet,200,472,HTML,en
en,https://quizlet.com/37641628/american-literature-flash-cards/,200,29,HTML,en-gb
en,https://en.wikipedia.org/wiki/Donald_Woods,200,312,HTML,en
es,http://www.taringa.net/posts/info/18045919/Kaprosuchus-el-cocodrilo-jabali.html,200,137,HTML,es
```

To do some ML classifying on the output:
```
python language_train.py
```

You will need to use pip install to install several python modules first.
```
pip install -r requirements.txt
```

The language classifier should output predictions:

Classification Report:
```
             precision    recall  f1-score   support

         de       0.90      0.45      0.60        40
         en       0.92      0.42      0.58        57
         es       0.86      0.29      0.43        86
         fr       1.00      0.43      0.60        35
         no       0.92      0.39      0.55        56
         ru       1.00      0.26      0.42       182
         sv       0.96      0.31      0.47       153
      zh-cn       0.86      1.00      0.93      2578

avg / total       0.88      0.87      0.84      3187
```

Confusion Matrix:
```
[[  18    0    0    0    0    0    0   22]
 [   1   24    0    0    0    0    0   32]
 [   0    1   25    0    0    0    0   60]
 [   1    0    0   15    1    0    0   18]
 [   0    0    0    0   22    0    0   34]
 [   0    0    0    0    0   48    0  134]
 [   0    1    0    0    0    0   47  105]
 [   0    0    4    0    1    0    2 2571]]
 ```
 
 
 Predictions of a sample of urls:
 ```
#0 predicted:[en], expected:[en], url:[https://en.wikipedia.org/wiki/Rhombicuboctahedron], result: correct
#1 predicted:[en], expected:[en], url:[https://en.wikipedia.org/wiki/Uniform_polyhedron], result: correct
#2 predicted:[en], expected:[sv], url:[https://sv.wikipedia.org/wiki/Geometri], result: incorrect
#3 predicted:[en], expected:[es], url:[https://es.wikipedia.org/wiki/Geometr%C3%ADa], result: incorrect
#4 predicted:[en], expected:[de], url:[https://de.wikipedia.org/wiki/Geometrie], result: incorrect
#5 predicted:[en], expected:[ru], url:[https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D1%8F], result: incorrect
#6 predicted:[en], expected:[en], url:[https://twitter.com/elonmusk], result: correct
#7 predicted:[sv], expected:[sv], url:[https://twitter.com/elonmusk?lang=sv], result: correct
#8 predicted:[zh-cn], expected:[zh-cn], url:[https://twitter.com/something?lang=zh-cn], result: correct
```

Not perfect, but with more data, configuration tweaks, and other fixes it can improve.