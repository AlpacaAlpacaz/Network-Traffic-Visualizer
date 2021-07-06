import dpkt
import socket
import pygeoip
import sys
from requests import get
 
gi = pygeoip.GeoIP('GeoLiteCity.dat')

def retKML(ip):
    if(ip[0:4]=='fe80' or ip[0:3]=='ff0'):
        return''
    
    if(len(ip)>15):
        dst = gi.record_by_addr(ip)
    else:
        dst = gi.record_by_name(ip)


    src = gi.record_by_name(gIP)

    if(dst != None):
        try:
            dstLongitude = dst['longitude']
            dstLatitude = dst['latitude']
            srcLongitude = src['longitude']
            srcLatitude = src['latitude']

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
        print('local IP')
        return ''


def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            """
            if(sys.getsizeof(ip.src)>37):
                src = socket.inet_ntop(socket.AF_INET6, ip.src)
            else:
                src = socket.inet_ntoa(ip.src)

            srcKML = retKML(src)
            """
            if(sys.getsizeof(ip.dst)>37):
                dst = socket.inet_ntop(socket.AF_INET6, ip.dst)
                print('ipv6')
            else:
                dst = socket.inet_ntoa(ip.dst)

            dstKML = retKML(dst)

            #kmlPts = kmlPts + srcKML + dstKML
            kmlPts = kmlPts + dstKML
        except:
            print("error in plotIPs()")
    return kmlPts
 
 
def main():
    global gIP 
    gIP = input("Enter the source IP here or press ENTER to fetch it automatically using ipify.org: ")

    if(gIP==''):
        gIP = get('https://api.ipify.org').text

    f = open('wireshark.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    #kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    
    with open('googleMaps.kml', 'w') as f:
        f.write(kmldoc)
        print("File Created")
 
if __name__ == '__main__':
    main()