from typing import List

from github import Github

from lgtm import LGTMSite
import sys
import yaml


def create_github() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])


def get_languages() -> List[str]:
    default_languages: List[str] = [
        'Kotlin',
        'Groovy',
        'Java',
        'C#',
        'C',
        'C++',
        'Python',
        'Javascript',
        'TypeScript',
        'Go'
    ]

    # If the user does not want to follow repos using a specific language(s), we
    # follow all repos that are CodeQL supported instead.
    if len(sys.argv) >= 3:
        languages = sys.argv[2].split(',')
        formatted_languages = [language.capitalize() for language in languages]
        return formatted_languages
    else:
        return default_languages


def load_repository_list(org: str) -> List[str]:
    languages = get_languages()
    github = create_github()
    repos = github.get_organization(org).get_repos(type='public')

    repos_to_load: List[str] = []
    for repo in repos:
        if repo.archived or repo.fork:
            continue
        if repo.language in languages:
            print("Adding: " + repo.full_name)
            repos_to_load.append(repo.full_name)

    return repos_to_load


org_to_follow = sys.argv[1]
print('Following Org: %s' % org_to_follow)

repository_list = load_repository_list(org_to_follow)

site = LGTMSite.create_from_file()

for repo_name in repository_list:
    repo_url: str = 'https://github.com/' + repo_name
    print(repo_url)
    site.follow_repository(repo_url)
