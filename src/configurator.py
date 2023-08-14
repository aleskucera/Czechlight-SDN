from typing import Dict, List

from .device import TerminationPoint, DirectionalPort


def simple_configuration(path: Dict[str, List[DirectionalPort]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """Generate a simple configuration based on the given path.

    This function generates a configuration for the devices along the given path.
    The configuration includes information about frequency range and attenuation.

    Args:
        path (Dict[str, List[DirectionalPort]]): A dictionary containing the shortest paths
            in both directions between two termination points.

    Returns:
        Dict[str, Dict[str, Dict[str, float]]]: A configuration dictionary containing
            frequency and attenuation information for each device port.
    """

    conf = {}
    lower_freq, upper_freq, attenuation = 193.1, 193.9, 0.5

    for node in path['direction_ab'] + path['direction_ba']:
        if isinstance(node.device, TerminationPoint):
            continue

        device_name = node.device.name
        port_name = node.port
        direction = node.direction

        if device_name not in conf:
            conf[device_name] = {}
        if port_name not in conf[device_name]:
            conf[device_name][port_name] = {}
        if direction not in conf[device_name][port_name]:
            conf[device_name][port_name][direction] = {}

        conf[device_name][port_name][direction]["lower_freq"] = lower_freq
        conf[device_name][port_name][direction]["upper_freq"] = upper_freq
        conf[device_name][port_name][direction]["attenuation"] = attenuation

    return conf
