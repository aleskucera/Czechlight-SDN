from typing import List
from .device import DirectionalPort


def condense_path(path: List[DirectionalPort]) -> List[str]:
    """Shorten the path by removing internal connections of devices.

    Args:
        path (List[DirectionalPort]): The path to shorten.

    Returns:
        List[str]: The list of device names in the shortened path.
    """

    return [node.device.name for i, node in enumerate(path) if
            i == 0 or node.device != path[i - 1].device]
