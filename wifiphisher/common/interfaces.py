"""
This module was made to handle all the interface related operations of
the program
"""

import random
import pyric
import pyric.pyw as pyw
import wifiphisher.common.constants as constants


class InvalidInterfaceError(Exception):
    """ Exception class to raise in case of a invalid interface """

    def __init__(self, interface_name, mode=None):
        """
        Construct the class

        :param self: A InvalidInterfaceError object
        :param interface_name: Name of an interface
        :type self: InvalidInterfaceError
        :type interface_name: str
        :return: None
        :rtype: None
        """

        message = "The provided interface \"{0}\" is invalid!".format(interface_name)

        # provide more information if mode is given
        if mode:
            message += "Interface {0} doesn't support {1} mode".format(interface_name, mode)

        Exception.__init__(self, message)


class InvalidMacAddressError(Exception):
    """
    Exception class to raise in case of specifying invalid mac address
    """

    def __init__(self, mac_address):
        """
        Construct the class

        :param self: A InvalidMacAddressError object
        :param mac_address: A MAC address
        :type self: InvalidMacAddressError
        :type mac_address: str
        :return: None
        :rtype: None
        """
        message = "The provided MAC address {0} is invalid".format(mac_address)
        Exception.__init__(self, message)


class InvalidValueError(Exception):
    """
    Exception class to raise in case of a invalid value is supplied
    """

    def __init__(self, value, correct_value_type):
        """
        Construct the class

        :param self: A InvalidValueError object
        :param value_type: The value supplied
        :param correct_value_type: The correct value type
        :type self: InvalidValueError
        :type value_type: any
        :type correct_value_type: any
        :return: None
        :rtype: None
        """

        value_type = type(value)

        message = ("Expected value type to be {0} while got {1}."
                   .format(correct_value_type, value_type))
        Exception.__init__(self, message)


class InvalidInternetInterfaceError(Exception):
    """
    Exception class to raise in case of a invalid internet interface
    is supplied
    """

    def __init__(self, interface_name):
        """
        Construct the class

        :param self: A InvalidInternetInterfaceError object
        :param interface_name: Name of an interface
        :type self: InvalidValueError
        :type interface_name: str
        :return: None
        :rtype: None
        """

        message = "{0} interface is not acceptable as an internet interface".format(interface_name)
        Exception.__init__(self, message)


class InterfaceCantBeFoundError(Exception):
    """
    Exception class to raise in case of a invalid value is supplied
    """

    def __init__(self, interface_modes):
        """
        Construct the class

        :param self: A InterfaceCantBeFoundError object
        :param interface_modes: Modes of interface required
        :type self: InterfaceCantBeFoundError
        :type interface_modes: tuple
        :return: None
        :rtype: None
        .. note: For interface_modes the tuple should contain monitor
            mode as first argument followed by AP mode
        """

        monitor_mode = interface_modes[0]
        ap_mode = interface_modes[1]

        message = "Failed to find an interface with "

        # add appropriate mode
        if monitor_mode:
            message += "monitor"
        elif ap_mode:
            message += "AP"

        message += " mode"

        Exception.__init__(self, message)


