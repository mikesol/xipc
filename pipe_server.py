import os
import select
from message import decode_msg_size

def get_message(fifo: int) -> str:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size).decode("utf8")
    return msg_content

def get_reader_writer():
    fd_read, fd_write = os.pipe()
    return fd_read, fd_write, os.fdopen(fd_read, 'r')

if __name__ == "__main__":
    # Make the named pipe and poll for new messages.
    rd, wt, rdr = get_reader_writer()
    with open('.pid', 'w') as x:
        x.write(str(wt))
    try:
        try:
            # Create a polling object to monitor the pipe for new data
            poll = select.poll()
            poll.register(rdr, select.POLLIN)
            try:
                while True:
                    # Check if there's data to read. Timeout after 2 sec.
                    if (rdr, select.POLLIN) in poll.poll(2000):
		    	# Do something with the message
                        msg = get_message(rdr)
                        print(msg)
                    else:
		    	# No data, do something else
                        print("Nobody here :(")
            finally:
                poll.unregister(rdr)
        finally:
            os.close(rdr)
    finally:
    	pass
