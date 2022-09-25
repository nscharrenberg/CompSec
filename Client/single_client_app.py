import user_c
import client

user = user_c.User("json_files/singe.json")
client.connect_to_server(user)