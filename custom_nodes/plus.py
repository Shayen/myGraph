from NodeGraphQt import NodeGraph, Node

from PySide2.QtGui import QFont
import command

import command
class Plus(Node):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'op.math.math'

    # initial default node name.
    NODE_NAME = 'Plus'

    def __init__(self):
        super(Plus, self).__init__()

        # create input & output ports
        self.add_input('in1')
        self.add_input('in2')
        self.add_output('result')

        self.create_property('result', 0)

    def execute(self):
        sum = 0
        for i,p in enumerate(self.inputs()):
            p_node = self.input(i).connected_ports()
            if not p_node:
                continue
            p_port = self.input(i).connected_ports()[0]
            p_node = p_port.node()

            # p_node.execute()
            # input = p_node.get_property('result')
            # input = command.getInputValue(self)
            input = p_node.get_property(p_port.name())
            # print input

            if input:
                input = int(input)
                print (p_node.name(),p_port.name(), input)

                sum += input

        print (self.NODE_NAME + ' :' , sum)
        self.set_property('result', sum)

