#pylint: skip-file
"""
This module was made to handle all the interface related operations for
Wifiphisher.py
"""

import pyric
import pyric.pyw as pyw
import random
import dbus
from constants import *

class NotEnoughInterfacesFoundError(Exception):
    """
    Exception class to raise in case of a finding less than enough interfaces.
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A NotEnoughInterfacesFoundError object
        :type self: NotEnoughInterfacesFoundError
        :return: None
        :rtype: None
        """

        message = ("There are not enough wireless interfaces for the tool to "
                   "run! Please ensure that at least two wireless adapters "
                   "are connected to the device and they are compatible " +
                   "(drivers should support netlink). At "
                   "least one must support Master (AP) mode and another "
                   "must support Monitor mode.\n"
                   "Otherwise, you may try --nojamming option that will turn "
                   "off the deauthentication phase.")
        Exception.__init__(self, message)


class NoApInterfaceFoundError(Exception):
    """
    Exception class to raise in case of a not finding a valid AP interface.
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A NoApInterfaceFoundError object
        :type self: NoApInterfaceFoundError
        :return: None
        :rtype: None
        """

        message = ("We have failed to find a wireless interface that supports"
                   " AP mode! Please make sure that all the wireless adapters "
                   "are connected and they are compatible.")
        Exception.__init__(self, message)


class NoMonitorInterfaceFoundError(Exception):
    """
    Exception class to raise in case of a not finding a valid monitor
    interface.
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A NoMonitorInterfaceFoundError object
        :type self: NoMonitorInterfaceFoundError
        :return: None
        :rtype: None
        """

        message = ("We have failed to find a wireless interface that supports"
                   " monitor mode! Please make sure that all the wireless "
                   "adapters are connected and they are compatible.")
        Exception.__init__(self, message)


class JammingInterfaceInvalidError(Exception):
    """
    Exception class to raise in case of a invalid jamming interface.
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A JammingInterfaceInvalidError object
        :type self: JammingInterfaceInvalidError
        :return: None
        :rtype: None
        """

        message = ("We have failed to set the jamming interface(-jI)! This is "
                   "either due to the fact that we were unable to find the "
                   "given interface in the available interfaces or the given "
                   "interface was incompatible.")
        Exception.__init__(self, message)


class ApInterfaceInvalidError(Exception):
    """
    Exception class to raise in case of a invalid ap interface.
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A ApInterfaceInvalidError object
        :type self: ApInterfaceInvalidError
        :return: None
        :rtype: None
        """

        message = ("We have failed to set the access point interface (-aI)! "
                   "This is either due to the fact that we were unable to find"
                   " the given interface in the available interfaces or the "
                   "given interface was incompatible.")
        Exception.__init__(self, message)


class  DeauthInterfaceMacAddrInvalidError(Exception):
    """
    Exception class to raise in case of specifying invalid mac address for
    jamming interface
    :param self: A DeauthInterfaceMacAddrInvalidError object
    :type self: DeauthInterfaceMacAddrInvalidError
    :return: None
    :rtype: None
    """

    def __init__(self):
        """
        Construct the class.

        :param self: A DeauthInterfaceMacAddrInvalidError object
        :type self: DeauthInterfaceMacAddrInvalidError
        :return: None
        :rtype: None
        """
        message = ("We have failed to set the mac address for jamming interface (-iDM)! "
               "This is due to the specified mac address may be invalid")
        Exception.__init__(self, message)

class  ApInterfaceMacAddrInvalidError(Exception):
    """
    Exception class to raise in case of specifying invalid mac address for
    ap interface
    :param self: An ApInterfaceMacAddrInvalidError object
    :type self: ApInterfaceMacAddrInvalidError
    :return: None
    :rtype: None
    """

    def __init__(self):
        """
        Construct the class.

        :param self: An ApInterfaceMacAddrInvalidError object
        :type self: ApInterfaceMacAddrInvalidError
        :return: None
        :rtype: None
        """

        message = ("We have failed to set the mac address for ap interface (-iAM)! "
               "This is due to the specified mac address may be invalid")
        Exception.__init__(self, message)

class DeauthInterfaceManagedByNMError(Exception):
    """
    Exception class to raise in case of NetworkManager controls the
    deauth interface.
    :param self: A DeauthInterfaceManagedByNMError object
    :type self: DeauthInterfaceManagedByNMError
    :return: None
    :rtype: None
    """
    def __init__(self):
        """
        Construct the class.

        :param self: An DeauthInterfaceManagedByNMError object
        :type self: DeauthInterfaceManagedByNMError object
        :return: None
        :rtype: None
        """

        message = ("We have failed to specify the jamming interface. This due to "
               "the specified interface is controlling by NetworkManager.")
        Exception.__init__(self, message)

