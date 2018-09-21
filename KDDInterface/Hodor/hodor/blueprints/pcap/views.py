import atexit
import threading
from flask import Blueprint
from flask.json import jsonify
from hodor.blueprints.pcap.tasks import pcap_learn_listener
from hodor.blueprints.pcap.tasks import pcap_predict_listener
from socket import socket, AF_INET, SOCK_DGRAM
import sys

pcap = Blueprint('pcap', __name__)

cond = threading.Event()

pcap_learn_thread = threading.Thread(target=pcap_learn_listener, args=(cond, ))
pcap_learn_thread.daemon = True

pcap_predict_thread = threading.Thread(target=pcap_predict_listener, args=(cond, ))
pcap_predict_thread.daemon = True

now_learning = False

train_data = "/home/nitesh/workspace/Project/pict-ml/pict-ml/KDDInterface/kddcup.data_cv"
test_data = "/home/nitesh/workspace/Project/pict-ml/pict-ml/KDDInterface/kddcup.data_test"


@pcap.route('/api/pcap_learn/<val>', methods=['GET'])
def pcap_learn_start(val):
		bval = str(val)
		result = "Invalid input"
		if bval == 'True' and pcap_learn_thread.isAlive() == False:
			result = "PCAP learn listener started ..."
			pcap_learn_thread.start()
		elif bval == 'False' and pcap_learn_thread.isAlive() == True:
			result = "PCAP learn listener stopped ..."
			now_learning = True
			cond.set()
		else:
			print "bval", bval, pcap_learn_thread.isAlive()
		send_file(train_data)
		return jsonify(result = result)

@pcap.route('/api/pcap_predict/<val>', methods=['GET'])
def pcap_predict_start(val):
		bval = str(val)
		result = "Invalid input"
		if bval == 'True' and pcap_predict_thread.isAlive() == False:
			result = "PCAP learn listener started ..."
			pcap_predict_thread.start()
		else:
			result = "Still learning ..."
		send_file(test_data)
		return jsonify(result = result)


@pcap.route('/api/pcap_is_running', methods=['GET'])
def pcap_is_learn_running():
		learn = False
		predict = True
		if pcap_learn_thread.isAlive():
			learn = True
		if pcap_predict_thread.isAlive():
			predict = True
		return jsonify(learn = learn, predict = predict)

def send_file(file_name):
		s = socket(AF_INET,SOCK_DGRAM)
		host = 'localhost'
		port = 5000

		addr = (host,port)

		f=open(file_name,"r")
		lines = f.readlines()

		for data in lines:
			if(s.sendto(data,addr)):
				# print "sending ..."
				pass
		s.close()
		f.close()

@pcap.route('/api/get_data', methods=['GET'])
def get_data():
		file = open("op_file.txt","r")
		return jsonify(result = file.readlines())		

		

@atexit.register
def cleanup():
	print "Removing listener"
	cond.set()