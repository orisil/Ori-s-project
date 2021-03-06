import threading,socket, sys
from SliceImage import * 
from SessionWithClient import * 

CLIENTS_LIMIT = 50
GUI_PORT = 12321
class PythonServer(threading.Thread):
	listenerSock = None
	startFlag = False
	open_clients = {} 
	checked_clients = {}    
	crypto_object = None  
	
	def run(self):
        	self.gui.guiSock.send("Server running...Waiting for a connection...#")   # to GUI 
		try:
			# Listener socket
			listenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			listenerSock.bind(("",self.listenerPort))
			listenerSock.listen(5)
			self.gui.guiSock.send("Listening to clients...#")   # to GUI 

			while True:
				clientSock, addr = listenerSock.accept()                   
				# Thread creating loop
				while True:
					if threading.activeCount() < CLIENTS_LIMIT:
						self.gui.guiSock.send("Connected client  ip=" + addr[0] + "#")   # to GUI 
						clientIP = addr[0]  # key - IP client
						# Connection by IP  clientIP
						sessionWithClient = SessionWithClient(self, clientSock, addr )
						sessionWithClient.start()
						self.open_clients[clientIP] = sessionWithClient 
						sessionWithClient.clientSock.send("Client_Hello")    
						data = sessionWithClient.clientSock.recv(1024)
						if data == "Server_Hello":
							sessionWithClient.aes_key = self.crypto_object.exchange_keys(sessionWithClient.clientSock)
							break
		except socket.error , er_msg:
			error_code = er_msg[0]
			if error_code == 10048:
				self.gui.guiSock.send("Port " + str(self.listenerPort) + " is busy#")   # to GUI  
			else:
				self.gui.guiSock.send(str(er_msg) + "#")   # to GUI            
		except Exception as er_msg:
			self.gui.guiSock.send(str(er_msg) + "#")   # to GUI  
			
		

	def __init__(self, gui, listenerPort, slicemode):
	
		threading.Thread.__init__(self)
		self.gui = gui
		self.listenerPort = listenerPort
		self.slicemode = slicemode
		self.crypto_object = MyCrypto()
		
class GuiHandler(threading.Thread):   
    pythonServer = None
    slice_image = None

    def __init__(self):
		# socket between the this server and the GUI
		self.guiSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.guiSock.connect(("127.0.0.1", GUI_PORT))
		self.slice_image = None
		threading.Thread.__init__(self)
		self.state_machine = {"StartSliceImage" :  self.StartSliceImage,"Stop" :  self.Stop,"StopAll" :  self.StopAll,"stopBroadcast" :  self.stopBroadcast,"UpdateCheckedClients" : self.UpdateCheckedClients}

    def close_all_clients(self):
		for client in self.pythonServer.open_clients.values():
			client.send("Stop")
			client.clientSock.close()
		self.pythonServer.open_clients.clear()  
		self.pythonServer.checked_clients.clear()      

    def  StartSliceImage(self, operands):
        self.pythonServer.startFlag = True
        self.slice_image = SliceImage(self.pythonServer, operands)
        self.slice_image.start()

    def  Stop(self, operands):
        ip = operands
        if self.slice_image != None:
			self.slice_image.stopIP = ip               
        else:
            self.pythonServer.open_clients[ip].send("Stop")
            self.pythonServer.open_clients[ip].clientSock.close()
            del self.pythonServer.open_clients[ip]
            del self.pythonServer.checked_clients[ip]

    def  StopAll(self, operands):
        if self.slice_image != None:
			self.slice_image.stopIP = '255.255.255.255'
        else:
            self.close_all_clients()

# the function who stopes the broadcast
    def  stopBroadcast(self, operands):
        if self.slice_image != None:
            self.slice_image.stopBroadcast = True

# the function who updates the checked clients
    def  UpdateCheckedClients(self, operands):
        fields = operands.split("$")   # [0] - ip  [1] - "True" or "False"
        if fields[1] == "True":
            self.pythonServer.checked_clients[fields[0]] = self.open_clients[fields[0]]
        else:
            del self.pythonServer.checked_clients[fields[0]]


# the main function
    def  run(self):   
        while True:
                # Wait message from GUI 
                data = self.guiSock.recv(1024)
                if len(data) > 0 :
                        items = data.split("#")   # Operation
                        self.state_machine[items[0]](items[1])   # items[1]  -  Operands                        

def main(args):
	try:  
		guiHandler = GuiHandler()            #  connection to GUI process
		guiHandler.start()            		#  start thread loop for session with GUI         
		guiHandler.pythonServer = PythonServer(guiHandler, int(args[0]), args[1])  
		guiHandler.pythonServer.start() 
	except socket.error , e:
		print e   

if __name__ == "__main__":
     main(sys.argv[1:])
