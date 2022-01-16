from django.core.cache import cache

cache.set('my_key', 'hello, world!', 30)
print(cache.get('my_key'))

d = input('name ')