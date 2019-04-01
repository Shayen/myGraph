from NodeGraphQt import NodeGraph, Node
import os
import command

class Print(Node):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'python.print'

    # set the initial default node name.
    NODE_NAME = 'Print'

    def __init__(self):
        super(Print, self).__init__()
        self.set_color(25, 58, 51)
        self.set_icon(os.path.realpath(os.path.join(os.path.dirname(__file__), '../icons/python.png')))

        # create input and output port.
        self.add_input('Input')

    def execute(self):

        p_port = self.input(0).connected_ports()[0]
        p_node = p_port.node()
        # print 'Port name :', p_port.model.name
        input = p_node.get_property(p_port.model.name)

        print '>>', input