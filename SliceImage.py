
import threading, socket, time, random
from PIL import Image, ImageGrab
import pickle
import zlib
from MyCrypto import *


ERROR_SOCKET = "Socket_Error"
END_LINE = "\r\n"
LEN_UNIT_BUF = 2048
ERROR_EXCEPT = "Exception"

class SliceImage(threading.Thread):   
    clientIp = None
    stopIP = None
    stopBroadcast = None
    NewClient = 0



    def __init__(self, python_server, name_image):
        threading.Thread.__init__(self)
        self.python_server = python_server
        self.name_image = name_image
        self.form = python_server.slicemode
        self.formation = {'snake': self.Snake, 'square': self.Square, 'BtB': self.BtB}

    # sending picture to client
    def send_image(self,picture, ip):
        self.clientIp = ip
        image = {'pixels': picture.tostring(), 'size': picture.size, 'mode': picture.mode}
        compressed = zlib.compress(str(image))
        data = pickle.dumps(compressed)
        len_image = str(len(data) + len('\r\n'))
        print len_image
        self.python_server.checked_clients[ip].send(len_image)
        ack1 = self.python_server.checked_clients[ip].recv_buf() 
        self.python_server.checked_clients[ip].clientSock.send(data + '/r/n')
        ack2 = self.python_server.checked_clients[ip].recv_buf()

    # closing all clients
    def close_all_clients(self):
        for client in self.python_server.open_clients.values():
            client.send("Stop")
            client.clientSock.close()
        self.python_server.open_clients.clear()
        self.python_server.checked_clients.clear()

    # close client with IP = stopIP
    def close_client(self):
        self.python_server.open_clients[self.stopIP].send("Stop")
        self.python_server.open_clients[self.stopIP].clientSock.close()
        delself.python_server.open_clients[self.stopIP]
        delself.python_server.checked_clients[self.stopIP]
        self.stopIP = None

    # stop broadcasting to checked clients
    def stop_broadcasting(self):
        for client in self.python_server.checked_clients.values():
                    client.send("StopBroadcast")

    # the main thread function
    def run(self): 
        while True:
            if self.stopIP != None:
                if self.stopIP == '255.255.255.255':
                    self.close_all_clients()
                    break
                else:
                    self.close_client()
                    continue
            if self.stopBroadcast == True:
                self.stop_broadcasting()
                break
            if len(self.python_server.checked_clients) == 0 :
                continue
            
            try:
                if self.name_image == "screen":
                    picture = ImageGrab.grab()  #  PrintScreen
                    for ip in self.python_server.checked_clients.keys():
                        self.send_image(picture, ip)
                ###else:
                    #### TBD if self.NewClient == len(self.python_server.checked_clients):
                    ####    continue
                self.NewClient = len(self.python_server.checked_clients)
                picture = Image.open(self.name_image) # open image from file and not from the screen
                if len(self.python_server.checked_clients) > 1: #if we send to more than one client, slice the picture to the number of the clients
                    list_images = self.Slice(picture, len(self.python_server.checked_clients), self.formation[self.form])
                    ind = 0
                    for ip in self.python_server.checked_clients.keys():
                        print'sending data to client No %s' % str(ind+1)
                        self.send_image(list_images[ind], ip)
                        ind += 1
                else:
                    self.send_image(picture, self.python_server.checked_clients.keys()[0])
            except socket.error , e:
                print str(e) + END_LINE + ERROR_SOCKET 
                self.python_server.open_clients[self.clientIp].clientSock.close()
                self.python_server.gui.guiSock.send("Disconnected#" + self.python_server.open_clients[self.clientIp].addr[0])   # to GUI 
                del self.python_server.open_clients[self.clientIp] # delete the problemtaic client
                del self.python_server.checked_clients[self.clientIp]
                continue
            except Exception as e:
                print str(e) + END_LINE + ERROR_EXCEPT   
                continue

    def NewSizeSquare(self, height, width, num):
        Nhe = height
        Nwi = width
        countW = 1
        countH = 1
        if num == 2 or num == 3 or num == 5 or num == 7:
            Nhe = height
            Nwi = width/num
            countW = num
            countH = 1
        if num == 4 or num == 6 or num == 8 or num == 10:
            Nhe = height/2
            Nwi = width/(num/2)
            countW = (num/2)
            countH = 2
        if num == 9 or num == 12 or num == 15:
            Nhe = height/3
            Nwi = width/3
            countW = (num/3)
            countH = 3
        return (Nhe, Nwi, countW, countH)

    #square slicing 
    def Square(self, name, num):
        pic = Image.open(name)
        width, height = pic.size
        Nhe, Nwi, Wcounts, Hcounts = NewSizeSquare(height, width, num)
        left = 0
        upper = 0
        right = Nwi
        lower = Nhe
        count = 1
        list_images = []
        for Hcount in xrange (Hcounts):
            left = 0
            right = Nwi
        for Wcount in xrange (Wcounts):
            box = (left, upper, right, lower)
            list_images.append(pic.crop(box))
            left += Nwi
            right += Nwi
            count += 1
            upper += Nhe
            lower += Nhe
        return list_images

    #new snake width and height
    #def NewSizeSnake(self, height, width, num):
    #        Nhe = height
    #        Nwi = width
    #        countW = 1
    #        countH = 1
    #        Nhe = height
    #        Nwi = width/num
    #        countW = num
    #        countH = 1
    #return (Nhe, Nwi, countW, countH)

    #long slicing       
    #def Snake(self, pic, num):
    #        width, height = pic.size
    #        Nhe, Nwi, Wcounts, Hcounts = self.NewSizeSnake(height, width, num)
    #        left = 0
    #        upper = 0
    #        right = Nwi
    #        lower = Nhe
    #        count = 1
    #        list_images = []
    #for Hcount in xrange(Hcounts):
    #            left = 0
    #            right = Nwi
    #for Wcount in xrange (Wcounts):
    #                box = (left, upper, right, lower)
    #                list_images.append(pic.crop(box))
    #                left += Nwi
    #                right += Nwi
    #                count += 1
    #            upper += Nhe
    #            lower += Nhe
    #return list_images

    #new back to back width and height
    def NewSizeBtB(self, height, width):
        Nhe = height
        Nwi = width/2
        countW = 2
        return Nhe, Nwi, countW

    #Back to back slicing
    def BtB(self, name, num):
        pic = Image.open(name)
        width, height = pic.size
        Nhe, Nwi, Wcounts = NewSizeBtB(height, width)
        left = 0
        upper = 0
        right = Nwi
        lower = Nhe
        list_images = []
        for Wcount in xrange (Wcounts):
            box = (left, upper, right, lower)
            list_images.append(pic.crop(box))
            left += Nwi
            right += Nwi
        return list_images

    # The general slicing function     
    def Slice(self, pic, num, form):
        return form(pic, num)
 

