# CzechLight Software-Defined Network (SDN) Planning and Configuration Tool

## Introduction

CzechLight SDN Controller is a software-defined network planning and configuration tool for the CzechLight optical
network.

## Prerequisites

Install prerequisites using `pip`:

```bash
pip install -r requirements.txt
```

## Code structure

The key class of this project is the `Network` (`src/network.py`) class which represents the whole network.
The `Network`
class stores all devices in the network and the connections between them. The `Network` can be created with the

```python
from src.network import Network

net = Network()
```

Then the devices can be added to the network using the `add_device` method. Before we add the devices though, we need to
specify the channels that are currently used by the devices. This is done by the `Channel` class:

```python
from src.channel import Channel
from src.device import CzechLightLineDegree, CzechLightAddDrop, TerminalPoint

channel_1 = Channel(191_325_000, 191_375_000)  # 13.5
channel_2 = Channel(191_550_000, 191_650_000)  # 16 (100GHz)

# Create Line Degree example
ln = CzechLightLineDegree("LN")
ln.add_channels([channel_1, channel_2])

# Create Add Drop example
ad = CzechLightAddDrop("AD")
ad.add_channels([channel_1])

# Create Terminal Point example
tp = TerminalPoint("TP")

net.add_device(ln)
net.add_device(ad)
net.add_device(tp)
```

We also need to specify the connections between the devices. This is done by the `add_bidi_link()` method:

```python
net.add_bidi_link("LN", "E1", "AD", "E2")
```

By now the network is created, you can visualize it by calling `net.draw()`, which will draw simplified undirected
graph.

![Network](./figures/graph.png)

We can also use it to find the shortest path between two devices:

```python
path = net.find_shortest_path("LN", "AD")
```

The `path` variable is `Path` object which contains the list of `DirectionalPorts` that need to be traversed to get from
the first device to the second one and the other way around. We can also generate a configuration for the devices on
this path:

```python
channel = Channel(195_975_000, 196_025_000)  # 60.0
config = path.generate_config(channel, "./output_dir")
```

> **NOTE**
> The `generate_config` method adds to configuration constant power values (0) which is arbitrary value just for
> testing purposes. The real values will be added later.

Which will generate configuration for the devices on the path and save it to the `./output_dir` directory.

If we are not sure which channel to use, we can visualize the bandwidth usage of the devices on the path by calling
`path.visualize_occupancy()`:

![Occupancy](./figures/spectrum.png)

## Plan of work

- [x] Create new repository for the controller
- [x] Create a NetworkX graph representation of the network
- [x] Use the NetworkX library to create find the shortest path between two nodes
- [x] From the shortest path, create a graph of the devices for visualization
- [x] From the shortest path, create a simple configuration for the devices
- [x] From this internal representation, create YAML/JSON configuration for the devices
- [ ] Send the configuration via RESTCONF to the devices