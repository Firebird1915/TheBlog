import requests
import dateparser
from settings import *

G_BLOGURL = "http://firebirds1915.blogspot.com/feeds/posts/default?alt=json"
POST_DIR = "_posts/"

def updateChanges(field, time):
	LAST_UPDATED[field] = time
	updates = open('settings.py','w')
	updates.write("LAST_UPDATED = %s" % LAST_UPDATED)
	updates.close()

def writePostEntry(entry):
	d = dateparser.parse(u'%s' % entry['updated']['$t'])
	datedfile = str(d.year) + "-" + str(d.month) + "-" + str(d.day) + "-" + entry['title']['$t'].strip().replace(" ", "-")
	path = POST_DIR + datedfile + '.html'
	post = open(path,'w')
	post.write("---\n")
	post.write("layout: post\n")
	post.write("title: \"%s\"\n" % entry['title']['$t'])
	post.write("---\n")
	post.write(entry['content']['$t'])
	#dateparser.parse(u'2015-09-17T04:05:53.528-04:00')
	#print(data['feed']['updated']['$t'])
	#entry['updated']
	#entry['published']
	post.close()

def updateGroveBog():
	data = requests.get(G_BLOGURL).json()
	if data['feed']['updated']['$t'] == LAST_UPDATED['grove']:
		print("Everything upto date.")
	else:
		print("updating Mr. Grove's Blog")
		for entry in data['feed']['entry']:
			writePostEntry(entry)
		print("Finished updates.\n Now updating settings.py")
		updateChanges('grove', data['feed']['updated']['$t'])

def main():
	updateGroveBog()

main()