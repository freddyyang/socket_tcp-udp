# ===== Name:  Freddy Yang =====
# ===== Perm#: 5516836 ===
# ===== CS176a HW1 ======
# ***** TCP_SERVER ******
# ===== Referrence from: 1> http://www.binarytides.com/python-socket-server-code-example/
#                        2> http://www.tutorialspoint.com/python/python_networking.htm
#                        3> https://wingware.com/psupport/python-manual/2.5/lib/socket-example.html
#                        4> http://www.jroller.com/RickHigh/entry/notes_on_creating_a_socket


#!/usr/bin/python             # This is server.py file
import socket                 # Import modules
import sys
import pickle
from collections import OrderedDict

# HELPER FUNCTION: Change the itemlized dict back to a normal order dict
def orderDictize(itemlized):
    orderDict = OrderedDict()
    for key,value in itemlized:                    # Change the itemlized dict back to a normal dict in order to add continuation key to it
        orderDict[key] = value
    return  orderDict


# HELPER FUNCTION: sending data during command: listc
def sendListc(newKeypairs,conKey):
    tempKeypairs = orderDictize(newKeypairs)         # Change the itemlized dict back to a normal dict in order to add continuation key to it
    tempKeypairs['continuation?Key'] = conKey        # Pass the continuation key to the client by having it attached to the \
                                                     # dictionary. To prevent it from conflicting with a possible user input of key,\
                                                     # the key of it is set to 'continuation?key', which makes it impossible \
                                                     # to be a normal key because of '?' in it
    sendData = pickle.dumps(tempKeypairs)            # Serialize the tempKeypairs and send it through the socket
    con.send(sendData)



# main()
# INITIALIZING, ARGV, and CONNECTING
keypairs = {}
keypairs_order = OrderedDict()
continuationKey = ''

port = int(sys.argv[1])

if (len(sys.argv) != 2):
  print >> sys.stderr,'ERROR: Invalid number or args. Terminating.'                  #ERROR1
  sys.stdout.flush()
if ( port < 1024 or port > 49151):        #Registered Port range
        print >> sys.stderr, 'ERROR: Invalid port. Terminating.'        								 #ERROR2
        sys.stdout.flush()
        exit(1)

# CONNECTING and BINDING PORT
s = socket.socket()           # Create a socket object
                              #host = socket.gethostname()+'.local'  # Get local machine name
try:
  s.bind(('localhost', port))        # Bind to the port
except:
  print >> sys.stderr,'ERROR: Could not bind port. Terminating.'   #ERROR4
  sys.stdout.flush()
  exit(1)


s.listen(5)                   # Now wait for client connection.

# WHILE LOOP TO ENSURE THE COMMUNICATION WITH CLIENT
while True:                   # Two While loops to ensure the data being received relentlessly until command "exit" happens
  con, addr = s.accept()      # Establish connection with client.
  # if not data: break   #ERROR handling
  # O c.send('Thank you for connecting')
  while True:                    
    valid = True
    recData = con.recv(1024)
    
    # COMMAND: ?key
    if (recData[0] == "?"):      # command: ?key
        key = recData[1:]
        if key in keypairs:
          con.send(key + '=' + keypairs[key])
        else:
          con.send(key + '=')

    # COMMAND: key=value 
    elif ('=' in recData):
        for i in range(0,len(recData)):
          if (recData[i] == '='):
            value = recData[i+1:]
            key = recData[:i]
            keypairs[key]=value
            keypairs_order = OrderedDict(sorted(keypairs.items(), key=lambda t: t[0]))   # order the dict aphabatically
            break
        con.send('OK')
        continue

    # COMMAND: list
    elif (recData == 'list'):
        sendData = pickle.dumps(keypairs_order)             # use Pickle library to pack dictionary and send it via the socket
        con.send(sendData)
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
              sendListc(newKeypairs,'END')
              continuationKey = 'END'
          else:
              conKey = str(num)
              newKeypairs = keypairs_order.items()[:num]       # Itemlize the keypair dictionary and set it to the first n numbers of pairs
              sendListc(newKeypairs,conKey)
              continuationKey = conKey

      # COMMAND: listc num conKey
      elif (len(_split) == 3):                                 # if listc num conKey
          num = int(_split[1])
          conKey_in = int(_split[2])
          conKey_in_str = str(conKey_in)
          # Detects whether conKey is a valid conkey (whether it is the stored conKey)
          if (conKey_in_str != continuationKey):
              sendData = 'BAD KEY'
              con.send(sendData)
          # If conKey is valid:
          else:
              continuationKey = int(num+conKey_in)
              if (num > len_keypairs):
                  newKeypairs = keypairs_order.items()[:num]       # Itemlize the keypair dictionary and set it to the first n numbers of pairs
                  continuationKey = 'END'
                  sendListc(newKeypairs,continuationKey)
              else:
                  if (continuationKey >= len_keypairs):   # set outputing continuation key to END when it gets to the end of the keypairs
                      continuationKey = 'END'
                  # elif(conKey_out > len_keypairs):
                  #     conKey_out = 'END'
                  else:
                      continuationKey = str(num+conKey_in)
                  newKeypairs = keypairs_order.items()[conKey_in:num+conKey_in]   # Itemlize the keypair dictionary and set it to the first n numbers of pairs
                  sendListc(newKeypairs,continuationKey)

    elif (recData == 'exit'):
        con.close
        break