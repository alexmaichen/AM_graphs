"""
# graphs.py
This is a graph-manipulation and -analysis module.
"""

from random import random, randint
import turtle
import math
from itertools import product
from typing import Callable

class Node(int):
	"""
	# Node
	used as an alias for int, for readability-reasons.
	"""

	pass

class Graph():
	"""
	# Graph
	the Graph constructor takes up to 1 argument; the graph's name.
	Graphs in this implementation are represented as an adjacency list to save space over an adjmatrix, especially in graphs with a low degree.
	it is recommended to not tamper with any field manually, exclusively call methods instead.

	for more info, consult definition for Node class
	"""

	def __init__(self, name: str = "") -> None:
		"""
		## __init__
		adjacency list (implemented here with a dictionary).
		at instantiation (optional parameter 1) or manually later (using `set_name()`), every graph can be assigned a name for readability reasons to describe what it represents
		"""

		self.nodes: dict[Node, list[Node]] = {} # {node: neighbors, ...}
		self.name: str = name

	# I/O
	def from_file(self, fname: str, ids: bool = False) -> None:
		"""
		## from_file
		read graph from file (recommended extension is .g)
		first line contains all nodes (unless left as default, so `ids = False`).
		following lines contain the node number to add adjacencies to, and following numbers are nodes to add as adjacencies.
		anything non-numeric is ignored.
		"""

		with open(fname, 'r') as f:
			lines: list[str] = f.readlines()

		if ids:
			node_ids: list[Node] = []
			for token in lines[0].strip().split():
				if token.isdigit():
					node_ids.append(Node(token))
			for node in node_ids:
				self.add_node(node)

		# adjacency
		for line in lines[ids:]:
			tokens: list[str] = line.strip().split()
			numeric: list[Node] = [Node(tok) for tok in tokens if tok.isdigit()]

			if len(numeric) < 1:
				continue # empty line or line only with comment

			u: Node = numeric[0]
			for v in numeric[1:]:
				self.add_edge(u, v)

	def to_file(self, fname: str, ids: bool = False, readable: bool = True) -> None:
		"""
		## to_file
		write graph to file (recommended extension is .g).
		first line contains all nodes (unless left as default, so `ids = False`).
		following lines contain the node number to add adjacencies to, and following numbers are nodes to add as adjacencies.
		if `readable = True`, write to file in a more human-readable manner.
		"""

		with open(fname, 'w') as f:
			if ids:
				f.write(' '.join(str(node) for node in self.nodes) + '\n')
			
				if readable:
					f.write('\n')

			# adjacency
			for node in self.nodes:
				arrow: str = " ->" * min(len(self.nodes[node]) * readable, 1)
				line: list[str] = [str(node) + arrow] + [str(neighbor) for neighbor in self.nodes[node]]
				f.write(' '.join(line) + '\n')

	def show(self) -> None:
		"""
		## show
		display graph
		"""

		if not self.name:
			print("g", self.nodes)
		else:
			print(f"g({self.name}) {self.nodes}")

	def set_name(self, name: str = "") -> None:
		"""
		takes up to 1 argument; the graph's name.
		"""
		self.name = name

	def draw(self) -> None:
		"""
		## draw
		Shoutouts to my highschool senior year where I had something very similar as a final project to turn in!
		"""

		w = 800
		h = 800

		def draw_node(x: float, y: float, label: Node) -> None:
			pen.up()
			pen.goto(x, y - node_radius)
			pen.down()
			pen.fillcolor("lightblue")
			pen.begin_fill()
			pen.circle(node_radius)
			pen.end_fill()
			pen.up()
			pen.goto(x, y - 5)
			pen.write(label, align = "center", font = ("Arial", 12, "bold"))

		def draw_arrow(x1, y1, x2, y2) -> None:
			pen.up()
			pen.goto(x1, y1)
			pen.down()
			pen.goto(x2, y2)

			# arrow
			angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
			pen.up()
			pen.goto(x2, y2)
			pen.setheading(angle + half)
			pen.right(arrow_angle)
			pen.down()
			pen.forward(arrow_length)
			pen.up()
			pen.goto(x2, y2)
			pen.setheading(angle + half)
			pen.left(arrow_angle)
			pen.down()
			pen.forward(arrow_length)

		screen: turtle._Screen = turtle.Screen()
		if not self.name:
			screen.title("graph")
		else:
			screen.title(self.name)
		screen.bgcolor("white")
		screen.setup(w, h)

		pen: turtle.Turtle = turtle.Turtle()
		pen.hideturtle()
		pen.speed(0)
		pen.pensize(2)

		radius: int = 300
		node_radius: int = 20
		arrow_length: int = 15
		arrow_angle: int = 25
		half: int = 180

		nodes: list[Node] = list(self.nodes.keys())
		n: int = len(nodes) # if n == 0, will skip all loops, make turtle finish, and return

		# circles
		positions: dict[Node, tuple[float, float]] = {}
		for i, node in enumerate(nodes):
			angle: float = 2 * math.pi * i / n
			x: float = radius * math.cos(angle)
			y: float = radius * math.sin(angle)
			positions[node] = (x, y)

		# edges
		for src, neighbors in self.nodes.items():
			for dest in neighbors:
				x1: float
				y1: float
				x2: float
				y2: float

				dx: float
				dy: float
				dist: float

				offset_x1: float
				offset_y1: float
				offset_x2: float
				offset_y2: float

				if dest not in positions:
					continue # invalid node
				x1, y1 = positions[src]
				x2, y2 = positions[dest]

				# avoid overlaps
				dx, dy = x2 - x1, y2 - y1
				dist = math.hypot(dx, dy)
				if dist == 0:
					continue # skip self-loops

				offset_x1 = x1 + dx * node_radius / dist
				offset_y1 = y1 + dy * node_radius / dist
				offset_x2 = x2 - dx * node_radius / dist
				offset_y2 = y2 - dy * node_radius / dist

				draw_arrow(offset_x1, offset_y1, offset_x2, offset_y2)

		# hide edge origins with node
		for node, (x, y) in positions.items():
			draw_node(x, y, node)

		turtle.done()

	# analysis
	def get_name(self) -> str:
		"""
		## get_name
		at instantiation, every graph can be assigned a name for readability reasons to describe what it represents
		"""

		return self.name

	def get_nodes(self) -> list[Node]:
		"""
		## get_nodes
		returns list of all nodes in graph
		"""

		return list(self.nodes.keys())

	def get_edges(self) -> list[tuple[Node, Node]]:
		"""
		## get_edges
		returns neighbors of every node
		"""

		return [(u, v) for u in self.nodes for v in self.nodes[u]]

	def get_degree(self, node: Node | None = None) -> int:
		"""
		## get_degree
		Returns amount of edges between nodes. If a node ID is provided, check outgoing degree for that node only.
		"""

		if node is None:
			return len(self.get_edges())
		
		if node not in self.nodes.keys():
			return 0 # not in graph, trivially has outgoing degree 0
		
		return len(self.nodes[node])

	def get_average_degree(self) -> float:
		"""
		## get_average_degree
		returns average degree of graph
		"""

		distr: dict[Node, int] = self.get_node_degrees()
		if distr:
			return sum(distr.values()) / len(distr)
		return 0

	def get_diameter(self) -> int:
		"""
		## get_diameter
		furthest distance between two nodes using bfs. if graph is not connected, return -1.
		"""

		def bfs(start: Node) -> dict[Node, int]:
			dist: dict[Node, int] = {start: 0}
			queue: list[Node] = [start]
			while queue:
				node = queue.pop(0)
				for neighbor in self.nodes[node]:
					if neighbor not in dist:
						dist[neighbor] = dist[node] + 1
						queue.append(neighbor)
			return dist

		if not self.is_connected():
			return -1

		max_dist = 0
		for node in self.nodes:
			distances = bfs(node)
			if len(distances) < len(self.nodes):
				return -1
			farthest = max(distances.values())
			max_dist = max(max_dist, farthest)

		return max_dist

	def get_node_degrees(self) -> dict[Node, int]:
		"""
		## get_node_degrees
		returns a dictionary of every node and its degree
		"""

		return {node: len(neighbors) for node, neighbors in self.nodes.items()}

	def are_connected(self) -> list[list[Node]]:
		"""
		## are_connected
		returns a list of all independent groups of nodes in the graph using dfs
		"""

		def dfs(node, comp) -> None:
			visited.add(node)
			comp.append(node)
			if node in self.nodes:
				for neighbor in self.nodes[node]:
					if neighbor not in visited:
						dfs(neighbor, comp)

		visited: set[Node] = set()
		components: list[list[Node]] = []

		for node in self.nodes:
			if node not in visited:
				comp: list[Node] = []
				dfs(node, comp)
				components.append(comp)

		return components

	def is_connected(self) -> bool:
		"""
		## is_connected
		checks if graph is unified, so if there is at least 1 path from at least 1 node to all others
		"""

		n: list[list[Node]] = self.are_connected()
		return len(n) == 1

	def is_strongly_connected(self) -> bool:
		"""
		## is_strongly_connected
		checks if it is possible to get from every node to every other, so if every node is in the same cycle
		"""

		def dfs(start: Node, graph: dict[Node, list[Node]]) -> set[Node]:
			visited: set[Node] = set()
			stack: list[Node] = [start]
			while stack:
				node: Node = stack.pop()
				if node not in visited:
					visited.add(node)
					if node in graph:
						for neighbor in graph[node]:
							if neighbor not in visited:
								stack.append(neighbor)
			return visited

		all_nodes: set[Node] = set(self.nodes.keys())

		if not all_nodes:
			return True

		# forward DFS
		reachable: set[Node] = dfs(next(iter(all_nodes)), self.nodes)
		if reachable != all_nodes:
			return False

		# reverse graph
		reversed_g: dict[Node, list[Node]] = {node: [] for node in all_nodes}
		for u in self.nodes:
			for v in self.nodes[u]:
				reversed_g[v].append(u)

		# reverse DFS
		reachable_rev: set[Node] = dfs(next(iter(all_nodes)), reversed_g)
		return reachable_rev == all_nodes

	def is_ugraph(self) -> bool:
		"""
		## is_ugraph
		checks if every arc is mirrored
		"""

		for u in self.nodes:
			for v in self.nodes[u]:
				if v not in self.nodes or u == v:
					return False
				if u not in self.nodes[v]:
					return False
		return True

	def is_nary_tree(self, n: int) -> bool:
		"""
		## is_nary_tree
		follows the properties of a tree:
		every node has at most n neighbors.
		there are no cycles.

		if you do not want to filter by at most n, just call `not Graph.has_cycle()` instead.
		"""
		
		in_distribution = self.get_node_degrees()
		root_count = sum(1 for node in self.nodes if in_distribution[node] == 0)

		if root_count > 1 or self.has_cycle():
			return False
		
		for node in self.nodes:
			if len(self.nodes[node]) > n:
				return False
		return True

	def is_bst(self) -> bool:
		"""
		## is_bst
		follows the properties of a binary search tree:
		is a binary tree.
		nodes are in sorted if read in infix order.
		"""

		order: int = 0

		if not self.is_nary_tree(2):
			return False # not a binary tree
		
		for node in self.nodes:
			children: list[Node] = self.nodes[node]

			if not children:
				pass

			elif len(children) == 1:
				child = children[0]
				if child == node:
					return False # duplicate
			
			elif len(children) == 2:
				left: Node
				right: Node

				left, right = children

				asc: bool = left < node < right
				desc: bool = left > node > right

				if not asc and not desc:
					return False # unordered

				if not order: # not YET set
					if asc:
						order = 1
					else:
						order = -1
				else: # order found previously, check for coherence
					if 1 + asc * -2 != order: # 1 = asc, -1 = desc. 0 is impossible since it was filtered out earlier
						return False # order flipped
		return True

	def is_planar_euler(self) -> bool:
		"""
		## is_planar_euler
		Necessary (but not sufficient) check for planarity.
		"""

		n: int = len(self.nodes)
		e: int = len(self.get_edges()) // 2 # undirected
		t: int = 3 * n - 6

		if not self.is_ugraph():
			return False
		if n < 5:
			return True
		return e <= t

	def find_shortest_path(self, start: Node, end: Node) -> list[Node]:
		"""
		## find_shortest_path
		find shortest path between two nodes using bfs (returns a list of nodes to traverse)
		"""

		if start not in self.nodes or end not in self.nodes:
			return []

		visited: set[Node] = set([start])
		prev: dict[Node, Node] = {}
		queue: list[Node] = [start]

		while queue:
			node: Node = queue.pop(0)
			if node == end:
				break
			for neighbor in self.nodes[node]:
				if neighbor not in visited:
					visited.add(neighbor)
					prev[neighbor] = node
					queue.append(neighbor)

		if end not in visited: # impossible to reach
			return []

		# reconstruct path
		path: list[Node] = [end]
		while path[-1] != start:
			path.append(prev[path[-1]])
		path.reverse()
		return path

	def has_cycle(self) -> bool:
		"""
		## has_cycle
		cycle-check via dfs graph-traversal
		"""

		def dfs(node: Node, visited: set[Node], stack: set[Node]) -> bool:
			visited.add(node)
			stack.add(node)

			if node in self.nodes:
				for neighbor in self.nodes[node]:
					if neighbor not in visited:
						if dfs(neighbor, visited, stack):
							return True
					elif neighbor in stack:
						return True
			stack.remove(node)
			return False

		visited: set[Node] = set()
		stack: set[Node] = set()

		for node in self.nodes:
			if node not in visited:
				if dfs(node, visited, stack):
					return True
		return False

	def get_chromatic_number(self) -> int:
		"""
		## colors
		returns the amount of different colors required to color the given graph
		
		source: https://en.wikipedia.org/wiki/Brooks%27_theorem
		"""

		def dfs(node: Node, visited: set[Node], stack: set[Node]) -> int:
			visited.add(node)
			stack.add(node)

			if node in self.nodes:
				for neighbor in self.nodes[node]:
					if neighbor not in visited:
						if dfs(neighbor, visited, stack):
							return len(stack) # cycle length
					elif neighbor in stack:
						return len(stack) # cycle length
			stack.remove(node)
			return 0 # no cycle

		visited: set[Node] = set()
		stack: set[Node] = set()
		u_cpy: Graph = Graph()

		u_cpy.merge(self)
		u_cpy.to_ugraph()

		if not u_cpy.is_connected():
			return -1 # error, algorithm only works on connected graphs

		for i in range(len(u_cpy.nodes.keys()) - 2):
			broken: bool = False
			for j in range(i, len(u_cpy.nodes.keys()) - 1):
				if Node(i) not in u_cpy.nodes[Node(j)]:
					# we defined u_cpy to be a ugraph:
					# if this succeeds then the other one necessarily would as well (and vice-versa)
					broken = True
					break
			if broken:
				break
		else: # graph is complete (could not find missing edge). need one color for each node. delta+1
			return 1 + max([len(u_cpy.nodes[Node(d)]) for d in u_cpy.nodes.keys()])

		for node in u_cpy.nodes:
			if node not in visited:
				res: int = dfs(node, visited, stack)
				if res % 2: # odd cycle, delta+1
					return 1 + max([len(u_cpy.nodes[Node(d)]) for d in u_cpy.nodes.keys()])
		
		return max([len(u_cpy.nodes[Node(d)]) for d in u_cpy.nodes.keys()])

	# manipulation
	def add_node(self, n1: Node) -> None:
		"""
		## add_node
		add node with no edges
		"""

		if n1 not in self.nodes.keys():
			self.nodes[n1] = []

	def add_edge(self, n1: Node, n2: Node) -> None:
		"""
		## add_edge
		add edge between two nodes. if any of the two nodes do not exist, add those node.
		"""

		if n1 not in self.nodes:
			self.add_node(n1)
		if n2 not in self.nodes:
			self.add_node(n2)
		self.nodes[n1].append(n2)

	def add_uedge(self, n1: Node, n2: Node) -> None:
		"""
		## add_uedge
		add edge both ways. useful for ugraphs.

		for the purposes of ugraphs, calling this is functionally identical to creating only regular edges, then calling to_ugraph
		"""

		self.add_edge(n1, n2)
		self.add_edge(n2, n1)

	def to_ugraph(self) -> None:
		"""
		## to_ugraph
		mirror all adjacencies
		"""

		for u in self.nodes:
			for v in self.nodes[u]:
				if v not in self.nodes:
					self.add_node(v)
				if u not in self.nodes[v]:
					self.nodes[v].append(u)

	def remove_cycles(self) -> None:
		"""
		## remove_cycles
		cut adjacencies in cycle until the cycle is broken
		"""

		visited: set[Node] = set()
		parent: dict[Node, Node|None] = {}

		def dfs(node: Node) -> None:
			visited.add(node)
			for neighbor in list(self.nodes[node]):
				if neighbor not in visited:
					parent[neighbor] = node
					dfs(neighbor)
				elif parent.get(node) != neighbor:
					self.nodes[node].remove(neighbor)

		for node in self.nodes:
			if node not in visited:
				parent[node] = None
				dfs(node)

	def balance_tree(self) -> None:
		"""
		## balance_tree
		balance tree to prevent degeneracy
		"""

		def build_balanced(vals: list[Node]) -> Node | None:
			if not vals:
				return None
			
			mid = len(vals) // 2
			root = vals[mid]
			left = build_balanced(vals[:mid])
			right = build_balanced(vals[mid+1:])

			if left != None:
				self.nodes[root].append(left)
			if right != None:
				self.nodes[root].append(right)
			return root

		sorted_nodes = sorted(self.nodes.keys())

		# reset
		self.nodes = {val: [] for val in sorted_nodes}

		build_balanced(sorted_nodes)

	def to_bst(self) -> None:
		"""
		## to_bst
		transform graph into binary search tree
		"""

		def build_bst(vals: list[Node]) -> Node | None:
			if not vals:
				return None
			
			mid: int = len(vals) // 2
			root: int = vals[mid]
			left: int | None = build_bst(vals[:mid])
			right: int | None = build_bst(vals[mid+1:])

			if left != None:
				self.nodes[root].append(left)
			if right != None:
				self.nodes[root].append(right)
			return root

		if not self.is_nary_tree(2):
			return # by definition, only binary trees can be BSTs

		sorted_nodes: list[Node] = sorted(self.nodes.keys())

		# reset
		self.nodes = {val: [] for val in sorted_nodes}

		build_bst(sorted_nodes)

	def merge(self, graph: "Graph") -> None:
		"""
		artificially merge two graphs into the same Graph object.
		
		naively takes the largest node-value of the first graph as an offset for the second one.

		create a new Graph object and successively perform merge() on it with both graphs you want to combine if you want to avoid side-effect-problems
		"""

		m: Node = max(self.nodes.keys())
		for n in graph.nodes.keys():
			self.nodes[Node(n + m)] = graph.nodes[n]

	# generation
	def gen_empty(self) -> None:
		"""
		## gen_empty
		reset graph to empty
		"""

		self.nodes = {}

	def gen_uniform(self, n: int, d: float, force_n: bool = True, clear: bool = True) -> None:
		"""
		## gen_uniform
		generates a graph with uniform degree with nodes labelled 0 to n - 1. if force_n == True, guarantees the existence of that many nodes in the graph. The graph should then have an average degree of (n**2)*d.

		recommend leaving force_n as default (True) other than to cut down on graph size or compute time.

		every node has equal chance of having an edge to any given other.
		"""

		if clear:
			self.gen_empty()

		if force_n:
			self.nodes = {Node(i): [] for i in range(n)}

		for i in range(n):
			for j in range(n):
				if i != j and random() < d:
					self.add_edge(Node(i), Node(j))

	def gen_clustered(self, n: int, s: int = 1, sd: float = 1, clear: bool = True) -> None:
		"""
		## gen_clustered
		generates a graph using preferential attachment.

		runs in O(n) but rounding may mess up the calculation, leading to a theoretical worst-case infinite runtime (however infinitely unlikely).
		
		s and sd represent the number of starting nodes, and the average degree between them respectively. this is to simulate hubs being connected among each other. recommend leaving them as default (only 1 node to start, and guaranteed to have an edge if s > 1).

		(as seen in https://www.youtube.com/watch?v=CYlon2tvywA by Veritasium)
		"""

		if clear:
			self.gen_empty()

		if not n:
			self.gen_empty()
			return
		
		self.gen_uniform(s, sd)

		id: int = s
		while id < n:
			new: Node = Node(id)
			out_deg: dict[Node, int] = {node: len(self.nodes[node]) for node in self.nodes}
			in_deg = self.get_node_degrees()
			connectivity = {node: out_deg[node] + in_deg[node] for node in self.nodes}

			total = sum(connectivity.values())

			if total == 0: # none, assign randomly. this should only happen during the first iteration
				target = Node(int(random() * id))

			else: # normalize
				norm = {node: connectivity[node] / total for node in self.nodes}
				r = random()
				cumulative = 0.0
				target = -1

				for node in self.nodes:
					cumulative += norm[node]
					if r <= cumulative:
						target = node
						break

				if target == -1: # rounding messed up the calculation :(
					continue

			self.add_node(new)
			self.add_edge(new, target)
			id += 1

	def gen_clustered2(self, n: int, clear: bool = True) -> None:
		"""
		## gen_clustered2

		generates a graph using preferential attachment where older nodes will on average have a higher degree because they've had more chances to connect.
		
		runs in O(n)

		thus, the average incoming degree of a node added with n iterations past and m iterations remaining is the harmonic series 0 + (1 / (n + 1)) + (1 / (n + 2)) + ..., m times.

		according to https://en.wikipedia.org/wiki/Harmonic_series_(mathematics):
		for m approaching +inf, the result follows ln(n + g) - 1 where (approx.) g = 0.577
		"""

		if clear:
			self.gen_empty()

		if not n:
			return
		
		self.add_node(Node(0))

		for i in range(1, n):
			self.add_edge(Node(i), Node(randint(0, i - 1)))

	def gen_collatz(self, n: int, a: int = 3, b: int = 1, div: int = 2, clear: bool = True) -> None:
		"""
		## gen_collatz
		graph the terms of the Collatz conjecture (unsolved problem in mathematics, formulated by Lothar Collatz in 1937) from 0 until at least some n.
		
		The conjecture claims that for any positive integer n with the following algorithm:
		- if a number is odd, multiply by 3 and add 1
		- else, divide by 2

		one will always eventually end up in the cycle of 4 -> 2 -> 1. 0 leads to itself, and has no incoming edges. Negative integers can also form cycles, but the behavior is much less well-known/-researched (see https://math.stackexchange.com/questions/4993544/status-of-collatz-conjecture-for-negative-integers-a-k-a-3x-1-problem). I recommend reading through this article to gain some insight as to how it works: https://www.chaos.org.uk/~eddy/math/Collatz.xhtml#:~:text=If%20you%20extend%20Collatz%20to%20%7Bintegers%7D%2C%20its%20action,%E2%86%92%20%E2%88%927%20%E2%86%92%20%E2%88%9220%20%E2%86%92%20%E2%88%9210%20%E2%86%92%20%E2%88%925.

		This also means we have no idea of the average runtime of this algorithm, or if it even always halts... however a graph plotting the total stopping time for every natural until 10,000 and a few unproven formulae for finding an expected stopping time can be found here https://math.stackexchange.com/questions/4678861/collatz-stopping-time-curves
		
		variations of this algorithm exist, as seen in https://www.youtube.com/watch?v=n63FBYqj98E by carykh.

		it is recommended to use the regular default numerical values to avoid exploding to infinity. the end-result is a long algue-like structure with a cycle as a head.

		other potentially interesting variations include:
		- anything with 0*x creates a graph with central focal point (0), to which all paths eventually lead (similar to the two gen_clustered methods but without less connections between branches, and without any cycles outside of 0).
		- running regular collatz gen with n == 0 will create only the 0-cycle
		- running regular collatz gen with n < 3 will create only the 0-cycle and the 4-2-1-cycle
		- I took some liberty over the implementation to make the regular division operation into a divide-and-floor operation to allow for divisors other than 2. increasing the divisor-term (div) can (but often doesn't) make many cases drop into stable cases faster. I recommend keeping a power of 2 for this, unfortunately other values for div diverge. there technically exists a "shortcut" for checking whether Collatz is true for some n, which consists in dividing by 2 at every step no matter the result of n % 2, which makes calculations on averagee 2 times faster at the expense of around half of all terms missing. I did not implement this optimisation here to allow for freely setting the divisor (div).
		- if a == 1 and b == 2, the variant produces all positive odd numbers.
		- if (a + b) % div != 0 and a != 0, the variant trivially diverges. among these, with a == 2 and b == 1, one produces the Mersenne primes (prime numbers one less than a power of 2).

		while this graph generation method is by no means random, it is chaotic. if you want to make it random, just call gen_collatz_random() instead, which will guarantee a randomly generated graph that does not take infinite time to calculate.
		"""

		if clear:
			self.gen_empty()

		# optimization: instead of going all the way to 1 every time, keep track of what we have already calculated
		seen: set[int] = set()

		for i in range(n):
			x = i
			while x not in seen:
				seen.add(x)
				# compute next term
				if x % div: # mod 2 by default
					y = a * x + b
				else:
					y = x // div

				self.add_edge(Node(x), Node(y))
				# continue from next term
				x = y

	def gen_collatz_random(self, graph_type: str, n: int, min: int, max: int, clear: bool = True) -> None:
		"""
		generate graph following the Collatz-function with some randomness, guaranteed to halt (assuming the Collatz conjecture is true and I implemented this correctly, at least one of which may not be true /j). check gen_collatz for more info.

		types of Collatz-like graphs:
		- "hub": a = 0. centered around one number.
		- "shape": `2**a`, `b = 0`. hub but with multiple independent centers.
		- regular: equal `2**a` and `2**b` to guarantee halting. behavior is similar to that of the regular collatz formula.
		"""

		match(graph_type):
			case "hub":
				self.gen_collatz(n, 0, randint(min, max), clear = clear)
			case "shape":
				self.gen_collatz(n, 2**randint(min, max), 0, clear = clear)
			case "regular":
				r: int = 2**randint(min, max)
				self.gen_collatz(n, r, r, clear = clear)

