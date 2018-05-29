import os

import requests
from django.utils.text import slugify


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cache.settings")

import django
django.setup()

from wiki.models import URLPath
from wiki.views.accounts import User
from housing_portal import models


class WikiPop:
    def __init__(self):
        pass

    def create_article(self, parent_path, title, slug, content, message, user=None):
        parent = URLPath.get_by_path(parent_path)

        # title = 'This is article ONE'
        # slug = slugify(title)
        # content = 'body text etc'
        # message = 'user message??'

        if not user:
            user = User.objects.get(id=1)

        try:
            newpath = URLPath.create_urlpath(
                parent,
                slug,
                title=title,
                content=content,
                user_message=message,
                user=user,
                ip_address="127.0.0.1",
                article_kwargs={'owner': user,
                                'group': None,
                                'group_read': True,
                                'group_write': True,
                                'other_read': False,
                                'other_write': False,
                                })
            return newpath
        except Exception as e1:
            print(e1)

        return None

    def add_all_datasets(self):

        all_packages = requests.get('http://localhost:5000/api/3/action/package_search?facet.limit=1000&rows=1000')
        json_blob = all_packages.json()
        cache_surveys = json_blob['result']['results']

        for cs in cache_surveys:
            print('Adding', cs['name'])
            self.create_article(
                '',
                cs['title'],
                cs['name'],
                cs['notes'],
                ''
            )


if __name__ == '__main__':
    wiki_pop = WikiPop()
    wiki_pop.add_all_datasets()
