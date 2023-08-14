# CzechLight Software-Defined Network (SDN) Planning and Configuration Tool

## Introduction

CzechLight SDN Controller is a software-defined network planning and configuration tool for the CzechLight optical
network.

## Installation

TODO

## Plan of work

- [x] Create new repository for the controller
- [x] Create a NetworkX graph representation of the network
- [x] Use the NetworkX library to create find the shortest path between two nodes
- [x] From the shortest path, create a graph of the devices for visualization
- [x] From the shortest path, create a simple configuration for the devices
- [ ] From this internal representation, create YAML/JSON configuration for the devices
- [ ] Send the configuration via RESTCONF to the devices