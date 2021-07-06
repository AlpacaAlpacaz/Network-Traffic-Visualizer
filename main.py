import dpkt
import socket
import pygeoip
import sys
from requests import get
 
gi = pygeoip.GeoIP('GeoLiteCity.dat')

#Grabs 
def retKML(ip):
    #Ignored Multicast and local IPV6
    if(ip[0:4]=='fe80' or ip[0:3]=='ff0'):
        return''
    
    dst = gi.record_by_addr(ip)
    src = gi.record_by_addr(gIP)

    #Tosses all local ipv4s that can't be resolved to a location
    if(dst != None):
        try:
            dstLongitude = dst['longitude']
            dstLatitude = dst['latitude']
            srcLongitude = src['longitude']
            srcLatitude = src['latitude']

            #Styles the lines placed on Google Maps
            kml = (
                '<Placemark>\n'
                    f'<name>{ip}</name>\n'
                    '<extrude>1</extrude>\n'
                    '<tessellate>1</tessellate>\n'
                    '<styleUrl>#transBluePoly</styleUrl>\n'
                    '<LineString>\n'
                        f'<coordinates>{dstLongitude},{dstLatitude}\n{srcLongitude},{srcLatitude}</coordinates>\n'
                    '</LineString>\n'
                '</Placemark>\n'
            )
            return kml
        except:
            print("error in retKML()")
            return ''
    else:
        return ''

#Pulls the IPs from the pcap
def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            #Unpacks the Ethernet frame in the pcap
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            #Converts the packed IP to decimal IP. ntop for ipv6 and ntoa for ipv4
            if(sys.getsizeof(ip.dst)>37):
                dst = socket.inet_ntop(socket.AF_INET6, ip.dst)
            else:
                dst = socket.inet_ntoa(ip.dst)

            dstKML = retKML(dst)

            kmlPts = kmlPts + dstKML
        except:
            print("error in plotIPs()")
    return kmlPts
 
 
def main():
    global gIP 
    gIP = input("Enter the source IP here or press ENTER to fetch it automatically using ipify.org: ")

    #Quereies ipify.org for the public IP to use as the source
    if(gIP==''):
        gIP = get('https://api.ipify.org').text
    
    print(f'Using {gIP} for the source IP')

    f = open('wireshark.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    
    with open('googleMaps.kml', 'w') as f:
        f.write(kmldoc)
        print("File Created")
 
if __name__ == '__main__':
    main()