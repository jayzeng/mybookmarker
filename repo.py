#!/bin/python
import github3
import string
import simplejson
import hashlib
import sys
import ConfigParser

CACHE_FILE = '.cache'

def login(config_reader):
    # Populate env token or use prompt
    # @TODO read from a config or env to pull token
    token = config_reader.get('github', 'token')
    return github3.login(token=token)

def create_or_use_repo(gh, bookmark_content):
    repo_name = "mybookmark"

    def update_bookmark(gh, repo, bookmark_content):
        readme_path = "README.md"

        # Retrieve README.md sha
        repo_inst = gh.repository(repo.owner, repo.name)

        # Update readme.md
        print "Updating bookmark"
        repo.update_file(readme_path, "update book marks", bookmark_content, repo_inst.contents(readme_path).sha)
        print "Done. See %s" % repo.html_url

    # See if rpeo already exists
    for repo in gh.iter_repos():
        if repo_name == repo.name:
            print "Updating README.md in %s (%s)" % (repo_name,repo.html_url )
            return update_bookmark(gh, repo, bookmark_content)

    # No repo yet, go ahead to create a repo
    repo = {}
    # Public repo
    repo["name"]        = repo_name
    repo["description"] = "My collection of useful bookmarks"
    repo["auto_init"]   = True

    res = gh.create_repo(**repo)
    if res:
       print("Created repo {0} successfully.".format(res.name))

    update_bookmark(gh, res, bookmark_content)

def get_starred_repos(gh, login):
    starred_repos = {}
    for repo in gh.iter_starred():
        # Filter out your own repos (forked and private)
        if login != str(repo.owner):
            starred_repos[repo.full_name] = '###%s (%d:star:)\r\n%s (%s)' %   \
                                            (repo.full_name, repo.stargazers, \
                                             repo.description.encode('ascii', 'ignore'), repo.html_url)

    return starred_repos

class Cache:
    def __init__(self,config_reader):
        self.cache_file = config_reader.get('caching', 'cache_file')
        self.is_cached_enabled = config_reader.getboolean('caching', 'enable_caching')

    def is_cached_enabled(self):
        return self.is_cached_enabled

    def has_cache(self,new_hash):
        import os
        if not os.path.exists(self.cache_file):
            return False

        with open(self.cache_file, 'r') as fr:
            content = fr.read();
            return content == new_hash

    def write_cache(self,new_hash):
        with open(self.cache_file, 'w') as fw:
            fw.write(new_hash)

class PercentTemplate(string.Template):
    delimiter = '%'

if __name__ == "__main__":
    with open('bookmark.template.md', 'r') as fr:
        content = fr.read()

    # init config parser and populates settings file
    config_reader = ConfigParser.ConfigParser()
    config_reader.read("settings.ini")

    gh = login(config_reader)
    login = gh.user().login
    starred_repos = get_starred_repos(gh, login)

    # Compute and compare json md5 hash to determine whether we have a new version
    starred_repos_json = simplejson.dumps(starred_repos)
    repos_hash = hashlib.md5(starred_repos_json).hexdigest()

    bookmark_cache = Cache(config_reader)

    # Caching is on and has Cache hit
    if bookmark_cache.is_cached_enabled and bookmark_cache.has_cache(repos_hash):
        sys.exit("No changes (starred repos) since last time")

    # store hash into local cache file
    bookmark_cache.write_cache(repos_hash)
    print "%d bookmarks are imported" % len(starred_repos)

    repos = ''
    for repo_str in starred_repos.values():
        repos += repo_str + '\r\n\r\n'

    bookmark_template = PercentTemplate(content)

    with open('bookmark.md', 'w+') as fh:
        fh.write(bookmark_template.substitute(starred_repos=repos))

    with open("bookmark.md", "r") as fh:
        create_or_use_repo(gh, fh.read())
