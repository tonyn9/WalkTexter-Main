from bluetoothConnect import *
from sensor import *

# ultrasonic sensor setup
sensor = sensor()

# camera setup

#bluetooth setup
bltSoc = bluetoothConnect()

if __name__ == '__main__':
 
    try :
        while True:
            if sensor.detectObst():
            	# prepare the string to send
            	data = ******
            	bltSoc.send(data)  
            
    except (IOError) as err:
        pass
        
    except (KeyboardInterrupt):
        print "disconnected"
        bltSoc.close()
        print "all done"
    finally:
        sensor.close()