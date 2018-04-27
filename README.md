# cache

Basically everything is Open Source, except for FontAwesome pro, which would need to be replaced with a free version if this project is reused. Check the FontAwesome licence before continuing.

```
source /usr/lib/ckan/default/bin/activate

paster serve /etc/ckan/default/development.ini
```

```
virtualenv -p python3 --no-site-packages venv_cache
```


/opt/django/cache/
/opt/django/venv_cache/

### CKAN settings

Create a local_settings.py file, next to settings.py, and add (assuming nginx is setup as such)

```
ckan_url = 'http://localhost/ckan'
```

## FAQ

### Connection aborted.', BadStatusLine("''",)
ckan library is trying to read the public uwsgi endpoint at localhost:5000, instead of http://localhost/ckan