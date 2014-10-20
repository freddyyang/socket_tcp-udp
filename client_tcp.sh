#! /bin/sh
set -e
if [ "$#" -ne 3 ] || ! [ -f "$2" ] ; then
    echo "Usage: $0 PORT CLIENTINPUT OUTPUTFILE" >&2
    exit 1
fi

#Start the client with the port ($1) and pipe in the commands ($2)
#Send output to $3
python client_python_tcp.py localhost $1 < $2 > $3 2>&1