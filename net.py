from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.topo import Topo


class MyTopo( Topo ):

    def build(self):
            h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1")
            h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2")
            h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3")
            h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4")
            h5 = self.addHost('h5', mac="00:00:00:00:00:05", ip="10.0.0.5")
            h6 = self.addHost('h6', mac="00:00:00:00:00:06", ip="10.0.0.6")
            h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="10.0.0.7")
            h8 = self.addHost('h8', mac="00:00:00:00:00:08", ip="10.0.0.8")

        
            s1 = self.addSwitch('s1', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s2 = self.addSwitch('s2', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s3 = self.addSwitch('s3', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s4 = self.addSwitch('s4', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s5 = self.addSwitch('s5', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s6 = self.addSwitch('s6', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s7 = self.addSwitch('s7', switch=OVSKernelSwitch, protocols='OpenFlow13')
            s8 = self.addSwitch('s8', switch=OVSKernelSwitch, protocols='OpenFlow13')

            



            self.addLink(h1, s1, bw=1000, delay='1ms')
            self.addLink(h2, s2, bw=1000, delay='1ms')
            self.addLink(h3, s3, bw=1000, delay='1ms')
            self.addLink(h4, s4, bw=1000, delay='1ms')
            self.addLink(h5, s5, bw=1000, delay='1ms')
            self.addLink(h6, s6, bw=1000, delay='1ms')
            self.addLink(h7, s7, bw=1000, delay='1ms')
            self.addLink(h8, s8, bw=1000, delay='1ms')
            self.addLink(s1, s3, bw=1000, delay='1ms')
            self.addLink(s1, s8, bw=1000, delay='1ms')
            self.addLink(s2, s4, bw=1000, delay='1ms')
            self.addLink(s2, s5, bw=1000, delay='1ms')
            self.addLink(s2, s7, bw=1000, delay='1ms')
            self.addLink(s3, s8, bw=1000, delay='1ms')
            self.addLink(s3, s6, bw=1000, delay='1ms')
            self.addLink(s3, s4, bw=1000, delay='1ms')
            self.addLink(s4, s5, bw=1000, delay='1ms')
            self.addLink(s4, s7, bw=1000, delay='1ms')
            self.addLink(s5, s7, bw=1000, delay='1ms')
            self.addLink(s5, s6, bw=1000, delay='1ms')
            self.addLink(s6, s8, bw=1000, delay='1ms')
            self.addLink(s7, s8, bw=1000, delay='1ms')
def topology():

    topo = MyTopo()
    net = Mininet(topo = topo,controller= lambda name: RemoteController( name, ip='127.0.0.1' ), switch=OVSKernelSwitch, link=TCLink)

 
    net.start()

    print ("*** Running CLI")
    CLI(net)

    print ("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

topos = {
    'mytopo': MyTopo
}