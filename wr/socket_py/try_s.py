from jsonsocket import Client, Server

host = 'localhost'
port = '8000'



# Server code:
server = Server(host, port)
server.accept()
data = server.recv()
# data now is: {'some_list': [123, 456]}
server.send({'data': data}).close()