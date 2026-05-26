"""
Coletar

"""

import redis

r = redis.Redis(
    host="street-macrosleek-debt-10830.db.redis.io",
    port=12096,
    decode_responses=True,
    username="default",
    password="kDNXskec3eXyFSU4PfOyEKRVDl7X5iLr",
)

success = r.set("foo", "bar")
# True

result = r.get("teste")
print(result)
success = r.set("teste", "testeeee")
# >>> bar
