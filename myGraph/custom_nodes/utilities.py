# from NodeGraphQt import NodeGraph, Node
import os
import Node

class Print(Node.NodeBase):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'python.utils'

    # set the initial default node name.
    NODE_NAME = 'print'

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

class Split_text(Node.NodeBase):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'python.utils'

    # set the initial default node name.
    NODE_NAME = 'split text'

    def __init__(self):
        super(Split_text, self).__init__()

        self.input_text = self.addInputPin('input_text')
        self.add_text_input(name='character_input', label='character', text = ' ')
        self.result = self.addOutputPin('result')

    def execute(self):
        split_character = self.get_property('character_input')
        self.result.setData(self.input_text.getData().split(split_character))