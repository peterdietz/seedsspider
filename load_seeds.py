import redis
import os

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# VC can generate seeds:  java -jar impl/task/lambda/target/vericite-task.jar seedslist /opt/seeds.txt
seeds_file = os.getcwd()+"/seeds.txt"
with open(seeds_file, 'r') as f:
    start_urls = f.read().splitlines()

print "Inserting {} urls from {} into redis start_urls".format(len(start_urls), seeds_file)
r.lpush('SeedsSpider:start_urls', *start_urls)

r.keys("SeedsSpider:items")