class ApInterfaceManagedByNMError(Exception):
    """
    Exception class to raise in case of NetworkManager controls the
    AP interface.
    :param self: An ApInterfaceManagedByNMError object
    :type self: ApInterfaceManagedByNMError
    :return: None
    :rtype: None
    """
    def __init__(self):
        """
        Construct the class.

        :param self: An ApInterfaceManagedByNMError object
        :type self: ApInterfaceManagedByNMError object
        :return: None
        :rtype: None
        """

        message = ("We have failed to specify the AP interface. This due to "
               "the specified interface is controlling by NetworkManager.")
        Exception.__init__(self, message)

class NetworkAdapter(object):
    """
    This class represents a newtrok interface (network adapter).
    """

    def __init__(self, name):
        """
        Setup the class with all the given arguments.

        :param self: A NetworkAdapter object
        :param name: Name of the interface
        :type self: NetworkAdapter
        :type name: str
        :return: None
        :rtype: None
        .. note: the availability of monitor mode and AP mode is set to False
            by default
        """

        # Setup the fields
        self._name = name
        self._support_ap_mode = False
        self._support_monitor_mode = False
        self.being_used = False
        self._prev_mac = None
        self._current_mac = None
        self.is_internet_iface = False

        # Set monitor and AP mode if card supports it
        card = pyw.getcard(name)
        modes = pyw.devmodes(card)
        mac = pyw.macget(card)

        if "monitor" in modes:
            self._support_monitor_mode = True
        if "AP" in modes:
            self._support_ap_mode = True
        #set the current and prev mac to the origianl mac
        self._prev_mac = mac
        self._current_mac = mac

    def _generate_random_address(self):
        """
        Make and return the randomized MAC address

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: A MAC address
        :rtype str
        """

        mac_addr = DEFAULT_OUI + ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255),\
                random.randint(0, 255), random.randint(0, 255))
        return mac_addr

    def randomize_interface_mac(self, mac=None):
        """
        Randomize the MACs for the network adapters

        :param self: A NetworkAdapter object
        :param mac: A MAC address 
        :type self: NetworkAdapter
        :type mac: string
        :return: None
        :rtype: None
        """
        mac_addr = self._generate_random_address() if mac is None else mac
        card = pyw.getcard(self.get_name())
        pyw.down(card)
        mode = pyw.modeget(card)
        if mode != 'managed':
            pyw.modeset(card, 'managed')
        pyw.macset(card, mac_addr)
        #change to the original mode
        pyw.modeset(card, mode)
        self._current_mac = mac_addr
   

    def get_name(self):
        """
        Return the name of the interface.

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The name of the interface
        :rtype: str
        """

        return self._name

    def get_current_mac(self):
        """
        Return the MAC address of the interface.

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: The mac address of the interface
        :rtype: str
        """
        return self._current_mac

    def has_ap_mode(self):
        """
        Return whether the interface supports AP mode.

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: True if interface supports AP mode and False otherwise
        :rtype: bool
        """

        return self._support_ap_mode

    def has_monitor_mode(self):
        """
        Return whether the interface supports monitor mode.

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: True if interface supports monitor mode and False otherwise
        :rtype: bool
        """

        return self._support_monitor_mode

    def set_channel(self, channel):
        """
        Set the device channel to the provided channel.

        :param self: A NetworkAdapter object
        :param channel: A channel number
        :type self: NetworkAdapter
        :type channel: string
        :return: None
        :rtype: None
        """
        card = pyw.getcard(self._name)
        pyw.chset(card, channel, None)


