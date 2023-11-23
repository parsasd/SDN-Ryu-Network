import array
from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether, inet

from ryu.topology.api import get_all_link, get_all_switch
from ryu.topology import event
import networkx as network
import random
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_get = self
        self.network = network.DiGraph()
        self.switches = []
        self.link_weights = {}
        self.sw_num = 0
        self.src = 1
        self.dst = 5

    events = [event.EventSwitchEnter,
              event.EventSwitchLeave, event.EventPortAdd,
              event.EventPortDelete, event.EventPortModify,
              event.EventLinkAdd, event.EventLinkDelete]
    @set_ev_cls([event.EventLinkAdd, event.EventLinkDelete])
    def update_topology_data(self, ev):
        print("Updating topology data:")
        switch_list = get_all_switch(self.topology_get)
        switches = [switch.dp.id for switch in switch_list]
        self.network.add_nodes_from(switches)
        links_list = get_all_link(self.topology_get)
        links = []
        for link in links_list:
            src = link.src.dpid
            dst = link.dst.dpid
            if (src, dst) not in self.link_weights:
                if (dst, src) not in self.link_weights:
                    self.link_weights[(src, dst)] = random.randint(1, 10)
                else:
                    self.link_weights[(src, dst)] = self.link_weights[(dst, src)]
                
            weight = self.link_weights[(src, dst)]
            links.append((src, dst, {'port': link.src.port_no, 'weight': weight}))
        self.network.add_edges_from(links)

        if len(links_list) == len(links):
            print("Network:", self.network)

            for (src, dst, attr) in self.network.edges(data=True):
                print(f"Link from {src} to {dst} has weight {attr['weight']}")

            

        try:
            path = network.shortest_path(self.network, self.src, self.dst, weight='weight')
            print(f"found path {path}")

            for i in range(len(path) - 1):
                src_switch = path[i]
                next_switch = path[i + 1]

                out_port = self.network[src_switch][next_switch]['port']

                datapath = None
                for switch in get_all_switch(self.topology_get):
                    if switch.dp.id == src_switch:
                        datapath = switch.dp
                        break

                if datapath:
                    ofproto = datapath.ofproto
                    parser = datapath.ofproto_parser
                    match = parser.OFPMatch(
                        eth_type=ether.ETH_TYPE_IP, 
                        ip_proto=inet.IPPROTO_ICMP, 
                        ipv4_src=f"10.0.0.{self.src}", 
                        ipv4_dst=f"10.0.0.{self.dst}"
                    )
                    actions = [parser.OFPActionOutput(out_port)]

                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                        actions)]
                    
                    mod = parser.OFPFlowMod(datapath=datapath, priority=1,
                                            match=match, instructions=inst)
                    datapath.send_msg(mod)

            num = 0
            for link in get_all_link(self.topology_get):
                if (link.src.dpid == self.dst or link.dst.dpid == self.dst):
                    num = num + 1

            datapath = None
            for switch in get_all_switch(self.topology_get):
                if switch.dp.id == path[-1]:
                    datapath = switch.dp
                    break

            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser
            match = parser.OFPMatch(
                eth_type=ether.ETH_TYPE_IP, 
                ip_proto=inet.IPPROTO_ICMP, 
                ipv4_dst=f"10.0.0.{self.dst}"
            )
            actions = [parser.OFPActionOutput(int(num / 2) + 1)]

            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                actions)]
            
            mod = parser.OFPFlowMod(datapath=datapath, priority=1,
                                    match=match, instructions=inst)
            datapath.send_msg(mod)
        
        except network.NetworkXNoPath:
            print(f"No path from {self.src} to {self.dst}")


        temp = self.src
        self.src = self.dst
        self.dst= temp
        try:
            path = network.shortest_path(self.network, self.src, self.dst, weight='weight')
            print(f"found path {path}")

            for i in range(len(path) - 1):
                src_switch = path[i]
                next_switch = path[i + 1]

                out_port = self.network[src_switch][next_switch]['port']

                datapath = None
                for switch in get_all_switch(self.topology_get):
                    if switch.dp.id == src_switch:
                        datapath = switch.dp
                        break

                if datapath:
                    ofproto = datapath.ofproto
                    parser = datapath.ofproto_parser
                    match = parser.OFPMatch(
                        eth_type=ether.ETH_TYPE_IP, 
                        ip_proto=inet.IPPROTO_ICMP, 
                        ipv4_src=f"10.0.0.{self.src}", 
                        ipv4_dst=f"10.0.0.{self.dst}"
                    )
                    actions = [parser.OFPActionOutput(out_port)]

                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                        actions)]
                    
                    mod = parser.OFPFlowMod(datapath=datapath, priority=1,
                                            match=match, instructions=inst)
                    datapath.send_msg(mod)

            num = 0
            for link in get_all_link(self.topology_get):
                if (link.src.dpid == self.dst or link.dst.dpid == self.dst):
                    num = num + 1

            datapath = None
            for switch in get_all_switch(self.topology_get):
                if switch.dp.id == path[-1]:
                    datapath = switch.dp
                    break
            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser
            match = parser.OFPMatch(
                eth_type=ether.ETH_TYPE_IP, 
                ip_proto=inet.IPPROTO_ICMP, 
                ipv4_dst=f"10.0.0.{self.dst}"
            )
            actions = [parser.OFPActionOutput(int(num / 2) + 1)]

            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                actions)]
            
            mod = parser.OFPFlowMod(datapath=datapath, priority=1,
                                    match=match, instructions=inst)
            datapath.send_msg(mod)

        except network.NetworkXNoPath:
            print(f"No path from {self.src} to {self.dst}")


    def get_path(self, datapath, src, dst):
        if src not in self.network.nodes() or dst not in self.network.nodes():
            return
        dpid = datapath.id
        path = network.shortest_path(self.network, src, dst)


        if dpid in path:
            next_stat = path[path.index(dpid) + 1]
            out_port = self.network[dpid][next_stat]['port']
            return out_port
        else:
            return None