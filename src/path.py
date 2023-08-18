import os
import json
from copy import deepcopy
from typing import List, Union

import numpy as np
from matplotlib import pyplot as plt

from .utils import condense_path
from .device import DirectionalPort, TerminalPoint
from .channel import Channel, SPECTRUM


class NetworkPath:
    def __init__(self, path: List[DirectionalPort]):
        self.path = path
        self.condensed_path = condense_path(path)
        self.devices = [node.device for node in self.condensed_path
                        if not isinstance(node.device, TerminalPoint)]

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

    def get_configuration(self, channel: Channel, directory: str):
        channel_plan = {
            "channel-plan":
                {
                    "channel": [
                        {
                            "name": channel.name,
                            "lower-frequency": channel.lower_frequency,
                            "upper-frequency": channel.upper_frequency,
                        }
                    ]
                }
        }

        mc_template = {
            "channel": channel.name,
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
        device_media_channels = {device.name: {"media-channels": [deepcopy(mc_template)]} for device in self.devices}
        for port in self.path:
            if isinstance(port.device, TerminalPoint):
                continue
            port.add_port_config(device_media_channels[port.device.name])
        print(json.dumps(device_media_channels, indent=4))
        return None

    def visualize_occupancy(self):
        """Visualize the spectrum occupancy of the path.

        Returns:
            None
        """

        int_array = self.spectrum_occupancy.astype(int)
        print(int_array.shape)
        plt.figure(figsize=(10, 5))
        plt.step(np.arange(len(int_array)) + SPECTRUM["lower_bound"], int_array, where='mid')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Occupied (True or False)')
        plt.title('Spectrum Occupancy')
        plt.ylim(-0.1, 1.1)  # Set y-axis limits to show only 0 and 1 values
        plt.grid()
        plt.show()
