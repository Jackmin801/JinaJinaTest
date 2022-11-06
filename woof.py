from jina import Client

c = Client(port=12345)
print(c.post("/"))