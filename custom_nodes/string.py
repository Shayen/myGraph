from NodeGraphQt import NodeGraph, Node

from PySide2.QtGui import QFont
import command

class String(Node):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'com.text'

    # set the initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(String, self).__init__()
        self.set_color(25, 58, 51)

        self.add_text_input(name='value',label='Value', text='0')

        # create input and output port.
        self.add_output('result')
        self.create_property(name='result', value= '')


    def execute(self):
        self.set_property('result', self.get_property('value'))