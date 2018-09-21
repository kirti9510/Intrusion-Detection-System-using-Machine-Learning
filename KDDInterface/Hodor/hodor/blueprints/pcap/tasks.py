from time import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.ensemble import IsolationForest
import blaze as bz
import socket, select, Queue
import pandas
import csv

clfisolation = IsolationForest(n_estimators=100, contamination=0.1)


def loadDataFile(filename):
		col_names = ["duration","protocol_type","service","flag","src_bytes",
				"dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
				"logged_in","num_compromised","root_shell","su_attempted","num_root",
				"num_file_creations","num_shells","num_access_files","num_outbound_cmds",
				"is_host_login","is_guest_login","count","srv_count","serror_rate",
				"srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
				"diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
				"dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
				"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
				"dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
		data = pandas.read_csv(filename, header=None, names = col_names)
		num_features = [
				"duration","src_bytes",
				"dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
				"logged_in","num_compromised","root_shell","su_attempted","num_root",
				"num_file_creations","num_shells","num_access_files","num_outbound_cmds",
				"is_host_login","is_guest_login","count","srv_count","serror_rate",
				"srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
				"diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
				"dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
				"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
				"dst_host_rerror_rate","dst_host_srv_rerror_rate"
		]
		features = data[num_features].astype(float)
		features_train, features_test, labels_train, labels_test = train_test_split(features[num_features], data['label'], test_size=0.0, random_state=42)
		features_train.apply(lambda x: MinMaxScaler().fit_transform(x))
		features_test.apply(lambda x: MinMaxScaler().fit_transform(x))
		labels = data['label'].copy()
		lables_train = labels[:len(features_train)]
		labels_test = labels[len(features_train):]
		return features_train, features_test, labels_train, labels_test


def pcap_learn_listener(cond):
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print "Creating learning listener"
		udp.bind(('0.0.0.0', 5000))
		f = open ('learnset.csv', 'w')
		pkt = 0
		while not cond.is_set():
			# 500 millisecond timeout? 
			r, w, x = select.select([udp], [], [], 0.5)
			for i in r:
				pkt += 1
				data, sender = i.recvfrom(65507)
				f.write(data)
				print pkt
		f.close()
		X, Xtest, Y, Ytest = loadDataFile("learnset.csv")
		clfisolation.fit(X)
		print "Done learning..."

def pcap_predict_listener(cond):
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print "Creating predict listener"
		udp.bind(('0.0.0.0', 5000))
		num_features = [
				"duration","src_bytes",
				"dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
				"logged_in","num_compromised","root_shell","su_attempted","num_root",
				"num_file_creations","num_shells","num_access_files","num_outbound_cmds",
				"is_host_login","is_guest_login","count","srv_count","serror_rate",
				"srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
				"diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
				"dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
				"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
				"dst_host_rerror_rate","dst_host_srv_rerror_rate"
		]
		while True:
			# 500 millisecond timeout? 
			r, w, x = select.select([udp], [], [], 0.5)
			output_file = open("op_file.txt","a")
			for i in r:
				Y, sender = i.recvfrom(65507)
				data = np.array(Y.split(','))
				y = np.delete(data,[1,2,3])
				string = ", ".join(str(c) for c in y)
				if clfisolation.predict(y) == 1:
					output_file.write(string + "Intrusion" + '\n')
					print "Intrusion"
			output_file.close()
		