from itertools import product
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class NeighborInfo:
    """Information about a connected neighbor.

    This class is used to store information about a neighbor of a device
    in the links dictionary of the Device class.

    Attributes:
        device (Device): The neighboring device.
        device_port (str): The port on the neighboring device.
    """
    device: 'Device'
    device_port: str


@dataclass
class DirectionalPort:
    """A directional port on a device used in the network graph representation.

    Attributes:
        device (Device): The device to which this port belongs.
        port (str): The name of the port.
        direction (str): The direction of the port (TX or RX).

    Raises:
        AssertionError: If an invalid direction is provided.
    """
    device: 'Device'
    port: str
    direction: str

    def __post_init__(self):
        assert self.direction in ["TX", "RX"], f"Invalid direction: {self.direction}"

    def __repr__(self):
        return f"{self.device.name}:{self.port}:{self.direction}"

    def __hash__(self):
        return hash((self.device, self.port, self.direction))


class Device:
    """Base class for network devices."""

    def __init__(self, name: str):
        self.name = name
        self.links = {}

    def add_link(self, port: str, device: 'Device', device_port: str) -> None:
        """Add a link to another device at the specified port.

        Args:
            port (str): The port to add the link to.
            device (Device): The device to link to.
            device_port (str): The port on the other device to link to.

        Returns:
            None
        """

        assert port in self.links
        self.links[port] = NeighborInfo(device, device_port)

    @property
    def neighbors(self) -> List['Device']:
        """Get a list of neighboring devices.

        Returns:
            List['Device']: A list of neighboring devices.
        """
        return [dev_info.device for dev_info in self.links.values() if dev_info is not None]

    @property
    def internal_edges(self) -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate a list of internal edges for the device.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of internal edges.
        """
        # Generate internal links based on the device's links
        return []

    @property
    def external_edges(self) -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate a list of external edges for the device.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of external edges.
        """
        links = []
        for port, info in self.links.items():
            links.extend(self._generate_edges(port, info))
        return links

    @property
    def graph_edges(self) -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate a list of graph edges for the device.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of graph edges.
        """
        internal_edges = self.internal_edges
        external_edges = self.external_edges

        # logger.info(f"From device {self.name}, added {len(internal_edges)} internal edges and "
        #             f"{len(external_edges)} external edges to the graph.")

        return internal_edges + external_edges

    def _generate_edges(self, port: str, device_info: NeighborInfo) \
            -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate edges based on the provided device information.

        Args:
            port (str): The port to generate edges from.
            device_info (NeighborInfo): Information about the connected neighbor.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of generated edges.
        """
        if device_info is None:
            return []

        # Extract information from the device_info tuple
        neighbor_device = device_info.device
        neighbor_device_port = device_info.device_port

        # Create directional ports for the current device
        self_tx_port = DirectionalPort(self, port, "TX")
        self_rx_port = DirectionalPort(self, port, "RX")

        # Create directional ports for the neighbor device
        neighbor_tx_port = DirectionalPort(neighbor_device, neighbor_device_port, "TX")
        neighbor_rx_port = DirectionalPort(neighbor_device, neighbor_device_port, "RX")

        # Create edges for both transmission directions
        self_to_neighbor_edge = (self_tx_port, neighbor_rx_port)
        neighbor_to_self_edge = (neighbor_tx_port, self_rx_port)

        # Return a list containing both edges
        return [self_to_neighbor_edge, neighbor_to_self_edge]

    def __repr__(self) -> str:
        representation = f"DEVICE\n"
        representation += f"  - name: {self.name}\n"
        representation += f"  - links:\n"

        for link_type, info in self.links.items():
            if info is not None:
                representation += f"\t  {link_type}: {info.device.name}\n"

        return representation

    def __str__(self) -> str:
        return self.__repr__()


class CzechLightLineDegree(Device):
    """Class representing Czech Light Line Degree devices.

    This class represents devices with express ports that are part of the Czech Light Line Degree network.

    Attributes:
        name (str): The name of the device.
        num_express_ports (int, optional): The number of express ports on the device. Default is 8.
    """

    def __init__(self, name: str, num_express_ports: int = 8):
        super().__init__(name)
        self.num_express_ports = num_express_ports

        self.links = {"LINE": None}
        self.links.update({f"E{i}": None for i in range(1, self.num_express_ports + 1)})

        # logger.info(f"Created CzechLightLineDegree device {self.name} with {self.num_express_ports} express ports.")

    @property
    def internal_edges(self) -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate internal edges for Czech Light Line Degree devices.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of internal edges.
        """
        valid_express_ports = [f"E{i}" for i in range(1, self.num_express_ports + 1) if self.links[f"E{i}"] is not None]

        edges = []
        if self.links['LINE'] is not None:
            for e_port in valid_express_ports:
                edges.extend(self._generate_edges("LINE", NeighborInfo(self, e_port)))

        return edges


class CzechLightAddDrop(Device):
    """Class representing Czech Light Add Drop devices.

    This class represents devices with both express and client ports that are part of the Czech Light Add Drop network.

    Attributes:
        name (str): The name of the device.
        num_express_ports (int, optional): The number of express ports on the device. Default is 8.
        num_client_ports (int, optional): The number of client ports on the device. Default is 8.
    """

    def __init__(self, name: str, num_express_ports: int = 8, num_client_ports: int = 8):
        super().__init__(name)
        self.num_client_ports = num_client_ports
        self.num_express_ports = num_express_ports

        self.links = {f"E{i}": None for i in range(1, self.num_express_ports + 1)}
        self.links.update({f"C{i}": None for i in range(1, self.num_client_ports + 1)})

        # logger.info(f"Created CzechLightAddDrop device {self.name} with {self.num_express_ports} "
        #             f"express ports and {self.num_client_ports} client ports.")

    @property
    def internal_edges(self) -> List[Tuple[DirectionalPort, DirectionalPort]]:
        """Generate internal edges for Czech Light Add Drop devices.

        Returns:
            List[Tuple[DirectionalPort, DirectionalPort]]: A list of internal edges.
        """
        valid_express_ports = [port for port, device_info in self.links.items() if
                               device_info is not None and port.startswith('E')]
        valid_client_ports = [port for port, device_info in self.links.items() if
                              device_info is not None and port.startswith('C')]

        edges = []
        for e_port, c_port in product(valid_express_ports, valid_client_ports):
            edges.extend(self._generate_edges(e_port, NeighborInfo(self, c_port)))

        return edges


class TerminationPoint(Device):
    """Class representing Termination Point devices.

    This class represents termination point devices which have a single client port.

    Attributes:
        name (str): The name of the termination point device.
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.links = {"C": None}

        # logger.info(f"Created TerminationPoint {self.name}.")