class NetworkAdapter(object):
    """ This class represents a network interface """

    def __init__(self, name, card_obj, mac_address):
        """
        Setup the class with all the given arguments

        :param self: A NetworkAdapter object
        :param name: Name of the interface
        :param card_obj: A pyric.pyw.Card object
        :param mac_address: The MAC address of interface
        :type self: NetworkAdapter
        :type name: str
        :type card_obj: pyric.pyw.Card
        :type mac_address: str
        :return: None
        :rtype: None
        """

        # Setup the fields
        self._name = name
        self._has_ap_mode = False
        self._has_monitor_mode = False
        self._is_wireless = False
        self._card = card_obj
        self._original_mac_address = mac_address
        self._current_mac_address = mac_address

    @property
    def name(self):
        """
        Return the name of the interface

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The name of the interface
        :rtype: str
        """

        return self._name

    @property
    def has_ap_mode(self):
        """
        Return whether the interface supports AP mode

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: True if interface supports AP mode and False otherwise
        :rtype: bool
        """

        return self._has_ap_mode

    @has_ap_mode.setter
    def has_ap_mode(self, value):
        """
        Set whether the interface supports AP mode

        :param self: A NetworkAdapter object
        :param value: A value representing AP mode support
        :type self: NetworkAdapter
        :type value: bool
        :return: None
        :rtype: None
        :raises InvalidValueError: When the given value is not bool
        """

        if isinstance(value, bool):
            self._has_ap_mode = value
        else:
            raise InvalidValueError(value, bool)

    @property
    def has_monitor_mode(self):
        """
        Return whether the interface supports monitor mode

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: True if interface supports monitor mode and False otherwise
        :rtype: bool
        """

        return self._has_monitor_mode

    @has_monitor_mode.setter
    def has_monitor_mode(self, value):
        """
        Set whether the interface supports monitor mode

        :param self: A NetworkAdapter object
        :param value: A value representing monitor mode support
        :type self: NetworkAdapter
        :type value: bool
        :return: None
        :rtype: None
        :raises InvalidValueError: When the given value is not bool
        """

        if isinstance(value, bool):
            self._has_monitor_mode = value
        else:
            raise InvalidValueError(value, bool)

    @property
    def is_wireless(self):
        """
        Return whether the interface is wireless or not

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: True if interface is wireless and False otherwise
        :rtype: bool
        """

        return self._is_wireless

    @is_wireless.setter
    def is_wireless(self, value):
        """
        Set adapters's wireless mode to True

        :param self: A NetworkAdapter object
        :param value: A value representing monitor mode support
        :type self: NetworkAdapter
        :type value: bool
        :return: None
        :rtype: None
        :raises InvalidValueError: When the given value is not bool
        """

        if isinstance(value, bool):
            self._is_wireless = value
        else:
            raise InvalidValueError(value, bool)

    @property
    def card(self):
        """
        Return the card object associated with the interface

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The card object
        :rtype: pyric.pyw.Card
        """

        return self._card

    @property
    def mac_address(self):
        """
        Return the current MAC address of the interface

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The MAC of the interface
        :rtype: str
        """

        return self._current_mac_address

    @mac_address.setter
    def mac_address(self, value):
        """
        Set the MAC address of the interface

        :param self: A NetworkAdapter object
        :param value: A value representing monitor mode support
        :type self: NetworkAdapter
        :type value: str
        :return: None
        :rtype: None
        """

        self._current_mac_address = value

    @property
    def original_mac_address(self):
        """
        Return the original MAC address of the interface

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The original MAC of the interface
        :rtype: str
        """

        return self._original_mac_address


