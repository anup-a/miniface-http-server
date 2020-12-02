#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import SingleSwitchTopo
from mininet.util import custom, pmonitor 
# def myNetwork():

#     net = Mininet( topo=None,
#                    build=False,
#                    ipBase='10.0.0.0/8')

#     info( '*** Adding controller\n' )
#     c0=net.addController(name='c0',
#                       controller=Controller,
#                       protocol='tcp',
#                       port=6633)

#     info( '*** Add switches\n')
#     s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

#     info( '*** Add hosts\n')
#     # h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
#     # h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

#     info( '*** Add links\n')
#     net.addLink(h1, s1)
#     net.addLink(s1, h2)

#     info( '*** Starting network\n')
#     net.build()
#     info( '*** Starting controllers\n')
#     for controller in net.controllers:
#         controller.start()

#     info( '*** Starting switches\n')
#     net.get('s1').start([])

#     info( '*** Post configure switches and hosts\n')
#     h1.cmd("python3 server/server.py &")
#     import time
#     time.sleep(3)
#     print(h2.cmd("python3  server/client_mininet.py client anup_22 hianup 5"))
#     time.sleep(3)
#     CLI(net)
#     net.stop()

def run_server():
    net = Mininet(SingleSwitchTopo(k=6))
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    # h1.cmd('python3 server.py '+str(h1.IP())+' &')
    
    import time
    # for host in net.hosts:
    popens = {}
    popens[ h1 ]=  h1.popen("python3 server/server.py")
    time.sleep(5)
    popens[ h2 ] = h2.popen( "python3 server/client_mininet.py client anup_22 hianup 5")
    # last = host
    # print(h2.popen("python3 server/client_mininet.py client anup_22 hianup 5"))
    time.sleep(5)
    for host, line in pmonitor( popens ):
        if host:
            info( "<%s>: %s" % ( host.name, line ) )
    # CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    # myNetwork()
    run_server()

