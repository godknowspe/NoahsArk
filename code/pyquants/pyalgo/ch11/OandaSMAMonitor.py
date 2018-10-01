#
# Python Script
# for Real-Time Monitoring
# via Socket
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://46.101.3.206:5555')  # adjust to remote IP
socket.setsockopt_string(zmq.SUBSCRIBE, 'SMA')  # channel is SMA

while True:
    msg = socket.recv_string()
    print(msg)
