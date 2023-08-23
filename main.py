from src import (Network, Channel,
                 CzechLightLineDegree, CzechLightAddDrop, TerminalPoint,
                 condense_path, create_random_channels)


def test_1():
    tp_1 = "TP1_A"
    tp_2 = "TP1_B"

    channel_1 = Channel(191_325_000, 191_375_000)  # 13.5
    channel_2 = Channel(191_425_000, 191_475_000)  # 14.5
    channel_3 = Channel(191_575_000, 191_625_000)  # 16.0
    channel_4 = Channel(192_375_000, 192_425_000)  # 24.0
    channel_5 = Channel(194_225_000, 194_275_000)  # 42.5
    channel_6 = Channel(195_975_000, 196_025_000)  # 60.0
    channel_7 = Channel(196_075_000, 196_125_000)  # 61.0

    channel_8 = Channel(191_550_000, 191_650_000)  # 16 (100GHz)
    channel_9 = Channel(192_350_000, 192_450_000)  # 24 (100GHz)
    channel_10 = Channel(194_200_000, 194_300_000)  # 42 (100GHz)
    channel_11 = Channel(195_950_000, 196_050_000)  # 60 (100GHz)

    ln_1 = CzechLightLineDegree("LN1_A")
    ln_1.add_channels([channel_1, channel_3, channel_8, channel_9])
    ln_2 = CzechLightLineDegree("LN2_A")
    ln_3 = CzechLightLineDegree("LN1_B")
    ln_3.add_channels([channel_5, channel_7, channel_11])
    ln_4 = CzechLightLineDegree("LN2_B")

    ad1 = CzechLightAddDrop("AD1_A")
    ad2 = CzechLightAddDrop("AD1_B")

    tp1 = TerminalPoint("TP1_A")
    tp2 = TerminalPoint("TP1_B")

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

    # Find the shortest path between two end points
    path = net.shortest_path(tp_1, tp_2)

    print(f"Path from {tp_1} to {tp_2}: {path.direction_1}")
    print(f"Path from {tp_2} to {tp_1}: {path.direction_2}")
    print(f"Condensed path from {tp_1} to {tp_2}: {condense_path(path.direction_1)}")
    print(f"Condensed path from {tp_2} to {tp_1}: {condense_path(path.direction_2)}")

    path.visualize_occupancy()
    path.generate_configuration(channel_1, f"./config/{test_1.__name__}")


def test_2():
    tp_1 = "TP1_D"
    tp_2 = "TP1_B"

    devices = [
        CzechLightLineDegree("LN1_A", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN2_A", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN3_A", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN4_A", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD1_A", create_random_channels(4, [50, 100])),
        TerminalPoint("TP1_A"),

        CzechLightLineDegree("LN1_B", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN2_B", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD1_B", create_random_channels(4, [50, 100])),
        TerminalPoint("TP1_B"),

        CzechLightLineDegree("LN1_C", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN2_C", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN3_C", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD1_C", create_random_channels(4, [50, 100])),
        TerminalPoint("TP1_C"),

        CzechLightLineDegree("LN1_D", create_random_channels(4, [50, 100])),
        CzechLightLineDegree("LN2_D", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD1_D", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD2_D", create_random_channels(4, [50, 100])),
        TerminalPoint("TP1_D"),
        TerminalPoint("TP2_D"),

        CzechLightLineDegree("LN1_E", create_random_channels(4, [50, 100])),
        CzechLightAddDrop("AD1_E", create_random_channels(4, [50, 100])),
        TerminalPoint("TP1_E"),
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

    # Find the shortest path between two end points
    path = net.shortest_path(tp_1, tp_2)

    print(f"Path from {tp_1} to {tp_2}: {path.direction_1}")
    print(f"Path from {tp_2} to {tp_1}: {path.direction_2}")
    print(f"Condensed path from {tp_1} to {tp_2}: {condense_path(path.direction_1)}")
    print(f"Condensed path from {tp_2} to {tp_1}: {condense_path(path.direction_2)}")

    path.visualize_occupancy()

    channel = Channel(191_325_000, 191_375_000)  # 13.5
    path.generate_configuration(channel, f"./config/{test_2.__name__}")


if __name__ == "__main__":
    test_1()
