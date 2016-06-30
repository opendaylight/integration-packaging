#!/usr/bin/env python
"""This module creates a Mininet Topology based on the examples in the Mininet Documentation"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
import time


class SingleSwitchTopo(Topo):
    """Single switch connected to n hosts."""
    def build(self, n=2):
        switch = self.addSwitch("s1")
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost("h%s" % (h + 1))
            self.addLink(host, switch)


def simple_test():
    """Create and test a simple network"""
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo, controller=None)
    net.addController("c0", controller=RemoteController, ip="127.0.0.1", port=6633)
    net.start()
    time.sleep(10)
    print "Testing network connectivity"
    net.pingAll()

if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simple_test()
