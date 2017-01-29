import oauth2 as oauth
import json, pandas


CONSUMER_KEY = "jxsImBs5RaK0qlb64VmOaXjWO"
CONSUMER_SECRET = "D1fGgFSQwCWz1B4ivK2XGb6jfXUNRFo1dWR5ZTviEDH6Afqbwa"
ACCESS_KEY = "74273738-anVwQKEykEmvIiygtw16q7HL4RfHZ5Xd0SKq24Ff4"
ACCESS_SECRET = "6XzwjjTXPAoPqcPDbBOIgvIAlXdszmN933UJ8GmiZ1oPu"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline = "https://api.twitter.com/1.1/search/tweets.json?q=sacca&count=100&since_id="
endpoint = '825403419376496641'

donations = []


def getDonations(orig_id, max_id, count):
	if count < 0:
		return
	req_str = timeline + str(orig_id)
	if orig_id != max_id:
		req_str += '&max_id=' + str(max_id)
	# print 'REQUEST: ', req_str
	response, data = client.request(req_str)
	tweets = json.loads(data)
	# print tweets
	if tweets['errors']:
		print 'ERROR: ' + tweets['errors'][0]['message']
		return

	try:
		print 'start: ', tweets['search_metadata']['since_id_str'], ' end: ', tweets['search_metadata']['max_id_str']

		# print tweets
		min_id = 900000000000000000
		for tweet in tweets['statuses']:
		    # print tweet['statuses']
		    min_id = min(min_id, tweet['id'])
		    # print 'TWEET: ', tweet['in_reply_to_status_id']
		    # print tweet
		    if tweet['in_reply_to_status_id'] == orig_id:
				line = {}
				line["name"] = tweet['user']['name'].encode('utf-8')
				line["handle"] = tweet['user']['screen_name'].encode('utf-8')
				line["id"] = tweet['id']
				line["time"] = tweet['created_at'].encode('utf-8')
				line["text"] = tweet['text'].encode('utf-8')
				try:
					line['link'] = tweet['entities']['media'][0]['url'].encode('utf-8')
					line["image"] = tweet['entities']['media'][0]['media_url'].encode('utf-8')
				except KeyError:
					print('ERR: media key not found')


				donations.append(line)

		    if tweet['is_quote_status']:
		    	try:
		    		q_id = tweet['quoted_status_id']
		    	except KeyError:
		    		print('ERR: quoted status ID not found')
		    		q_id = 0
				if q_id == orig_id:
					line = {}
					line["name"] = tweet['user']['name'].encode('utf-8')
					line["handle"] = tweet['user']['screen_name'].encode('utf-8')
					line["id"] = tweet['id']
					line["time"] = tweet['created_at'].encode('utf-8')
					line["text"] = tweet['text'].encode('utf-8')
					try:
						line['link'] = tweet['entities']['media'][0]['url'].encode('utf-8')
						line["image"] = tweet['entities']['media'][0]['media_url'].encode('utf-8')
					except KeyError:
						print('ERR: media key not found')

					donations.append(line)

		getDonations(orig_id, min_id, count - 1)
	except KeyError:
		print('ERR: SOME KEY ERROR FUCK')
	# getDonations(orig_id, tweets['search_metadata']['max_id_str'], count - 1)
	# getDonations(orig_id, tweets['search_metadata']['next_results'], count - 1)

getDonations(825403419376496641, 825403419376496641, 100)

print donations

df = pandas.DataFrame.from_dict(donations)
df.to_csv('test.csv')






