import user_c
import client

user = user_c.User("json_files/user0.json")
client.connect_to_server(user)