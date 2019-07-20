import Node

class Loop_for(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'loop.for'

    # initial default node name.
    NODE_NAME = 'for'

    def __init__(self):
        super(Loop_for, self).__init__()

        # create input & output ports
        self.input_list = self.addInputPin('list_input', multi_input=True)
        self.start_knob = self.addOutputPin('start', default_value=None)
        self.end_knob = self.addOutputPin('end', default_value=None)
        self.next_node = self.addOutputPin('next', default_value=None)

    def execute(self):
        # node.input(0).connected_ports()[0].node().get_property(node.input(0).connected_ports()[0].name())
        result = []
        for connected_port in self.input_list.instance.connected_ports():
            data = connected_port.node().get_property(connected_port.name())
            result.append(data)

        self.result.setData(result)