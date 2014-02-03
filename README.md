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
- Give it a app name
- Register the token as an environmental variable

# Example
https://github.com/jayzeng/mybookmark
