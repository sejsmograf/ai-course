# Wroclaw's public transport pathfinding

This repo contains project createad for the Artificial Intelligence course at Wroclaw Uniwesrity of Science and Technology.
Project focues on implementing graph search algorithms to find the shortest path between stops.
It uses Dijkstra's algorithm, and A* algorithm with different heuristics to find the shortest path between two stops
in Wroclaw's public transport network. There also is option for pseudo Traveling Salesman Problem utilizing A* algorithm
where you have to visit all stops in the network optimizing the cost of the path.

## Features

- **Interactive terminal menu** - easy to use terminal menu to choose the algorithm and stops
- **Path from stop A to stop B** - find the shortest path between two stops using Dijkstra or A* algorithm
- **Choose priority** - choose between time and change as priority for the path

## Installation
- ***(Recommended)** Create virtual pythjon environment and activate it
```
python3 -m venv env
source env/bin/activate
```
- Install required packages from requirements.txt
```
pip install -r requirements.txt
```
## Usage
- Run the program
```
python3 main.py
```
This is recommended way to run the program.


