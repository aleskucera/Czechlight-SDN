import json
import logging.config

import yaml

from src.network import Network
from src.configurator import simple_configuration
from src.device import CzechLightLineDegree, CzechLightAddDrop, TerminationPoint

with open('config/logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


def test_1():
    ln_1 = CzechLightLineDegree("LN1_A")
    ln_2 = CzechLightLineDegree("LN2_A")
    ln_3 = CzechLightLineDegree("LN1_B")
    ln_4 = CzechLightLineDegree("LN2_B")

    ad1 = CzechLightAddDrop("AD1_A")
    ad2 = CzechLightAddDrop("AD1_B")

    tp1 = TerminationPoint("TP1_A")
    tp2 = TerminationPoint("TP1_B")

    net = Network()
    net.add_device(ln_1)
    net.add_device(ln_2)
    net.add_device(ln_3)
    net.add_device(ln_4)
    net.add_device(ad1)
    net.add_device(ad2)
    net.add_device(tp1)
    net.add_device(tp2)

    net.add_bidi_link("LN1_A", "E1", "LN2_A", "E1")
    net.add_bidi_link("LN1_A", "E2", "AD1_A", "E1")
    net.add_bidi_link("LN2_A", "E2", "AD1_A", "E2")
    net.add_bidi_link("AD1_A", "C1", "TP1_A", "C")

    net.add_bidi_link("LN1_B", "E1", "LN2_B", "E1")
    net.add_bidi_link("LN1_B", "E2", "AD1_B", "E1")
    net.add_bidi_link("LN2_B", "E2", "AD1_B", "E2")
    net.add_bidi_link("AD1_B", "C1", "TP1_B", "C")

    net.add_bidi_link("LN1_A", "LINE", "LN1_B", "LINE")

    net.draw()

    # Calculate the shortest path
    paths = net.shortest_path("TP1_A", "TP1_B")
    print(f"Path from TP1_A to TP1_B: {paths['direction_ab']}")
    print(f"Path from TP1_B to TP1_A: {paths['direction_ba']}")
    print(f"Condensed path from TP1_A to TP1_B: {net.condensed_path(paths['direction_ab'])}")
    print(f"Condensed path from TP1_B to TP1_A: {net.condensed_path(paths['direction_ba'])}")


def test_2():
    devices = [
        CzechLightLineDegree("LN1_A"),
        CzechLightLineDegree("LN2_A"),
        CzechLightLineDegree("LN3_A"),
        CzechLightLineDegree("LN4_A"),
        CzechLightAddDrop("AD1_A"),
        TerminationPoint("TP1_A"),

        CzechLightLineDegree("LN1_B"),
        CzechLightLineDegree("LN2_B"),
        CzechLightAddDrop("AD1_B"),
        TerminationPoint("TP1_B"),

        CzechLightLineDegree("LN1_C"),
        CzechLightLineDegree("LN2_C"),
        CzechLightLineDegree("LN3_C"),
        CzechLightAddDrop("AD1_C"),
        TerminationPoint("TP1_C"),

        CzechLightLineDegree("LN1_D"),
        CzechLightLineDegree("LN2_D"),
        CzechLightAddDrop("AD1_D"),
        CzechLightAddDrop("AD2_D"),
        TerminationPoint("TP1_D"),
        TerminationPoint("TP2_D"),

        CzechLightLineDegree("LN1_E"),
        CzechLightAddDrop("AD1_E"),
        TerminationPoint("TP1_E"),
    ]

    net = Network()
    for device in devices:
        net.add_device(device)

    # Connect point A
    net.add_bidi_link("LN1_A", "E1", "LN2_A", "E1")
    net.add_bidi_link("LN1_A", "E2", "LN3_A", "E1")
    net.add_bidi_link("LN1_A", "E3", "LN4_A", "E1")
    net.add_bidi_link("LN2_A", "E2", "LN3_A", "E2")
    net.add_bidi_link("LN2_A", "E3", "LN4_A", "E2")
    net.add_bidi_link("LN3_A", "E3", "LN4_A", "E3")

    net.add_bidi_link("LN1_A", "E4", "AD1_A", "E1")
    net.add_bidi_link("LN2_A", "E4", "AD1_A", "E2")
    net.add_bidi_link("LN3_A", "E4", "AD1_A", "E3")
    net.add_bidi_link("LN4_A", "E4", "AD1_A", "E4")

    net.add_bidi_link("AD1_A", "C1", "TP1_A", "C")

    # Connect point B
    net.add_bidi_link("LN1_B", "E1", "LN2_B", "E1")
    net.add_bidi_link("LN1_B", "E2", "LN2_B", "E2")

    net.add_bidi_link("LN1_B", "E2", "AD1_B", "E1")
    net.add_bidi_link("LN2_B", "E2", "AD1_B", "E2")

    net.add_bidi_link("AD1_B", "C1", "TP1_B", "C")

    # Connect point C
    net.add_bidi_link("LN1_C", "E1", "LN2_C", "E1")
    net.add_bidi_link("LN1_C", "E2", "LN3_C", "E1")
    net.add_bidi_link("LN2_C", "E2", "LN3_C", "E2")

    net.add_bidi_link("LN1_C", "E2", "AD1_C", "E1")
    net.add_bidi_link("LN2_C", "E2", "AD1_C", "E2")
    net.add_bidi_link("LN3_C", "E2", "AD1_C", "E3")

    net.add_bidi_link("AD1_C", "C1", "TP1_C", "C")

    # Connect point D
    net.add_bidi_link("LN1_D", "E1", "LN2_D", "E1")

    net.add_bidi_link("LN1_D", "E2", "AD1_D", "E1")
    net.add_bidi_link("LN1_D", "E3", "AD2_D", "E1")
    net.add_bidi_link("LN2_D", "E2", "AD1_D", "E2")
    net.add_bidi_link("LN2_D", "E3", "AD2_D", "E2")

    net.add_bidi_link("AD1_D", "C1", "TP1_D", "C")
    net.add_bidi_link("AD2_D", "C1", "TP2_D", "C")

    # Connect point E
    net.add_bidi_link("LN1_E", "E1", "AD1_E", "E1")

    net.add_bidi_link("AD1_E", "C1", "TP1_E", "C")

    # Connect components via the line links
    net.add_bidi_link("LN1_A", "LINE", "LN1_B", "LINE")
    net.add_bidi_link("LN2_A", "LINE", "LN1_C", "LINE")
    net.add_bidi_link("LN3_A", "LINE", "LN1_D", "LINE")
    net.add_bidi_link("LN4_A", "LINE", "LN1_E", "LINE")

    net.add_bidi_link("LN2_B", "LINE", "LN2_C", "LINE")

    net.add_bidi_link("LN3_C", "LINE", "LN2_D", "LINE")

    # Test
    net.draw()

    # Find the shortest path between two points
    path = net.shortest_path("TP1_D", "TP1_B")
    print("Shortest path between TP1_D and TP1_C:", path['direction_ab'])
    print("Condensed path:", net.condensed_path(path['direction_ab']))
    conf = json.dumps(simple_configuration(path), indent=4)
    print(f"Configuration: {conf}")


if __name__ == "__main__":
    test_1()
