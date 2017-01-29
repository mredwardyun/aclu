import twitter

api = twitter.Api(consumer_key='jxsImBs5RaK0qlb64VmOaXjWO',
                  consumer_secret='D1fGgFSQwCWz1B4ivK2XGb6jfXUNRFo1dWR5ZTviEDH6Afqbwa',
                  access_token_key='74273738-anVwQKEykEmvIiygtw16q7HL4RfHZ5Xd0SKq24Ff4',
                  access_token_secret='6XzwjjTXPAoPqcPDbBOIgvIAlXdszmN933UJ8GmiZ1oPu')
sacca = api.GetUserTimeline('586')

replies = api.GetSearch(raw_query='q=sacca',since_id='825403419376496641')
# print replies

donations = []

def createLine(raw_json):
	line = {}
	line["name"] = raw_json.user.name
	line["handle"] = raw_json.user.screen_name
	if raw_json.media != None:
		# print raw_json.media
		line['link'] = raw_json.media
		# line["link"] = raw_json.media['DisplayURL']
		# line["image"] = raw_json.media.media_url
	line["id"] = raw_json.id
	return line

print replies[0]['created_at']

# for r in replies:
# 	# if r.in_reply_to_user_id == 586:
# 	line = createLine(r)
# 	print(line)
# 	donations.append(line)

# print donations