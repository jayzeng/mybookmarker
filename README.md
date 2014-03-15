mybookmarker
============
![MyBookMarker](https://cdn1.iconfinder.com/data/icons/meBaze-Freebies/32/add-address.png)
The idea is simple: pull all starred repos and convert them into another repoistory on Github

Project setup:
(If virtualenvwrapper is not installed)
```
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ source /usr/local/bin/virtualenvwrapper.sh
```

1. Create a virtual env
```
mkvirtualenv mybookmarker
```

2. Switch on to virtual env
```
workon mybookmarker
```

3. Install dependencies
```
pip install github3.py
```

4. Take a snapshot of requirements
```
$ pip freeze > requirements.txt
```

(Replicate requirements)
```
$ pip install -r requirements.txt
```


# Create a token
- Create new token https://github.com/settings/tokens/new
- Give it an app name
- Put the token in github section in settings.ini
- Mybookmarker only need "public_repo" access, it is recommended that you remove the rest of privilages to better protect yourself. 


# Customize template? 
Easy, modify base template (https://github.com/jayzeng/mybookmarker/blob/master/bookmark.template.md). It is a mark down file, customize it in the way you want. 

Note: ```%starred_repos``` is the variable for all your starred repositories. 

# How to run?
python repo.py

# Example
https://github.com/jayzeng/mybookmark
