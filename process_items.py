import json
import redis
import numpy

r = redis.StrictRedis(host='localhost', port=6379, db=0)
elements = r.lrange("SeedsSpider:items", 0, -1)
l=[]

f = open('items.json', 'w')
f.write('[')
for i in elements:
    j = json.loads(i)
    #if 'fk_grade' in j:
    #    l.append(j['fk_grade'])
    f.write("{},".format(i))
f.write("]")


#print "Mean: {}".format(str(numpy.mean(l)))
#print "Avg: {}".format(str(numpy.average(l)))
#print "Median: {}".format(str(numpy.median(l)))
#print "Standard deviation: {}".format(numpy.std(l))
#print "Min: {}".format(str(numpy.min(l)))
#print "Max: {}".format(str(numpy.max(l)))
