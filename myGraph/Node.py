from NodeGraphQt import Node, Port
from NodeGraphQt import constants
import new
import command

PORT_INPUT = 1
PORT_OUTPUT = 2

class PortBase(object):

    __instance = None  # type: Port

    def __init__(self, port, port_type):
        self.__instance = port
        self.port_type = port_type

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def getData(self):
        if self.port_type == PORT_INPUT:
            # return command.getInputValue(self.instance.node())
            p_port = self.instance.connected_ports()[0]
            p_node = p_port.node()
            p_port_name = p_port.name()
            input = p_node.get_property(p_port_name)
            return input
        elif self.port_type == PORT_OUTPUT:
            return self.instance.node().get_property(self.instance.name())
        else:
            raise NotImplementedError()

    def setData(self, val):
        if self.port_type == PORT_OUTPUT:
            return self.instance.node().set_property(self.instance.name(), val)
        else:
            raise TypeError('Cannot set data to input')

    @property
    def instance(self):
        return self.__instance

    def get_instance(self):
        return self.instance

class NodeBase(Node):

    def addInputPin(self, name='input', multi_input=False, display_name=True):
        """
        Inherited from Node
        Add input :class:`Port` to node.

        Args:
            name (str): name for the input port.
            multi_input (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.

        Returns (PortBase):
            NodeGraphQt.Port: the created port object.
        """

        port = self.add_input(name = name, multi_input = multi_input, display_name=display_name)
        # port.getData = lambda : command.getInputValue(self)
        port = PortBase(port, PORT_INPUT)
        return port

    def addOutputPin(self, name='output', multi_output=True, display_name=True, default_value = None, widget_type = constants.NODE_PROP_QLABEL):
        """
        Inherited from Node
        Add output :class:`Port` to node.

        Args:
            name (str): name for the output port.
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.

        Returns (PortBase):
            NodeGraphQt.Port: the created port object.
        """

        self.create_property(name, default_value, widget_type=widget_type)

        port = self.add_output(name = name, multi_output=multi_output, display_name=display_name)
        # port.getData = new.instancemethod(getData, port, None)
        # port.setData = new.instancemethod(setData, port, None)
        port = PortBase(port, PORT_OUTPUT)
        return port

    def execute(self):
        pass