class NetworkManager(object):
    """
    This class represents a network manager where it handles all the management
    for the interfaces.
    """

    def __init__(self):
        """
        Setup the class with all the given arguments.

        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: None
        :rtype: None
        """

        self._name_to_object = dict()
        self._active = set()

    def is_interface_valid(self, interface_name, mode=None):
        """
        Check if interface is valid

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :param mode: The mode of the interface to be checked
        :type self: NetworkManager
        :type interface_name: str
        :type mode: str
        :return: True if interface is valid
        :rtype: bool
        .. note: The available modes are monitor and AP
        """

        # raise an error if interface can't be found
        try:
            interface_adapter = self._name_to_object[interface_name]

            # raise an error if interface doesn't support the mode
            if mode == "monitor" and not interface_adapter.has_monitor_mode:
                raise InvalidInterfaceError(interface_name, mode)
            elif mode == "AP" and not interface_adapter.has_ap_mode:
                raise InvalidInterfaceError(interface_name, mode)

            return True
        except KeyError:
            raise InvalidInterfaceError(interface_name)

    def set_interface_mac(self, interface_name, mac_address):
        """
        Set the specified MAC address for the interface

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :param mac_address: A MAC address
        :type self: NetworkManager
        :type interface_name: str
        :type mac_address: str
        :return: None
        :rtype: None
        .. note: This method will set the interface to managed mode
        """

        card = self._name_to_object[interface_name].card
        self.set_interface_mode(interface_name, "managed")

        try:
            pyw.macset(card, mac_address)
        # make sure to catch an invalid mac address
        except pyric.error as error:
            if error[0] == 22:
                raise InvalidMacAddressError(mac_address)
            else:
                raise

    def get_interface_mac(self, interface_name):
        """
        Return the MAC address of the interface

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :type self: NetworkManager
        :type interface_name: str
        :return: Interface MAC address
        :rtype: str
        """

        return self._name_to_object[interface_name].mac_address

    def set_interface_mac_random(self, interface_name):
        """
        Set random MAC address for the interface

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :type self: NetworkManager
        :type interface_name: str
        :return: None
        :rtype: None
        .. note: This method will set the interface to managed mode.
            Also the first 3 octets are always 00:00:00 by default
        """

        # generate a new mac address
        new_mac_address = generate_random_address()
        self._name_to_object[interface_name].mac_address = new_mac_address
        self.set_interface_mac(interface_name, new_mac_address)

    def set_interface_mode(self, interface_name, mode):
        """
        Set the specified mode for the interface

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :param mode: Mode of an interface
        :type self: NetworkManager
        :type interface_name: str
        :type mode: str
        :return: None
        :rtype: None
        .. note: Available modes are unspecified, ibss, managed, AP
            AP VLAN, wds, monitor, mesh, p2p
        """

        card = self._name_to_object[interface_name].card

        # set interface mode between brining it down and up
        pyw.down(card)
        pyw.modeset(card, mode)
        pyw.up(card)

    def get_interface(self, has_ap_mode=None, has_monitor_mode=None):
        """
        Return the name of a valid interface with modes supplied

        :param self: A NetworkManager object
        :param has_ap_mode: AP mode support
        :param has_monitor_mode: Monitor mode support
        :type self: NetworkManager
        :type has_ap_mode: bool
        :type has_monitor_mode: bool
        :return: Name of valid interface
        :rtype: str
        .. raises InterfaceCantBeFoundError: When an interface with
            supplied modes can't be found
        """

        chosen_interface = None

        # find an interface with supplied modes
        for interface, adapter in self._name_to_object.iteritems():
            # check to make sure interface is not active
            if interface not in self._active:
                # in case we have a perfect match set interface and exit
                if (adapter.has_ap_mode == has_ap_mode and
                        adapter.has_monitor_mode == has_monitor_mode):
                    chosen_interface = interface
                    break

                # in case of requested AP mode and interface has AP mode
                elif has_ap_mode and adapter.has_ap_mode:
                    # try to choose an interface that is a perfect match
                    if adapter.has_monitor_mode:
                        chosen_interface = interface
                        continue
                    else:
                        chosen_interface = interface
                        break

                # in case of requested monitor mode and interface has monitor mode
                elif has_monitor_mode and adapter.has_monitor_mode:
                    # try to choose an interface that is a perfect match
                    if adapter.has_ap_mode:
                        chosen_interface = interface
                        continue
                    else:
                        chosen_interface = interface
                        break

        # return interface if found otherwise raise an error
        if chosen_interface:
            self._active.add(chosen_interface)
            return chosen_interface
        else:
            raise InterfaceCantBeFoundError((has_ap_mode, has_monitor_mode))

    def get_interface_automatically(self):
        """
        Return a name of two interfaces
        :param self: A NetworkManager object
        :param self: NetworkManager
        :return: Name of monitor interface followed by AP interface
        :rtype: tuple
        """

        monitor_interface = self.get_interface(has_monitor_mode=True)
        ap_interface = self.get_interface(has_ap_mode=True)

        return (monitor_interface, ap_interface)

    def is_interface_wired(self, interface_name):
        """
        Check whether the interface is wired or not

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :type self: NetworkManager
        :type interface_name: str
        :return: None
        :rtype: None
        :raises InvalidInternetInterfaceError: If interface is not wired
        """

        if self._name_to_object[interface_name].is_wireless:
            raise InvalidInternetInterfaceError(interface_name)

    def unblock_interface(self, interface_name):
        """
        Unblock interface if it is blocked

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :type self: NetworkManager
        :type interface_name: str
        :return: None
        :rtype: None
        """

        card = self._name_to_object[interface_name].card

        # unblock card if it is blocked
        if pyw.isblocked(card):
            pyw.unblock(card)

    def set_interface_channel(self, interface_name, channel):
        """
        Set the channel for the interface

        :param self: A NetworkManager object
        :param interface_name: Name of an interface
        :param channel: A channel number
        :type self: NetworkManager
        :type interface_name: str
        :type channel: int
        :return: None
        :rtype: None
        """

        card = self._name_to_object[interface_name].card

        pyw.chset(card, channel)

    def start(self):
        """
        Start the network manager

        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: None
        :rtype: None
        """

        # populate our dictionary with all the available interfaces on the system
        for interface in pyw.interfaces():
            try:
                card = pyw.getcard(interface)
                mac_address = pyw.macget(card)
                adapter = NetworkAdapter(interface, card, mac_address)
                self._name_to_object[interface] = adapter
                interface_property_detector(adapter)
            # ignore devices that are not supported(93) and no such device(19)
            except pyric.error as error:
                if error[0] == 93 or error[0] == 19:
                    pass
                else:
                    raise error

    def on_exit(self):
        """
        Perform a clean up for the class

        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: None
        :rtype: None
        """

        for interface in self._active:
            mac_address = self._name_to_object[interface].original_mac_address

            self.set_interface_mac(interface, mac_address)


def interface_property_detector(network_adapter):
    """
    Add appropriate properties of the interface such as supported modes
    and wireless type(wireless)

    :param network_adapter: A NetworkAdapter object
    :type interface_name: NetworkAdapter
    :return: None
    :rtype: None
    """

    supported_modes = pyw.devmodes(network_adapter.card)

    # check for monitor, AP and wireless mode support
    if "monitor" in supported_modes:
        network_adapter.has_monitor_mode = True
    if "AP" in supported_modes:
        network_adapter.has_ap_mode = True
    if pyw.iswireless(network_adapter.name):
        network_adapter.is_wireless = True


def generate_random_address():
    """
    Make and return the randomized MAC address

    :return: A MAC address
    :rtype str
    .. warning: The first 3 octets are 00:00:00 by default
    """

    mac_address = constants.DEFAULT_OUI + ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255),
                                                                         random.randint(0, 255),
                                                                         random.randint(0, 255))
    return mac_address
