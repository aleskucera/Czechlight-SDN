from typing import Dict, List

import networkx as nx
import matplotlib.pyplot as plt

from .device import Device, DirectionalPort


class Network:
    """Class representing a network of devices.

    This class manages the devices in the network and provides methods for adding devices,
    creating bidirectional links, finding paths, and visualizing the network.

    Attributes:
        devices (dict): A dictionary containing devices in the network, indexed by their names.
    """

    def __init__(self):
        self.devices = {}

    def add_device(self, device: Device) -> None:
        """Add a device to the network.

        Args:
            device (Device): The device to add to the network.

        Returns:
            None
        """

        self.devices[device.name] = device

    def add_bidi_link(self, device_a: str, port_a: str, device_b: str, port_b: str) -> None:
        """Add a bidirectional link between two devices.

        Args:
            device_a (str): The name of the first device to link.
            port_a (str): The port on the first device to link.
            device_b (str): The name of the second device to link.
            port_b (str): The port on the second device to link.

        Returns:
            None
        """

        self.devices[device_a].add_link(port_a, self.devices[device_b], port_b)
        self.devices[device_b].add_link(port_b, self.devices[device_a], port_a)

    @property
    def device_graph(self) -> nx.Graph:
        """Create a graph of devices and their neighbors.

        Returns:
            nx.Graph: A graph of devices and their neighbors.
        """

        graph = nx.Graph()
        for device in self.devices.values():
            for neighbor in device.neighbors:
                graph.add_edge(device.name, neighbor.name)
        return graph

    @property
    def graph(self) -> nx.Graph:
        """Create a graph of devices and their links.

        Returns:
            nx.Graph: A graph of devices and their links.
        """

        graph = nx.Graph()
        for device in self.devices.values():
            graph.add_edges_from(device.graph_edges)
        return graph

    def shortest_path(self, tp_a: str, tp_b: str) -> Dict[str, List[DirectionalPort]]:
        """Find the shortest path between two termination points.

        Args:
            tp_a (str): The name of the first termination point.
            tp_b (str): The name of the second termination point.

        Returns:
            Dict[str, List[DirectionalPort]]: A dictionary containing the shortest paths in both directions.
        """

        ret = {}

        node_a_rx = DirectionalPort(self.devices[tp_a], 'C', "RX")
        node_a_tx = DirectionalPort(self.devices[tp_a], 'C', "TX")
        node_b_rx = DirectionalPort(self.devices[tp_b], 'C', "RX")
        node_b_tx = DirectionalPort(self.devices[tp_b], 'C', "TX")

        ret["direction_ab"] = nx.shortest_path(self.graph, node_a_tx, node_b_rx)
        ret["direction_ba"] = nx.shortest_path(self.graph, node_b_tx, node_a_rx)
        return ret

    def draw(self) -> None:
        """Draw the device graph.

        Returns:
            None
        """

        nx.draw(self.device_graph, with_labels=True)
        plt.show()
