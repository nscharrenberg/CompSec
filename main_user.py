import user_c
import client

user = user_c.User("user1.json")


client.connect_to_server(user)
