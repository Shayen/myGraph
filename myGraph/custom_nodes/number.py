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
    NODE_NAME = 'integer'

    def __init__(self):
        super(Integer, self).__init__()

        # create input & output ports
        self.result = self.addOutputPin('result')

        # create QLineEdit text input widget.
        self.add_text_input('value1', 'Text Input',text='0', tab='widgets')

    def execute(self):
        self.result.setData(int(self.get_property('value1')))

