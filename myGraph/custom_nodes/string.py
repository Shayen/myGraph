# from NodeGraphQt import NodeGraph, Node
import Node
from PySide2.QtGui import QFont

class String(Node.NodeBase):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'com.text'

    # set the initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(String, self).__init__()
        # self.set_color(25, 58, 51)

        self.add_text_input(name='value',label='Value', text='text')

        # create input and output port.
        self.add_output('value')

class Split_text(Node.NodeBase):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'com.text.split'

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