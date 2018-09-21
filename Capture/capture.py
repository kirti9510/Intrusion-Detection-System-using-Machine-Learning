from scapy.all import IP, sniff
import pyshark

def packet_data():
	capture = pyshark.LiveCapture(interface='wlan0')
	for packet in capture.sniff_continuously(packet_count=5):
		print 'Just Arrived:', packet

if __name__ == '__main__':
	packet_data()