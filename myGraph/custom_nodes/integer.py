# from ..NodeGraphQt import NodeGraph, Node
import Node

from PySide2.QtGui import QFont

class Integer(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'constant.math.int'

    # initial default node name.
    NODE_NAME = 'Integer'

    def __init__(self):
        super(Integer, self).__init__()

        # create input & output ports
        self.add_output('value1')

        # create QLineEdit text input widget.
        self.add_text_input('value1', 'Text Input', tab='widgets')

    def execute(self):
        pass

