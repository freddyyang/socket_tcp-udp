#! /bin/sh
set -e
if [ "$#" -ne 2 ] ; then
    echo "Usage: $0 PORT OUTPUTFILE" >&2
    exit 1
fi

#Start the server with the port ($1)
#Send output to $2
python server_python_tcp.py $1 > $2 2>&1 &

echo $!
#Save its PID so we can kill it after we run the server.

