# ===== Name:  Freddy Yang =====
# ===== Perm#: 5516836 ===
# ===== CS176a HW1 ======
# ***** UDP_CLIENT ******
# ===== Referrence from: 1> http://www.binarytides.com/python-socket-server-code-example/
#                        2> https://www.youtube.com/watch?v=vNVMlXLGrTE
#                        3> https://wiki.python.org/moin/UdpCommunication


#!/usr/bin/python
import socket               # Import socket module
import sys
import pickle
from collections import OrderedDict

# HELPER FUNCTION: check if the inputting key is in the correct format
def checkValidKey(key):	      
	# Check validation of the key
	if ('?' in key) or ('=' in key) or ('\n' in key):   # check validation of key
		print >> sys.stderr, 'ERROR: Invalid command.'
		sys.stdout.flush()
		return False
	return True

# HELPER FUNCTION: Change the itemlized dict back to a normal order dict
def orderDictize(itemlized):
    orderDict = OrderedDict()
    for key,value in itemlized:                    # Change the itemlized dict back to a normal dict in order to add continuation key to it
        orderDict[key] = value
    return  orderDict

# HELPER FUNCTION: toggles the counter 
def toggle(counter):
  if counter == '1':
    return '0'
  return '1'

def receivingData (socket):
  recData, addr = socket.recvfrom(1024)
  return recData,addr

# HELPER FUNCTION: sends the smaller segment of the packet, which contains the ACK verification
def sendSeg (data,socket,address,counter):
  ACKreceived = False
  socket.sendto(counter+data, address)
  ACK = '0'
  for i in range (0,2):
      ACK,address = receivingData(socket)
      #print ('inside loop' + ACK)
      if ACK == '1':					#if the message sent is received
          #print ('sent onceeee')
          counter = toggle(counter)
          ACKreceived = True
          return True,counter
          break
      socket.sendto(counter+data,address)
      socket.settimeout(0.5)    # time out of 500ms
  if ACKreceived == False:
      print >> sys.stderr, "Failed to send message. Terminating"
      sys.stdout.flush()
      exit(1)

# HELPER FUNCTION: the main sending function which contains sending the length before sending the main body
def sendMessage (data,socket,address,counter):
  	length = sys.getsizeof(data)
  	length_str = str(length) 
  	#if length < 1024:
	ifSent, counter = sendSeg(length_str,socket,address,counter)
	if ifSent:
	  #print (length)
	  ifSent, counter = sendSeg(data,socket,address,counter)
	  #print ('test2')
	  return counter

	##
	# if length < 1024:
	# 	ifSent, counter = sendSeg(length_str,socket,address,counter)
	# 	if ifSent:
	# 	  #print (length)
	# 	  ifSent, counter = sendSeg(data,socket,address,counter)
	# 	  #print ('test2')
	# 	  return counter
	# else:
	# 	encode_data = data.encode('utf-8')
	# 	num = int(length)/1024 + 1
	# 	encode_data = [data[i:i+num] for i in range(0, len(data), num)]
	# 	for i in range (0,num):
	# 		sendSeg (encode_data[i],socket,address,counter)

# HELPER FUNCTION: received the message (length and body), also sends ACK to sender
def recMessage (socket):
  socket.settimeout(2)          # time out of 2000ms
  length,address = receivingData(socket)
  length_str = str(length[0:])
  ACK = '1'         # ACK: 1 for message received, 0 for vise versea
  #sendSeg(ACK,socket,host,port)
  socket.sendto(ACK,address)
  #print length_str
  recData,address = receivingData(socket)
  socket.sendto(ACK,address)
  counter = recData[0]
  recData = recData[1:]
  return recData, address, counter

##
# try:
	 #  if (int(length) > 1024):
	 #  		recStr = ''
	 #  		num = int(length)/1024 + 1
	 #  		for i in range(i,num):
	 #  			recData,address = receivingData(socket)
		# 		socket.sendto(ACK,address)
		# 		counter = recData[0]
		# 		recData = recData[1:]
	 #  			recStr += recData
	 #  		recData = recStr.decode('utf-8')
	 #  		if sys.getsizeof(recData) != length:
	 #  			print >> sys.stderr, 'ERROR: Failed to receive message. Terminating.'
		# 		sys.stdout.flush()
		# 		exit(1)
	 #  else:
	 #  	  recData,address = receivingData(socket)
		#   socket.sendto(ACK,address)
		#   recStr = ''
		#   counter = recData[0]
		#   recData = recData[1:]
  # except:
	 #  print >> sys.stderr, 'ERROR: Failed to receive message. Terminating.'
	 #  sys.stdout.flush()
	 #  exit(1)

# INITIALIZING, ARGV, and CONNECTING
host = str(sys.argv[1])		# host is 'localhost' as defined in server_python_tcp.py
port = int(sys.argv[2])
if (len(sys.argv) != 3):
	print >> sys.stderr, 'ERROR: Invalid number of args. Terminating.'									 #ERROR1
	sys.stdout.flush()
if ( port < 1024 or port > 49151):        #Registered Port range
        print >> sys.stderr, 'ERROR: Invalid port. Terminating.'        								 #ERROR2
        sys.stdout.flush()
        exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) #Create socket of udp


# WHILE LOOP ENSURE THE COMMUNICATING WITH CLIENT
counter = '0'
while True:
	valid = True
	key = ''
	sendData = raw_input()
	#print ('==================')
	#print ('test1')
	#counter = sendMessage(sendData,s,(host,port),counter)
	#s.sendto(sendData,(host,port))
	#print receivingData (s)

	# COMMAND: ?key
	if (sendData[0] == "?"):
		key = sendData[1:]
		# Check validation of the key
		valid = checkValidKey(key)
		if (valid == True):
			sendMessage(sendData,s,(host,port),counter)
			recData, address, counter = recMessage(s)
			print recData #Message(s)[0]
			sys.stdout.flush()

    # COMMAND: key=value 
	elif ('=' in sendData):
		# value equals everything after the 1st '='' 
		for i in range(0,len(sendData)):
			if (sendData[i] == '='):
				key = sendData[:i]
				break
		# Check validation of the key
		valid = checkValidKey(key)
		if (valid == True):
			sendMessage(sendData,s,(host,port),counter)
			print recMessage(s)[0]
			sys.stdout.flush()

	# COMMAND: list
	elif (sendData == 'list'):
		sendMessage(sendData,s,(host,port),counter)
		recData = recMessage(s)[0]
		recData = pickle.loads(recData)
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
			sendMessage(sendData,s,(host,port),counter)
			recData = pickle.loads(recMessage(s)[0])
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
			sendMessage(sendData,s,(host,port),counter)
			recData = recMessage(s)[0]
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
		sendMessage(sendData,s,(host,port),counter)
		s.close                     # Close the socket when done
		break
	else:
		print >> sys.stderr, 'ERROR: Invalid command.'
		sys.stdout.flush()
