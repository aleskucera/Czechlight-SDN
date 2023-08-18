from typing import List
from .device import DirectionalPort


def condense_path(path: List[DirectionalPort]) -> List[DirectionalPort]:
    """Shorten the path by removing internal connections of devices.

    Args:
        path (List[DirectionalPort]): The path to shorten.

    Returns:
        List[DirectionalPort]: The shortened path.
    """

    return [node for i, node in enumerate(path) if i == 0 or node.device != path[i - 1].device]
