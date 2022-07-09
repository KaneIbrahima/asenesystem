
import requests


def get_member_data(url):
    """View Instagram user follower count"""
    link = f'https://www.instagram.com/{url}/?__a=1'
    user = requests.get(link)
    return (user.json()['graphql']['user']['edge_followed_by']['count'])


def getname(url):
    """Split the URL from the username"""
    return url.split("instagram.com/")[1].replace("/", "")