class NetworkManager(object):
    """
    This class represents a network manager where it handles all the management
    for the interfaces.
    """

    def __init__(self):
        """
        Setup the class with all the given arguments.

        :param self: A NetworkManager object
        :param jamming_argument: The jamming argument given by user
        :param ap_argument: The AP argument given by user
        :type self: NetworkManager
        :type jamming_argument: str
        :type ap_argument: str
        :return: None
        :rtype: None
        .. seealso:: NetworkAdapter
        """

        # Setup the fields
        self._interfaces = {}
        self.ap_iface = ""
        self.jam_iface = ""

        # Create, add and check compatibility for each interface
        for interface in pyw.interfaces():
            try:
                self._interfaces[interface] = NetworkAdapter(interface)
            except pyric.error as e:
                pass

    def up_ifaces(self, ifaces):
        for i in ifaces:
            card = pyw.getcard(i.get_name())
            pyw.up(card)
    

    def set_interface_mode(self, interface, mode):
        """
        Set the desired mode to the network interface.

        :param self: A NetworkManager object
        :param interface: A NetworkAdapter object
        :param mode: The mode the interface should be set to
        :type self: NetworkManager
        :type interface: NetworkAdapter
        :type mode: str
        :return: None
        :rtype: None
        :raises IfconfigCmdError: if an error is produced after executing
            ifconfig command
        .. note:: available modes are ad-hoc, managed, master, monitor,
            repeater, secondary
        .. seealso:: _ifconfig_cmd
        """

        # Get the card
        card = pyw.getcard(interface.get_name())

        # Turn off, set the mode and turn on the interface
        pyw.down(card)
        pyw.modeset(card, mode)
        pyw.up(card)

    def find_interface_automatically(self):
        """
        Find and return an interface with monitor mode support followed by
        an interface with AP mode support.

        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: a tuple containing monitor interface fallowed by AP interface
        :rtype: tuple
        :raises NoApInterfaceFoundError: if no interface with AP mode is found
        :raises NoMonitorInterfaceFoundError: if no interface with monitor mode
            is found
        .. seealso:: NetworkAdapter
        .. warning:: The function returns NetworkAdapter objects and not str
        """

        # Raise an error in case of less than two interfaces found
        if len(self._interfaces) < 2:
            raise NotEnoughInterfacesFoundError()

        # Initialize list for comparison
        ap_available = list()
        monitor_available = list()

        # Populate ap_available and monitor_available lists
        for k, interface in self._interfaces.iteritems():
            if not interface.being_used:
                # Add all the interfaces with monitor mode
                if interface.has_monitor_mode():
                    monitor_available.append(interface)
                # Add all the interfaces with AP mode
                if interface.has_ap_mode():
                    ap_available.append(interface)

        # Raise error if no interface with AP mode is found
        if len(ap_available) == 0:
            raise NoApInterfaceFoundError()
        # Raise error if no interface with monitor mode is found
        if len(monitor_available) == 0:
            raise NoMonitorInterfaceFoundError()
        # Raise error if one card is supposed to do both
        if len(monitor_available) == 1 and len(ap_available) == 1:
            if monitor_available[0] == ap_available[0]:
                raise NotEnoughInterfacesFoundError()

        # We only have one AP mode interface. We don't want to use it for
        # jamming.
        if len(monitor_available) > 1 and \
                len(ap_available) == 1 and \
                ap_available[0] in monitor_available:
            # Select an AP interface and remove it from available interfaces
            ap_interface = ap_available[0]
            ap_available.remove(ap_interface)
            # Select the first available interface with monitor mode
            for m in monitor_available:
                if m != ap_interface:
                    monitor_interface = m
            return monitor_interface, ap_interface

        # We only have one Monitor mode interface. We don't want to use it for AP.
        # Covers all other cases too
        monitor_interface = monitor_available[0]
        # Select the first available interface with monitor mode
        for a in ap_available:
            if a != monitor_interface:
                ap_interface = a

        return monitor_interface, ap_interface

    def get_jam_iface(self, interface_name):
        for k, interface in self._interfaces.iteritems():
            if k == interface_name and not interface.being_used:
                if interface.has_monitor_mode():
                    return interface
                else:
                    raise JammingInterfaceInvalidError
        raise JammingInterfaceInvalidError

    def get_ap_iface(self, interface_name=None):
        for k, interface in self._interfaces.iteritems():
            if interface_name == None and not interface.being_used:
                if interface.has_ap_mode():
                    return interface
            if k == interface_name and not interface.being_used:
                if interface.has_ap_mode():
                    return interface
                else:
                    raise ApInterfaceInvalidError
        if interface_name == None:
            raise NoApInterfaceFoundError
        raise ApInterfaceInvalidError

    def _is_iface_managed_by_nm(self, iface):
        """
        Check if the interface is managed by NetworkManager

        :param self: A NetworkManager object
        :type self: NetworkManager
        :param iface: Interface name
        :type iface: str
        :return True if nterface is managed by NetworkManager
        :rtype bool
        """
        bus = dbus.SystemBus()
        nm_proxy = bus.get_object(NM_APP_PATH, NM_MANAGER_OBJ_PATH)
        nm = dbus.Interface(nm_proxy, dbus_interface=NM_MANAGER_INTERFACE_PATH)
        devs = nm.GetDevices()
        is_managed = False
        for dev_obj_path in devs:
            dev_proxy = bus.get_object(NM_APP_PATH, dev_obj_path)
            dev = dbus.Interface(dev_proxy, dbus_interface=dbus.PROPERTIES_IFACE)
            if dev.Get(NM_DEV_INTERFACE_PATH, 'Interface') == iface:
                is_managed = dev.Get(NM_DEV_INTERFACE_PATH, 'Managed')
        return is_managed

    def set_internet_iface(self, iface):
        self.internet_iface = iface
        if pyw.iswireless(iface):
            iface_obj = self._interfaces[iface]
            iface_obj.being_used = True
            iface_obj.is_internet_iface = True
            self._interfaces[iface] = iface_obj

    def set_ap_iface(self, iface):
        """
        Specify the ap interface
        
        :param self: A NetworkManager object
        :param iface: AP interface Name
        :type self: NetworkManager
        :type iface: str
        :return: None
        """
        self.ap_iface = iface
        iface_obj = self._interfaces[iface]
        iface_obj.being_used = True
        self._interfaces[iface] = iface_obj

    def set_jam_iface(self, iface):
        """
        Specify the jamming interface
        
        :param self: A NetworkManager object
        :param iface: Deauth interface name
        :type self: NetworkManager
        :type iface: str
        :return: None
        :rtype: None
        """
        self.jam_iface = iface
        iface_obj = self._interfaces[iface]
        iface_obj.being_used = True
        self._interfaces[iface] = iface_obj
   
    def check_ifaces_uncontrolled_by_nm(self):
        """
        Check the interfaces are uncontrolled by NM
        
        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: None
        :rtype: None
        :raises DeauthInterfaceManagedByNMError if deauth interface is in managed state
        :raises ApInterfaceManagedByNMError if ap interface is in managed state
        """

        for iface, iface_obj in self._interfaces.iteritems():
            if iface == self.jam_iface:
                if self._is_iface_managed_by_nm(iface):
                    raise DeauthInterfaceManagedByNMError
            elif iface == self.ap_iface:
                if self._is_iface_managed_by_nm(iface):
                    raise ApInterfaceManagedByNMError 

    def reset_ifaces_to_managed(self):
        for k, i in self._interfaces.iteritems():
            if i.being_used and not i.is_internet_iface:
                self.set_interface_mode(i, "managed")
    
    def randomize_ap_interface_mac_addr(self, mac=None):
        """
        randomzie the mac address of ap interface

        :param self: A NetworkManager object
        :param mac: A mac address
        :type self: NetworkManager
        :type mac: str
        :return: None
        :raises ApInterfaceMacAddrInvalidError if specified mac addr is
                invalid
        :rtype: None 
        """
        try:
            self._interfaces[self.ap_iface].randomize_interface_mac(mac)
        except pyric.error:
            raise ApInterfaceMacAddrInvalidError()

    def randomize_deauth_interface_mac_addr(self, mac=None):
        """
        randomzie the mac address of deauth interface

        :param self: A NetworkManager object
        :param mac: A mac address
        :type self: NetworkManager
        :type mac: str
        :return: None
        :raises DeauthInterfaceMacAddrInvalidError if specified mac addr is
                invalid
        :rtype: None 
        """
        try:
            self._interfaces[self.jam_iface].randomize_interface_mac(mac)
        except pyric.error:
            raise DeauthInterfaceMacAddrInvalidError()

    def recover_mac_address_to_original(self):
        """
        Recover the mac addresses to original one on exit

        :param self: A NetworkManager object
        :type self: NetworkManager
        :return: None
        :rtype: None 
        """
        for k, i in self._interfaces.iteritems():
            if i._prev_mac != i._current_mac:
                card = pyw.getcard(i.get_name())
                pyw.down(card)
                pyw.macset(card, i._prev_mac) 
                pyw.up(card)

    def on_exit(self):
        """
        Reset interfaces to managed on exit

        :param self: A NetworkManager object
        :return: None
        :rtype: None 
        """
        self.reset_ifaces_to_managed()
        self.recover_mac_address_to_original()
