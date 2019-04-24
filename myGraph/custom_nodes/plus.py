import Node

from PySide2.QtGui import QFont

class Plus(Node.NodeBase):
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
        self.input1 = self.addInputPin('in1')
        self.input2 = self.addInputPin('in2')
        self.result = self.addOutputPin('result', default_value=0)
        # self.add_output('result')
        # self.create_property('result', 0)

    def execute(self):

        print self.input1.getData(), self.input2.getData()
        sum = int(self.input1.getData()) + int(self.input2.getData())
        self.result.setData( sum)

        # sum = 0
        # for i,p in enumerate(self.inputs()):
        #     p_node = self.input(i).connected_ports()
        #     if not p_node:
        #         continue
        #     p_port = self.input(i).connected_ports()[0]
        #     p_node = p_port.node()
        #
        #     # p_node.execute()
        #     # input = p_node.get_property('result')
        #     # input = command.getInputValue(self)
        #     input = p_node.get_property(p_port.name())
        #     # print input
        #
        #     if input:
        #         input = int(input)
        #         print (p_node.name(),p_port.name(), input)
        #
        #         sum += input
        #
        # print (self.NODE_NAME + ' :' , sum)
        # self.set_property('result', sum)

