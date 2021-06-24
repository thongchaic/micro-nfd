import network
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("PNHome2","st11ae58*")
wlan.ifconfig()
