# Network-Traffic-Visualizer
Uses a wireshark .pcap to display a visualization of network traffic using google maps.

## Installing
dpkt and pygeoip modules will need to be installed
`pip install dpkt pygeoip`

You will also need GeoLiteCity.dat to convert IP addreses to longitude and latitude. This can be downloaded [here](https://github.com/mbcc2006/GeoLiteCity-data) and placed beside the main.py

## Usage
Using wireshark, start recording the network data you want visualized than once you stop it Export Specified Packets and save it as a Wireshark/tcpdump/...-pcap to the same folder as main.py and name it wireshark.pcap

execute main.py and it will generate a file called googleMaps.kml. Next go [here](https://www.google.com/mymaps) and create a new map than add the kml file as a new layer.