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
      if ACK == '1':          #if the message sent is received
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
  ##
  # if length < 1024:
  #   ifSent, counter = sendSeg(length_str,socket,address,counter)
  #   if ifSent:
  #     #print (length)
  #     ifSent, counter = sendSeg(data,socket,address,counter)
  #     #print ('test2')
  #     return counter
  # else:
  #   encode_data = data.encode('utf-8')
  #   num = int(length)/1024 + 1
  #   encode_data = [data[i:i+num] for i in range(0, len(data), num)]
  #   for i in range (0,num):
  #     sendSeg (encode_data[i],socket,address,counter)


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

# HELPER FUNCTION: received the message (length and body), also sends ACK to sender
def recMessage (socket):
  #socket.settimeout(2)          # time out of 2000ms, used on the client side
  length,address = receivingData(socket)
  ACK = '1'         # ACK: 1 for message received, 0 for vise versea
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
   #      recStr = ''
   #      num = int(length)/1024 + 1
   #      for i in range(i,num):
   #        recData,address = receivingData(socket)
    #     socket.sendto(ACK,address)
    #     counter = recData[0]
    #     recData = recData[1:]
   #        recStr += recData
   #      recData = recStr.decode('utf-8')
   #      if sys.getsizeof(recData) != length:
   #        print >> sys.stderr, 'ERROR: Failed to receive message. Terminating.'
    #     sys.stdout.flush()
    #     exit(1)
   #  else:
   #      recData,address = receivingData(socket)
    #   socket.sendto(ACK,address)
    #   recStr = ''
    #   counter = recData[0]
    #   recData = recData[1:]
  # except:
   #  print >> sys.stderr, 'ERROR: Failed to receive message. Terminating.'
   #  sys.stdout.flush()
   #  exit(1)



# HELPER FUNCTION: sending data during command: listc
def sendListc(newKeypairs,conKey,s,address,counter):
    tempKeypairs = orderDictize(newKeypairs)         # Change the itemlized dict back to a normal dict in order to add continuation key to it
    tempKeypairs['continuation?Key'] = conKey        # Pass the continuation key to the client by having it attached to the \
                                                     # dictionary. To prevent it from conflicting with a possible user input of key,\
                                                     # the key of it is set to 'continuation?key', which makes it impossible \
                                                     # to be a normal key because of '?' in it
    sendData = pickle.dumps(tempKeypairs)            # Serialize the tempKeypairs and send it through the socket
    sendMessage(sendData,s,address,counter)


# INITIALIZING, ARGV, and CONNECTING
keypairs = {}
keypairs_order = OrderedDict()
port = int(sys.argv[1])
host = 'localhost'

if (len(sys.argv) != 2):
    print >> sys.stderr,'ERROR: Invalid number or args. Terminating.'                  #ERROR1
    sys.stdout.flush()
if ( port < 1024 or port > 49151):        #Registered Port range
         print >> sys.stderr,'ERROR: Invalid port. Terminating.'                        #ERROR2
         sys.stdout.flush()
         exit(1)

# CONNECTING and BINDING PORT
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) #Create socket of udp
                              #host = socket.gethostname()+'.local'  # Get local machine name
try:
  s.bind((host, port))        # Bind to the port
except:
  print >> sys.stderr, 'ERROR: Could not bind port. Terminating.'   #ERROR4
  sys.stdout.flush()
  exit(1)

# WHILE LOOP TO ENSURE THE COMMUNICATION WITH CLIENT
while True:
  while True:                   
    valid = True
    recData,address, counter = recMessage(s)
    #print ('counter::::::' + counter)
      #recData = receivingData(s)
      #recData, addr = s.recvfrom(1024)
    recData = str(recData)
    #print 'sent'
    # sendMessage('test',s,host,port)
    #print recData
    #print 'hello'
    #print recData[0]

    # COMMAND: ?key
    if (recData[0] == '?'):      # command: ?key
        key = recData[1:]
        if key in keypairs:
          sendMessage(key + '=' + keypairs[key],s,address,counter)
        else:
          sendMessage(key + '=',s,address,counter)

    # COMMAND: key=value 
    elif ('=' in recData):
        for i in range(0,len(recData)):
          if (recData[i] == '='):
            value = recData[i+1:]
            key = recData[:i]
            keypairs[key]=value
            keypairs_order = OrderedDict(sorted(keypairs.items(), key=lambda t: t[0]))   # order the dict aphabatically
            break
        sendMessage('OK',s,address,counter)
        continue

    # COMMAND: list
    elif (recData == 'list'):
        sendData = pickle.dumps(keypairs_order)             # use Pickle library to pack dictionary and send it via the socket
        sendMessage(sendData,s,address,counter)
        continue

    # COMMAND: listc 
    elif ('listc' in recData):
      _split = recData.split(' ')
      len_keypairs=len(keypairs_order.items())

      # COMMAND: listc num
      if (len(_split) == 2):                                   # if listc num
          num = int(_split[1])
          # If num is more than index then:
          if (num >= len_keypairs):
              newKeypairs = keypairs_order.items()[:num]       # Itemlize the keypair dictionary and set it to the first n numbers of pairs
              sendListc(newKeypairs,'END',s,address,counter)
              continuationKey = 'END'
          else:
              conKey = str(num)
              newKeypairs = keypairs_order.items()[:num]       # Itemlize the keypair dictionary and set it to the first n numbers of pairs
              sendListc(newKeypairs,conKey,s,address,counter)
              continuationKey = conKey

      # COMMAND: listc num conKey
      elif (len(_split) == 3):                                 # if listc num conKey
          num = int(_split[1])
          conKey_in = int(_split[2])
          conKey_in_str = str(conKey_in)
          # Detects whether conKey is a valid conkey (whether it is the stored conKey)
          if (conKey_in_str != continuationKey):
              sendData = 'BAD KEY'
              sendMessage(sendData,s,address,counter)
          # If conKey is valid:
          else:
              continuationKey = int(num+conKey_in)
              if (num > len_keypairs):
                  newKeypairs = keypairs_order.items()[:num]       # Itemlize the keypair dictionary and set it to the first n numbers of pairs
                  continuationKey = 'END'
                  sendListc(newKeypairs,continuationKey,s,address,counter)
              else:
                  if (continuationKey >= len_keypairs):   # set outputing continuation key to END when it gets to the end of the keypairs
                      continuationKey = 'END'
                  # elif(conKey_out > len_keypairs):
                  #     conKey_out = 'END'
                  else:
                      continuationKey = str(num+conKey_in)
                  newKeypairs = keypairs_order.items()[conKey_in:num+conKey_in]   # Itemlize the keypair dictionary and set it to the first n numbers of pairs
                  sendListc(newKeypairs,continuationKey,s,address,counter)

    # COMMAND: exit
    elif (recData == 'exit'):
        s.close
        break
