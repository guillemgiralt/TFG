import threading
import time
import logging

class my_servo:

    def __init__ (self, name):
        self.name = name
        self.t    = None
        return
    
    def mymove(self, delay):
        logging.info("mymove start {} delay={}".format(self.name, delay))
        time.sleep(delay)
        logging.info("mymove finish {} delay={}".format(self.name, delay))
        
    def move(self, delay):
        logging.info("move {} start".format(self.name))
        self.t = threading.Thread(target=self.mymove, args=(delay,))
        self.t.start()
        logging.info("move {} finish".format(self.name))

    def wait(self):
        logging.info("wait {} start".format(self.name))
        self.t.join()
        logging.info("wait {} finish".format(self.name))


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    z = my_servo("servo1")
    z.move(1.0)

    x = my_servo("servo2")
    x.move(6.0)
    
    y = my_servo("servo3")
    y.move(7.0)

    y.wait()
    z.wait()
    x.wait()
    
    