class StateMachine(Graph):
	"""
	# StateMachine
	A state machine is just a graph one can traverse through certain transformations. Functionally, it is equivalent to a Turing-machine.

	for more info on the general structure, consult definition for Graph class.
	"""

	def __init__(self, name: str = "") -> None:
		super().__init__(name)
		
		# constants
		self.error: Node = Node(-1)
		self.start: Node = Node(1)
		self.end: Node = Node(0)

		# structure
		self.state: list[Node] = [self.start]
		self.add_node(self.start)

	def check(self) -> bool:
		"""
		## check

		Check whether end-state has been reached. This is assumed to only be called at the END of a test.

		True means state is the end-state.
		"""

		if self.state[-1] != self.end:
			self.reset()
			return False
		self.reset()
		return True
	
	def reset(self) -> None:
		"""
		## reset
		Reset the state machine's callstack.
		"""

		self.state = [self.start]

	def next(self, t: int) -> Node:
		"""
		## next
		go from current state to next state through transformation t
		"""

		if self.state not in self.nodes.keys():
			self.state.append(self.error)
			return self.error

		# take transformation t of the latest element on the stack, and add it on the stack.
		res: Node = self.nodes[self.state[-1]][Node(t)]
		self.state.append(res)
		return res
	
	def prev(self) -> Node:
		"""
		## prev
		revert last move. if callstack is empty, return -1
		"""
		
		if not self.state:
			return self.error
		return self.state.pop()

	def to(self, n: Node) -> bool:
		"""
		## to	

		go to state n. return whether this move was successful.
		"""

		if n in self.nodes[self.state[-1]]:
			self.state.append(n)
			return True
		return False
	
	def match_s(self, path: list[Node]) -> bool:
		"""
		## match_s
		
		test whether the path is possible and valid
		"""

		for reach in path:
			if not self.to(reach):
				self.reset()
				return False
		return self.check()
	
	def match_t(self, t: list[int]) -> bool:
		"""
		## match_t

		check if a certain list of transformations (t) is valid
		"""

		for trans in t:
			self.next(trans)
			if self.state[-1] == self.error:
				self.reset()
				return False
		return self.check()

	def gen_walk(self, n: int, steps: int, force_n: bool = True, clear: bool = True) -> None:
		"""
		## gen_walk
		generates a graph with nodes labelled 0 to n - 1. if force_n == True, guarantees the existence of that many nodes in the graph.

		recommend leaving force_n as default (True) other than to cut down on graph size or compute time.

		to get similar behavior as for gen_uniform (but with guarantee of a connected graph), set steps = n*(probability of you want)
		
		Turning force_n to false guarantees that the graph is connected.

		Though this is not relevant to graph generation here, the probability of the stack having the same value at the start and end should logically be 1/n since we are picking uniformly among all possible nodes including the current node.
		
		Lets define the term "movecount" as the absolute value of the current size of the stack before a move happens, minus 1 (to account for the starting node, AKA 0 moves). Lets also define "movecount-difference" as `|(movecount 1) - (movecount 2)|`. If we were to make moving from one note to this same node impossible on the same move, the probability of landing back at the start would trivially be 1/n for any even movecount-difference after that, and impossible (0) for any odd movecount-difference.

		Setting `steps` to something greater or equal to n-1, guarantees the presence of at least one cycle.

		Trivially, taking less than 2 steps makes cycles impossible.
		"""

		if clear:
			self.gen_empty()

		if force_n:
			self.nodes = {Node(i): [] for i in range(n)}

		for _ in range(steps):
			target: Node = Node(randint(0, n-1))
			self.add_edge(self.state[-1], target)
			self.to(target)

		self.reset()

	def gen_walk2(self, g: Graph, s: Node, steps: int, clear: bool = True) -> list[Node]:
		"""
		## gen_walk
		Create another graph from random walk on a graph.

		Has the properties described in this [wikipedia article section](https://en.wikipedia.org/wiki/Random_walk#On_graphs) about random walks on graphs.
		"""

		if clear:
			self.gen_empty()
		
		self.state = [s]

		for _ in range(steps):
			target: Node = Node(randint(0, len(g.nodes[self.state[-1]]) - 1))
			self.to(target)

		r: list[Node] = self.state[:]
		self.reset()
		return r

