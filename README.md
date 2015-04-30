# socket_tcp-udp
A network socket containing a server and a client, implemented using Python in both TCP and UDP ways. There will be 4 commands supported: get, put, list, and listc.

Client Input/Output Example

csil-machine2> client 128.163.7.19 3300 Optimus 
Connected. 
?apple 
apple= 
apple=hello 
OK 
?= 
ERROR: Invalid command. 
?apple 
apple=hello 
key2=this is a test 
OK 
list 
apple=hello 
key2=this is a test 
key4=blob 
OK 
listc 1 
apple=hello 
1 
listc 1 1 
key2=this is a test 
2 
listc 1 2 
key4=blob 
END 
listc 1 23 
ERROR: Invalid continuation key. 
exit 
csil-machine2>
