# ***** TCP_CLIENT ******
# ===== Referrence from: 1> http://www.binarytides.com/python-socket-server-code-example/
#                        2> http://www.tutorialspoint.com/python/python_networking.htm
#                        3> https://wingware.com/psupport/python-manual/2.5/lib/socket-example.html
#						 4> http://www.jroller.com/RickHigh/entry/notes_on_creating_a_socket


#!/usr/bin/python
import socket               # Import socket module
import sys
import pickle
from collections import OrderedDict

# HELPER FUNCTION_ check if the key is in the correct format
def checkValidKey(key):
	# Check validation of the key
	if ('?' in key) or ('=' in key) or ('\n' in key):   # check validation of key
		print >> sys.stderr, 'ERROR: Invalid command.'
		sys.stdout.flush()
		return False
	return True

# INITIALIZING, ARGV, and CONNECTING
host = str(sys.argv[1])		# host is 'localhost' as defined in server_python_tcp.py
port = int(sys.argv[2])
if (len(sys.argv) != 3):
	print >> sys.stderr,'ERROR: Invalid number or args. Terminating.' 								 #ERROR1
	sys.stdout.flush()
if ( port < 1024 or port > 49151):        #Registered Port range
        print >> sys.stderr, 'ERROR: Invalid port. Terminating.'        								 #ERROR2
        sys.stdout.flush()
        exit(1)

s = socket.socket()        			# Create a socket object

try:
	s.connect((host, port))
	print ('Connected.')
	sys.stdout.flush()
except:
	print >> sys.stderr, "ERROR: Could not connect to server. Terminating."
	sys.stdout.flush()


# WHILE LOOP TO ENSURE THE COMMUNICATION WITH CLIENT
while True:
	valid = True
	key = ''
	sendData = raw_input()

	# COMMAND: ?key
	if (sendData[0] == "?"):
		key = sendData[1:]
		# Check validation of the key
		valid = checkValidKey(key)
		if (valid == True):
			s.send(sendData)
			print s.recv(1024)
			sys.stdout.flush()

    # COMMAND: key=value 
	elif ('=' in sendData):
		for i in range(0,len(sendData)):
			if (sendData[i] == '='):
				key = sendData[:i]
				break
		# Check validation of the key
		valid = checkValidKey(key)
		if (valid == True):
			s.send(sendData)
			print s.recv(1024)
			sys.stdout.flush()

	# COMMAND: list
	elif (sendData == 'list'):
		s.send(sendData)
		recData = pickle.loads(s.recv(1024))
		tempKeypairs = recData.items()
		for key,value in tempKeypairs:
			print (key+'='+value)
			sys.stdout.flush()
		continue

	# COMMAND: listc 
	elif ('listc' in sendData):
		_split = sendData.split(' ')
		# CHECK FORMAT ERRORS
		if (len(_split) > 3) or ('?' in sendData) or ('=' in sendData) or ('\n' in sendData):
			print >> sys.stderr, 'ERROR: Invalid command.'
			sys.stdout.flush()
			continue

		# COMMAND: listc num
		elif (len(_split) == 2):
			s.send(sendData)
			recData = pickle.loads(s.recv(1024))
			conKey = recData['continuation?Key']	# Retrive the continuation key
			recData.pop('continuation?Key')		 	# Delete the continuation key from the attaching dictionary
			recData = recData.items()				
			for key,value in recData:
				print (key+'='+value)
				sys.stdout.flush()
			print str(conKey)
			sys.stdout.flush()

		# COMMAND: listc num conKey
		elif (len(_split) == 3):
			s.send(sendData)
			recData = s.recv(1024)
			if ( recData == 'BAD KEY'):
				print >> sys.stderr, 'ERROR: Invalid continuation key.'
				sys.stdout.flush()
			else:
				recData = pickle.loads(recData)
				conKey = recData['continuation?Key']	# Retrive the continuation key
				recData.pop('continuation?Key')		 	# Delete the continuation key from the attaching dictionary
				recData = recData.items()				
				for key,value in recData:
					print (key+'='+value)
					sys.stdout.flush()
				print str(conKey)
				sys.stdout.flush()
		else:
			print >> sys.stderr,'ERROR: Invalid command.'
			sys.stdout.flush()


	# COMMAND: help
	elif (sendData == 'help'):
	  print('Commands: ?key, key=, list, listc, num, listc num continuationkey, exit, help')
	  sys.stdout.flush()

	# COMMAND: exit
	elif (sendData == 'exit'):
		s.send(sendData)
		s.close                     # Close the socket when done
		break

	else:
		print >> sys.stderr,'ERROR: Invalid command.'
		sys.stdout.flush()
