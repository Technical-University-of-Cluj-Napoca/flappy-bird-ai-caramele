import node
import random
import connection

class Brain:
    def __init__(self, inputs):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.network = []
        self.layers = 2

        for i in range(0, self.inputs):
            self.nodes.append(node.Node(i))
            self.nodes[i].layer = 0
        #bias
        self.nodes.append(node.Node(3))
        self.nodes[3].layer = 0

        #output
        self.nodes.append(node.Node(4))
        self.nodes[4].layer = 1

        for i in range(0, 4):
            self.connections.append(connection.Connection(self.nodes[i], self.nodes[4], random.uniform(-1, 1)))

    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []
        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    def generate_network(self):
        self.network = []
        self.connect_nodes()
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.network.append(self.nodes[i])

    def feedforward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[3].output_value = 1
        for i in range(0, len(self.network)):
            self.network[i].activate()
        output_value = self.nodes[4].output_value
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0
        return output_value