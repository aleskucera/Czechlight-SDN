from typing import Union, Tuple

import numpy as np

# Spectrum info in GHz
SPECTRUM = {"bandwidth": 4_800,
            "lower_bound": 191_325,
            "upper_bound": 196_125,
            "name_offset": 190_000}


class Channel:
    def __init__(self, lower_frequency: Union[int, float, str], upper_frequency: Union[int, float, str]):
        self.spec_bounds = (SPECTRUM["lower_bound"], SPECTRUM["upper_bound"])
        self.lower_frequency, self.upper_frequency = self.convert_units(lower_frequency, upper_frequency)

    @property
    def frequency_band(self):
        """Get the frequency band of the channel.

        Returns:
            np.ndarray: The frequency band of the channel.

        """
        return np.arange(self.lower_frequency, self.upper_frequency, dtype=int)

    @property
    def name(self):
        bandwidth = self.upper_frequency - self.lower_frequency
        center = self.lower_frequency + bandwidth / 2
        return f"{(center - SPECTRUM['name_offset']) / 100} ({bandwidth}GHz)"

    def convert_units(self, lower_frequency: Union[int, float, str], upper_frequency: Union[int, float, str]) \
            -> Tuple[float, float]:

        low_freq, up_freq = float(lower_frequency), float(upper_frequency)
        assert low_freq < up_freq, "The lower frequency must be lower than the upper frequency"

        if low_freq < self.spec_bounds[0]:
            low_freq, up_freq = low_freq * 1e3, up_freq * 1e3
        elif up_freq > self.spec_bounds[1]:
            low_freq, up_freq = low_freq * 1e-3, up_freq * 1e-3

        assert low_freq >= self.spec_bounds[0] and up_freq <= self.spec_bounds[1], \
            "The frequencies are not in the correct range"

        return low_freq, up_freq
