import argparse
import requests


def get_repos(user_name):
    '''In ra tat ca cac repo cua user_name'''
    url = 'https://api.github.com/users/{}/repos'.format(user_name)
    resp = requests.get(url)
    if resp.status_code == 200:
        repos = resp.json()
        names = [repo['name'] for repo in repos]
        return names
    else:
        return 'User\'s name is not exist'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name",
        help="use\'s name",
        type=str
        )
    arg = parser.parse_args().name
    print(get_repos(arg))


if __name__ == '__main__':
    main()
