import requests
from tabulate import tabulate
from bs4 import BeautifulSoup

home_url = 'https://www.codechef.com'
base_url = 'https://www.codechef.com/users/'

list_len_3 = ['JAN', 'FEB', 'MAY', 'AUG', 'OCT', 'NOV', 'DEC']
list_len_4 = ['JUNE', 'JULY', 'SEPT']
list_len_5 = ['MARCH', 'APRIL']

def print_user_data(user):
	print('Name: ' + user['name'])
	print('Summary of Long Challenges')
	print('\n')
	headers = ["Problem", user['name'].split()[0] +  "'s Submission"]
	for challenge in user['challenges']:
		print(challenge['name'] + ', Problem Count: ' + str(challenge['count']))
		print("\n")
		table = []
		for question in challenge['questions']:
			que_row = []
			que_row.append(question['name'])
			que_row.append(question['url'])
			table.append(que_row)
		t = tabulate(table, headers, tablefmt="fancy_grid")
		print(t)
		print("\n")

def extract_user_data():
	while(True):
		user = {}
		print("Enter the username you want to stalk")
		username = input()
		response = requests.get(base_url+username)
		soup = BeautifulSoup(response.text,'lxml')
		profile_name = soup.find('div',{'class':'profile'}).find('div',{'class':'user-name-box'}).text
		category_list = soup.find('div',{'class':'profile'}).findAll('table')[1].findAll('tr')[7].findAll('td')[1].findAll('p')[::-1] #Reversing the list to get recent 10 long challenges.
		if not category_list:
			category_list = soup.find('div',{'class':'profile'}).findAll('table')[1].findAll('tr')[8].findAll('td')[1].findAll('p')[::-1]
		list_challenges = []
		for	item in category_list:
			challenge = {}
			flag = False
			challenge_name = item.find('b').text
			if len(challenge_name) == 5:
				if any(challenge_name[:3] in x for x in list_len_3):
					challenge_name = challenge_name
					flag = True
			elif len(challenge_name) == 6:
				if any(challenge_name[:4] in x for x in list_len_4):
					challenge_name = challenge_name
					flag = True
			elif len(challenge_name) == 7:
				if any(challenge_name[:5] in x for x in list_len_5):
					challenge_name = challenge_name
					flag = True
			if flag:
				list_question = []
				list_1 = item.find('span').findAll('a')
				for i in list_1:
					ques_data={}
					q_name = i.text
					q_url = i['href']
					ques_data = {
						'name': q_name,
						'url': home_url + q_url,
					}
					list_question.append(ques_data)
				challenge = {
					'name': challenge_name,
					'questions': list_question,
					'count': len(list_question),
				}
				list_challenges.append(challenge)
		user = {
			'name': profile_name,
			'challenges': list_challenges,
		}
		print_user_data(user)
		print("Do you wish to stalk more? Enter 'Y' for more and any other key for quitting")
		inp = input()
		if inp == 'y' or inp == 'Y':
			pass
		else:
			print("Thank You!")
			break

extract_user_data();










