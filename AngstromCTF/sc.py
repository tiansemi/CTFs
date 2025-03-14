#!/usr/bin/env python3
#
	# import socket

	# s = socket.socket()
	# host = 'challs.actf.co'
	# port = 31402

	# s.connect((host, port))
	# msg = ''
	# # while msg != "quit":
	# #		msg = s.recv(1024).decode('utf-8')
	# #     print("SERVER: {}".format(msg))
	# #     if msg != '':
	# #         s.send(b"Message Recieved")

	# msg = s.recv(1024).decode('utf-8')
	# print("SERVER: {}".format(msg))
	# print(s.send(b"Message"))
	# msg = s.recv(1024).decode('utf-8')
	# print("SERVER: {}".format(msg))

	# s.close()
	# print("Disconnected from server")


def fake_psi(a, b):
    return [i for i in a if i in b]

def zero_encoding(x, n):
    ret = []

    for i in range(n):
        if (x & 1) == 0:
            ret.append(x | 1)
        x >>= 1

    return ret

def one_encoding(x, n):
	ret = []

	for i in range(n):
		if x & 1:
			ret.append(x)
		x >>= 1

	return ret

x=214785822366985585484894968498498498498484984984
y=2

if len(fake_psi(one_encoding(x, 64), zero_encoding(y, 64))) == 0 and x > y and x > 0 and y > 0:
	print('COOl')

a=one_encoding(x, 64)
b=zero_encoding(y, 64)
print("a = ",a,"\n\nb = ",b,"\n\nlen fake = ",len(fake_psi(a,b)))