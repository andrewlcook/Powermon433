import serial
import time
import httplib, urllib   # http and url libs used for HTTP POSTs
import socket            # socket used to get host name/IP


server = "data.sparkfun.com" # base URL of your feed
publicKey = "pw3V5x60GDu56ERLQg7w" # public key, everyone can see this
privateKey = "64Eb7DlJoKUvzMpNaj5k"  # private key, only you should know
fields = ["power", "temp"] # Your feed's data fields
count = 0


try:
    while 1:
        ser = serial.Serial(port='/dev/ttyACM0',baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=40)
        print("connected to: " + ser.portstr)
        crap=ser.readline() #first line is junk
        while count < 240:	
            count = count + 1
	    params=ser.readline()
            if params:
            	print("Sending an update!")
            	print count
            	# Now we need to set up our headers:
            	headers = {} # start with an empty set
            	# These are static, should be there every time:
            	headers["Content-Type"] = "application/x-www-form-urlencoded"
            	headers["Connection"] = "close"
            	headers["Content-Length"] = len(params) # length of data
            	headers["Phant-Private-Key"] = privateKey # private key header

            	# Now we initiate a connection, and post the data
            	c = httplib.HTTPConnection(server)
            	# Here's the magic, our reqeust format is POST, we want
            	# to send the data to data.sparkfun.com/input/PUBLIC_KEY.txt
            	# and include both our data (params) and headers
            	c.request("POST", "/input/" + publicKey + ".txt", params, headers)
            	r = c.getresponse() # Get the server's response and print it
            	print r.status, r.reason
	    else:
		print("Error nothing sent")	
            time.sleep(1) # delay for a second
        ser.close()
        count = 0
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
       ser.close()
