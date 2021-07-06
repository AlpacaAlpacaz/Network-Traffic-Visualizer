import dpkt
import socket
import pygeoip
import sys
 
gi = pygeoip.GeoIP('GeoLiteCity.dat')

def retKML(ip):
    rec = gi.record_by_name(ip)
    if (rec != None):
        try:
            longitude = rec['longitude']
            latitude = rec['latitude']
            kml = (
                '<Placemark>\n'
                    '<name>%s</name>\n'
                    '<Point>\n'
                        '<coordinates>%6f,%6f</coordinates>\n'
                    '</Point>\n'
                '</Placemark>\n'
                )%(ip,longitude, latitude)
            return kml
        except:
            print("error in retKML()")
            return ''
    else:
        print("local IP")
        return ''


def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            size = sys.getsizeof(ip.src)
            src = socket.inet_ntoa(ip.src)
            srcKML = retKML(src)

            dst = socket.inet_ntoa(ip.dst)
            dstKML = retKML(dst)

            kmlPts = kmlPts + srcKML + dstKML
        except:
            print("error in plotIPs()")
    return kmlPts
 
 
def main():
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