#!/bin/python
import github3
import string

def login():
    # Populate env token or use prompt
    # @TODO read from a config or env to pull token
    return github3.login(token='')

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

def get_starred_repos(gh):
    starred_repos = []
    login = gh.user().login
    for repo in gh.iter_starred():
        # Filter out your own repos (forked and private)
        if login != str(repo.owner):
            repo_string = '###%s (%d:star:)' % (repo.full_name, repo.stargazers)
            repo_string += '\r\n%s (%s)' % (repo.description.encode('ascii', 'ignore'), repo.html_url)
            starred_repos.append(repo_string)

    starred_repos = sorted(starred_repos)
    return starred_repos

class PercentTemplate(string.Template):
    delimiter = '%'

if __name__ == "__main__":
    with open('bookmark.template.md', 'r') as fr:
        content = fr.read()

    gh = login()
    starred_repos = get_starred_repos(gh)
    print "%d bookmarks are imported" % len(starred_repos)
    starred_repos = '\n'.join(starred_repos)
    bookmark_template = PercentTemplate(content)

    # @TODO need a better way
    with open('bookmark.md', 'w+') as fh:
        fh.write(bookmark_template.substitute(locals()))

    with open("bookmark.md", "r") as fh:
        create_or_use_repo(gh, fh.read())
