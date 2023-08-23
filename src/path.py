import os
import json
from typing import List
from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt

from .device import DirectionalPort
from .channel import Channel, SPECTRUM

MC_TEMPLATE = {
    "channel": None,
    "add": {
        "port": None
    },
    "drop": {
        "port": None
    },
    "power":
        {
            "common-in": None,
            "common-out": None,
            "leaf-in": None,
            "leaf-out": None
        }
}


class NetworkPath:
    """Representation of a network path connecting two directional ports.

    This class represents a network path connecting two directional ports in a network graph.

    Attributes:
        direction_1 (List[DirectionalPort]): The ports in the first direction of the path.
        direction_2 (List[DirectionalPort]): The ports in the second direction of the path.
        terminal_points (List[DirectionalPort]): List of terminal ports in the path.
    """

    def __init__(self, direction_1: List[DirectionalPort], direction_2: List[DirectionalPort]):
        """Initialize a NetworkPath instance.

        Args:
            direction_1 (List[DirectionalPort]): List of directional ports in the first direction.
            direction_2 (List[DirectionalPort]): List of directional ports in the second direction.
        """
        self.direction_1 = direction_1
        self.direction_2 = direction_2
        self.terminal_points = [node for node in self.direction_1 if node.is_terminal]

    @property
    def ports(self):
        """Get a list of non-terminal ports in the network path.

        Returns:
            List[DirectionalPort]: List of non-terminal ports in the path.
        """
        all_ports = [node for node in self.direction_1 if not node.is_terminal]
        all_ports += [node for node in self.direction_2 if not node.is_terminal]
        return list(set(all_ports))

    @property
    def devices(self):
        """Get a list of devices in the network path.

        Returns:
            List[Device]: List of devices in the path.
        """
        all_devices = [node.device for node in self.direction_1 if not node.is_terminal]
        all_devices += [node.device for node in self.direction_2 if not node.is_terminal]
        return list(set(all_devices))

    @property
    def spectrum_occupancy(self):
        """Get the spectrum occupancy of the path.

        Returns:
            np.ndarray: The spectrum occupancy of the path.
        """
        spectrum_occupancy = np.zeros(SPECTRUM["bandwidth"], dtype=bool)

        for device in self.devices:
            spectrum_occupancy |= device.spectrum_occupancy

        return spectrum_occupancy

    def generate_configuration(self, channel: Channel, directory: str):
        """Generate configuration files for the network path.

        Args:
            channel (Channel): The channel to configure in the path.
            directory (str): The directory to save configuration files in.

        Returns:
            None
        """

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create channel plan file
        with open(os.path.join(directory, "channel_plan.json"), "w") as f:
            json.dump(channel.channel_plan, f, indent=4)

        # Create media channel files
        mc_template = deepcopy(MC_TEMPLATE)
        mc_template["channel"] = channel.name
        device_media_channels = {device.name: {"media-channels": [deepcopy(mc_template)]} for device in self.devices}

        for port in self.ports:
            port.add_port_config(device_media_channels[port.device.name])

        for device in self.devices:
            with open(os.path.join(directory, f"{device.name}.json"), "w") as f:
                json.dump(device_media_channels[device.name], f, indent=4)

    def visualize_occupancy(self):
        """Visualize the spectrum occupancy of the path.

        Returns:
            None
        """
        int_array = self.spectrum_occupancy.astype(int)
        plt.figure(figsize=(10, 5))
        plt.step(np.arange(len(int_array)) + SPECTRUM["lower_bound"], int_array, where='mid')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Occupied (True or False)')
        plt.title('Spectrum Occupancy')
        plt.ylim(-0.1, 1.1)  # Set y-axis limits to show only 0 and 1 values
        plt.grid()
        plt.show()
