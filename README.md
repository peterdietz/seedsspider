scrapy crawl HackerNews -o results.csv -t csv

scrapy crawl SeedsSpider

Reads seeds from /opt/seeds.txt, which looks like:
https://en.wikipedia.org/wiki/Rhombicuboctahedron
https://martinfowler.com/articles/viticulture-gallerist.html

Writes output scraped items (intermediate look at the data) to /opt/export.csv
domain,query_path,language,title,url,response_code,num_links,score
en.wikipedia.org,,en,Kosciuszko Huts Association - Wikipedia,https://en.wikipedia.org/wiki/Kosciuszko_Huts_Association,200,103,1


To do some ML classifying on the output:
python language_train.py