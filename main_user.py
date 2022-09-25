import user_c
import client


users = []

max = 10

for i in range(0, max):
    users.append(user_c.User("json_files/user" + i + ".json"))

for user in users:
    client.connect_to_server(user)
