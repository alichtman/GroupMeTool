# GroupMe Tool
# Created on Aug 8, 2017
# @author: Reid Schendel
# Updated by Aaron Lichtman

# Note: This could be much more Pythonic than it is at the moment.
# Future maintainers should clean up this code more.
# It is not in the greatest shape, but it does work.

import requests

auth_token = ""  # put your auth token here in double quotes
currentGM = -1  # The group chat ID you want to analyze here


def get_member_list(group_id, message_id, member_list):
	"""
	Gets the member list and adds up all like counts.
	"""
	if message_id == 0:
		message_id = get_most_recent_messsage_id(group_id)

	response = requests.get('https://api.groupme.com/v3/groups/' + str(group_id) + '/messages?token=' +
							auth_token + '&before_id=' + str(message_id) + '&limit=100')
	data = response.json()

	# see if member is in member_list
	i = 0
	while i < len(data['response']['messages']):
		# print str(data['response']['messages'][i]['user_id'])
		if is_in_list(data['response']['messages'][i]['user_id'], member_list):
				add_to_member(data['response']['messages'][i]['user_id'],
							  member_list,
							  len(data['response']['messages'][i]['favorited_by']))

		# Add new member to list
		else:
				try:
						member = {'name'       : str(data['response']['messages'][i]['name']),
								  'id'         : data['response']['messages'][i]['user_id'],
								  'total_likes': len(data['response']['messages'][i]['favorited_by']),
								  'total_posts': 1}
						print(member)
				except UnicodeEncodeError:  # Jovan exception - For anyone with a non Unicode character in their name.
						member = {'name'       : 'Non-Unicode Character In Name',
								  'id'         : data['response']['messages'][i]['user_id'],
								  'total_likes': len(data['response']['messages'][i]['favorited_by']),
								  'total_posts': 1}

				member_list.append(member)
		i += 1
	# recurse
	last_id = data['response']['messages'][i - 1]['id']
	try:
			get_member_list(group_id, last_id, member_list)
	except ValueError:
			print('Should be done')


def is_in_list(user_id, member_list):
	"""
	Checks if a member is in a list. Returns true if they are, returns false otherwise.
	"""
	i = 0
	while i < len(member_list):
			if user_id == member_list[i]['id']:
					return True
			i += 1
	return False


def add_to_member(user_id, member_list, count):
	"""
	Adds to the member's like count
	"""
	i = 0
	while i < len(member_list):
			if user_id == member_list[i]['id']:
					member_list[i]['total_likes'] += count
					member_list[i]['total_posts'] += 1
					return
			i += 1


def get_most_recent_messsage_id(group_id):
	"""
	Gets the most recent message ID
	"""
	response = requests.get('https://api.groupme.com/v3/groups/' + str(group_id) + '?token=' + auth_token)
	data = response.json()

	return data['response']['messages']['last_message_id']


def print_person(member):
	print("Name:", member['name'])
	total_likes = member['total_likes']
	total_posts = member['total_posts']
	print("\tTotal Likes:", str(total_likes))
	print("\tTotal Posts:", str(total_posts))
	print("\tAvg. Likes Per Post:", float(float(total_likes) / float(total_posts)))


def main():

	mem_list = []
	get_member_list(currentGM, 0, mem_list)

	# NOTE: I do not understand why this was written the way it was.
	# This seems horribly inefficient to me. Do I care enough to fix it
	# right now, though? Absolutely not.

	# Display the members with less than 10,000 likes.
	ranked_by_total_likes = []
	for i in reversed(range(10000)):
		if i == 0:
			break

		# Sort list in descending order of total likes.
		# TODO: Should really be using the built-in sorted function.
		j = 0
		while j < len(mem_list):
			if mem_list[j]['total_likes'] == i:
					ranked_by_total_likes.append(mem_list[j])
			j += 1

	[print_person(member) for member in ranked_by_total_likes]


if __name__ == "__main__":
	main()
