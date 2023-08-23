import random
from typing import Union, Tuple, List

import numpy as np

# Spectrum info in GHz
SPECTRUM = {
    "bandwidth": 4_800,
    "lower_bound": 191_325,
    "upper_bound": 196_125,
    "name_offset": 190_000
}


class Channel:
    """Representation of a communication channel within a frequency spectrum.

    This class represents a communication channel within a specific frequency spectrum. It provides methods
    to calculate the frequency band, channel name, and channel plan.

    Attributes:
        lower_frequency (float): The lower frequency boundary of the channel.
        upper_frequency (float): The upper frequency boundary of the channel.
    """

    def __init__(self, lower_frequency: Union[int, float, str], upper_frequency: Union[int, float, str]):
        """Initialize a Channel instance.

        Args:
            lower_frequency (Union[int, float, str]): The lower frequency boundary of the channel.
            upper_frequency (Union[int, float, str]): The upper frequency boundary of the channel.
        """
        self.spec_bounds = (SPECTRUM["lower_bound"], SPECTRUM["upper_bound"])
        self.lower_frequency, self.upper_frequency = self.convert_units(lower_frequency, upper_frequency)

    @property
    def frequency_band(self):
        """Get the frequency band covered by the channel.

        Returns:
            np.ndarray: An array containing the frequencies in the channel's band.
        """

        return np.arange(self.lower_frequency, self.upper_frequency, dtype=int)

    @property
    def name(self):
        """Generate a name for the channel.

        Returns:
            str: The generated name for the channel.
        """
        bandwidth = self.upper_frequency - self.lower_frequency
        center = self.lower_frequency + bandwidth / 2
        return f"{(center - SPECTRUM['name_offset']) / 100} ({bandwidth}GHz)"

    @property
    def channel_plan(self):
        """Generate a channel plan for the channel.

        Returns:
            dict: A dictionary containing the channel plan information.
        """
        return {
            "channel-plan":
                {
                    "channel": [
                        {
                            "name": self.name,
                            "lower-frequency": self.lower_frequency,
                            "upper-frequency": self.upper_frequency,
                        }
                    ]
                }
        }

    def convert_units(self, lower_frequency: Union[int, float, str], upper_frequency: Union[int, float, str]) \
            -> Tuple[float, float]:
        """Convert frequency units to GHz.

        Args:
            lower_frequency (Union[int, float, str]): The lower frequency boundary.
            upper_frequency (Union[int, float, str]): The upper frequency boundary.

        Returns:
            Tuple[float, float]: The converted lower and upper frequency boundaries.
        """

        low_freq, up_freq = float(lower_frequency), float(upper_frequency)
        assert low_freq < up_freq, "The lower frequency must be lower than the upper frequency"

        if low_freq < self.spec_bounds[0]:
            low_freq, up_freq = low_freq * 1e3, up_freq * 1e3
        elif up_freq > self.spec_bounds[1]:
            low_freq, up_freq = low_freq * 1e-3, up_freq * 1e-3

        assert low_freq >= self.spec_bounds[0] and up_freq <= self.spec_bounds[1], \
            "The frequencies are not in the correct range"

        return low_freq, up_freq

    def __repr__(self):
        return f"Channel {self.name} ({self.lower_frequency} - {self.upper_frequency})"

    def __str__(self):
        return self.__repr__()


def create_random_channels(num_channels: int, bandwidths: List[int] = None) -> List[Channel]:
    """Create a list of randomly generated channels.

    This function generates a list of random channels with specified bandwidths. The lower and upper frequency
    boundaries for each channel are randomly selected within the specified frequency spectrum.

    Args:
        num_channels (int): The number of random channels to create.
        bandwidths (List[int], optional): List of bandwidths to randomly select from. Defaults to None.

    Returns:
        List[Channel]: A list of randomly generated Channel instances.
    """
    channels = []

    for _ in range(num_channels):
        bandwidth = random.choice(bandwidths)
        lower_bound = random.randrange(SPECTRUM["lower_bound"], SPECTRUM["upper_bound"] - bandwidth + 1, bandwidth)
        upper_bound = lower_bound + bandwidth
        channels.append(Channel(lower_bound, upper_bound))

    return channels