def generate_all(n: int, produceFile: bool = False, produceFileAt: str = "", sep: str = "_", ext: str = ".g", predicate: Callable | None = None, *args) -> int:
	"""
	## generate_all
	Generates all unique directed graphs from size 0 to n, without isomorphism checks. Returns total amount of graphs generated.

	`produceFile` determines whether a file with graph data should be created (one for every graph). By default does not create.

	If `produceFile` is "True-like", `produceFileAt` gives the location to store these files. By default creates in the current directory, however I would recommend directing this to a different folder or subfolder.

	If `produceFile` is "True-like", `sep` is the filename part separator. By default an underscore.

	If `produceFile` is "True-like", `ext` is the file extension. I like the idea of files representing graphs being marked with ".g", so that is the default.

	By default, the names of output-files produced by this function will thus have the following format:
	- The number of nodes in the graph `n`.
	- Filename separator `sep` (by default 0).
	- A unique identifier for this graph. This ID will be identical for a given graph regardless of property filtering.
	- File-extension `ext` (by default ".g").

	`predicate` is an additional condition one can filter by; a "True-like" return value causes the graph to be added. This function must take a Graph object as first element, and a tuple of function arguments as second argument. It is None by default, meaning no additional filtering.

	If `predicate` is not None, any additional arguments (`args`) are passed as-is into that filtering-function.
	"""

	vertices: list[int] = list(range(n))
	possible_edges: list[tuple[int, int]] = list(product(vertices, vertices)) # get all combinations
	seen: set[Graph] = set()
	avg: float = 0

	for bits in range(2 ** len(possible_edges)): # O(2 ** (n ** 2))
		# Bits set to 1 represent edges that exist in the current graph. Just adding 1 to bits at every loop iteration guarantees graph uniqueness and hence ID. A graph's ID is basically an encoding of it.
		g: Graph = Graph()
		
		for node in range(n):
			g.add_node(Node(node))
		
		for i, edge in enumerate(possible_edges):
			if bits & (2 ** i):
				g.add_edge(Node(edge[0]), Node(edge[1]))

		if g not in seen: # filtering
			seen.add(g)
			if predicate is None or predicate(seen, args):
				avg += 1
				if produceFile:
					g.to_file(produceFileAt + str(len(g.get_nodes())) + sep + str(bits + 1) + ext)
	
	print(avg / len(seen))
	return len(seen)

if __name__ == "__main__":
	print("Do not run this module directly.")
	exit(1)
