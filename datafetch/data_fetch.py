import time
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('GITHUB')

user_data_list = []
headers = {"Authorization": f'token {token}'}
for i in range(0,10000,100):
    print(i)
    urls = f'https://api.github.com/users?since={i}&per_page=100'
    response = requests.get(urls , headers=headers)
    data = response.json()
    user_urls = [each['url'] for each in data]
    print(user_urls)
    
    for user_url in user_urls:
        time.sleep(3)
        user_data = requests.get(user_url, headers=headers).json()
        user_repos_url = user_data['repos_url']
        print(user_repos_url)
        time.sleep(3)
        user_repos = requests.get(user_repos_url, headers=headers).json()
        user_login = user_data['login']
        user_id = user_data['id']
        print(user_id)
        user_name = user_data['name']
        user_email = user_data['email']
        user_twitter = user_data['twitter_username']
        user_public_repos = user_data['public_repos']
        user_forks = [each['forks'] for each in user_repos]
        try:
            average_user_forks = sum(user_forks) / len(user_forks)
        except ZeroDivisionError: 
            average_user_forks = 0
        user_followers = user_data['followers']
        user_following = user_data['following']
     
        user_dict = {
            'Login': user_login,
            'ID': user_id,
            'Name': user_name,
            'Email': user_email,
            'Twitter': user_twitter,
            'Followers': user_followers,
            'Following': user_following,
            'No of Repos':int(user_public_repos),
            'Fork_avg': average_user_forks
        }
        
        user_data_list.append(user_dict)

df = pd.DataFrame(user_data_list)

print(df)

df.to_csv("github_profiles.csv",index=False)