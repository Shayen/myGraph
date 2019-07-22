# from ..NodeGraphQt import NodeGraph, Node
import Node

class Integer(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'constant'

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

class String(Node.NodeBase):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'constant'

    # set the initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(String, self).__init__()
        # self.set_color(25, 58, 51)

        self.add_text_input(name='value',label='Value', text='text')

        # create input and output port.
        self.add_output('value')