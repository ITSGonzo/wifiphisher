# pylint: skip-file
""" This module tests the interface module """

import unittest
import mock
import wifiphisher.common.interfaces as interfaces
import pyric


class TestNetworkAdapter(unittest.TestCase):
    """ Tests NetworkAdapter class """

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def setUp(self, pyw):
        """ Set up the tests """

        self.adapter_name = "wlan0"
        self.card = pyw.Card
        self.mac_address = "00:00:00:00:00:00"
        self.adapter = interfaces.NetworkAdapter(self.adapter_name, self.card, self.mac_address)

    def test_name_value(self):
        """ Test the name of the interface """

        message = "Failed to get correct adapter name!"
        self.assertEqual(self.adapter.name, self.adapter_name, message)

    def test_has_ap_mode_false(self):
        """
        Test has_ap_mode variable when no AP mode support is available
        """

        message = "Failed to get False for adapter with no AP support!"
        self.assertFalse(self.adapter.has_ap_mode, message)

    def test_has_ap_mode_true(self):
        """
        Test has_ap_mode variable when AP mode support is available
        """

        # set AP support to available
        self.adapter.has_ap_mode = True

        message = "Failed to get True for adapter with AP support!"
        self.assertTrue(self.adapter.has_ap_mode, message)

    def test_has_ap_mode_set_invalid_value_error(self):
        """
        Test setting has_ap_mode variable with invalid value
        """

        with self.assertRaises(interfaces.InvalidValueError):
            self.adapter.has_ap_mode = "Invalid Value"

    def test_has_monitor_mode_false(self):
        """
        Test has_monitor_mode variable when no monitor mode support
        is available
        """

        message = "Failed to get False for adapter with no monitor support!"
        self.assertFalse(self.adapter.has_monitor_mode, message)

    def test_has_monitor_mode_true(self):
        """
        Test has_monitor_mode variable when monitor mode support is available
        """

        # set monitor support to available
        self.adapter.has_monitor_mode = True

        message = "Failed to get True for adapter with monitor support!"
        self.assertTrue(self.adapter.has_monitor_mode, message)

    def test_has_monitor_mode_set_invalid_value_error(self):
        """
        Test setting has_monitor_mode variable with invalid value
        """

        with self.assertRaises(interfaces.InvalidValueError):
            self.adapter.has_monitor_mode = "Invalid Value"

    def test_is_wireless_false(self):
        """
        Test is_wireless variable when interface is not wireless
        """

        message = "Failed to get False for adapter which is not wireless"
        self.assertFalse(self.adapter.is_wireless, message)

    def test_is_wireless_true(self):
        """ Test is_wireless variable when interface is wireless """

        # mark interface as wireless
        self.adapter.is_wireless = True

        message = "Failed to get True for adapter which is wireless"
        self.assertTrue(self.adapter.is_wireless, message)

    def test_is_wireless_set_invalid_value_error(self):
        """ Test setting is_wireless variable with invalid type"""

        with self.assertRaises(interfaces.InvalidValueError):
            self.adapter.is_wireless = "Invalid Value"

    def test_card_value(self):
        """
        Test card variable to get the pyric.Card object
        """

        message = "Failed to get the card object"
        self.assertEqual(self.card, self.adapter.card, message)

    def test_original_mac_address(self):
        """
        Test original_mac_address variable to make sure it is properly
        set
        """

        message = "Failed to get the original MAC address"
        self.assertEqual(self.adapter.original_mac_address, self.mac_address, message)

    def test_mac_address_original(self):
        """
        Test mac_address variable before a second address is specified
        """

        message = "Failed to get the current MAC address before modification"
        self.assertEqual(self.adapter.mac_address, self.mac_address, message)

    def test_mac_address_modified(self):
        """
        Test mac_address variable after a second address is specified
        """

        new_mac_address = "11:11:11:11:11:11"
        self.adapter.mac_address = new_mac_address

        message = "Failed to get the current MAC address after modification"
        self.assertEqual(self.adapter.mac_address, new_mac_address, message)


class TestInterfacePropertyDetector(unittest.TestCase):
    """ Test interface_property_detector function"""

    def setUp(self):
        """ Set up the tests """

        # setup fake card
        card = "Card"
        mac_address = "00:00:00:00:00:00"
        self.adapter = interfaces.NetworkAdapter("wlan0", card, mac_address)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_has_monitor_mode(self, pyric):
        """
        Test interface_property_detector function when the interface
        has monitor mode support
        """

        pyric.devmodes.return_value = ["monitor"]

        interfaces.interface_property_detector(self.adapter)

        message = "Failed to get monitor mode support when interface has support"
        self.assertTrue(self.adapter.has_monitor_mode, message)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_no_monitor_mode(self, pyric):
        """
        Test interface_property_detector function when the interface
        doesn't have monitor mode support
        """

        pyric.devmodes.return_value = []

        interfaces.interface_property_detector(self.adapter)

        message = "Shows interface has monitor mode when it does not"
        self.assertFalse(self.adapter.has_monitor_mode, message)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_has_ap_mode(self, pyric):
        """
        Test interface_property_detector function when the interface
        has AP mode support
        """

        pyric.devmodes.return_value = ["AP"]

        interfaces.interface_property_detector(self.adapter)

        message = "Failed to get AP mode support when interface has support"
        self.assertTrue(self.adapter.has_ap_mode, message)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_no_ap_mode(self, pyric):
        """
        Test interface_property_detector function when the interface
        doesn't have AP mode support
        """

        pyric.devmodes.return_value = []

        interfaces.interface_property_detector(self.adapter)

        message = "Shows interface has AP mode when it does not"
        self.assertFalse(self.adapter.has_ap_mode, message)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_is_wireless(self, pyric):
        """
        Test interface_property_detector function when the interface
        is wireless
        """

        pyric.iswireless.return_value = True

        interfaces.interface_property_detector(self.adapter)

        message = "Failed to show interface as wireless when it is"
        self.assertTrue(self.adapter.is_wireless, message)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_interface_property_detector_is_not_wireless(self, pyric):
        """
        Test interface_property_detector function when the interface
        is not wireless
        """

        pyric.iswireless.return_value = False

        interfaces.interface_property_detector(self.adapter)

        message = "Shows interfaces is wireless when it is not"
        self.assertFalse(self.adapter.is_wireless, message)


class TestNetworkManager(unittest.TestCase):
    """ Tests NetworkManager class """

    def setUp(self):
        """
        Set up the tests
        """

        self.network_manager = interfaces.NetworkManager()
        self.mac_address = "00:00:00:00:00:00"

    def test_is_interface_valid_valid_none(self):
        """ Tests is_interface_valid method when interface is valid """

        interface_name = "wlan0"

        self.network_manager._name_to_object[interface_name] = None

        self.network_manager.is_interface_valid(interface_name)

    def test_is_interface_valid_no_interface_error(self):
        """
        Tests is_interface_valid method when interface is non existent
        """

        interface_name = "wlan0"

        with self.assertRaises(interfaces.InvalidInterfaceError):
            self.network_manager.is_interface_valid(interface_name)

    def test_is_interface_valid_no_ap_error(self):
        """
        Tests is_interface_valid method when interface has no AP
        mode support but it is required
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_ap_mode = False
        self.network_manager._name_to_object[interface_name] = adapter

        with self.assertRaises(interfaces.InvalidInterfaceError):
            self.network_manager.is_interface_valid(interface_name, "AP")

    def test_is_interface_valid_has_ap_none(self):
        """
        Tests is_interface_valid method when interface has AP
        mode support and it is required
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_ap_mode = True
        self.network_manager._name_to_object[interface_name] = adapter

        self.network_manager.is_interface_valid(interface_name, "AP")

    def test_is_interface_valid_has_monitor_none(self):
        """
        Tests is_interface_valid method when interface has monitor
        mode support and it is required
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_monitor_mode = True
        self.network_manager._name_to_object[interface_name] = adapter

        self.network_manager.is_interface_valid(interface_name, "monitor")

    def test_is_interface_valid_no_monitor_error(self):
        """
        Tests is_interface_valid method when interface has no monitor
        mode support and it is required
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_monitor_mode = False
        self.network_manager._name_to_object[interface_name] = adapter

        with self.assertRaises(interfaces.InvalidInterfaceError):
            self.network_manager.is_interface_valid(interface_name, "monitor")

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_set_interface_mode_interface_none(self, pyric):
        """ Test set_interface_mode method"""

        interface_name = "wlan0"
        interface_object = "Card Object"
        mode = "monitor"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter

        self.network_manager.set_interface_mode(interface_name, mode)

        pyric.down.assert_called_once_with(interface_object)
        pyric.modeset.assert_called_once_with(interface_object, mode)
        pyric.up.assert_called_once_with(interface_object)

    def test_get_interface_no_interface_error(self):
        """
        Tests get_interface method when no interface can be found
        """

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface(True)

    def test_get_interface_active_interface_error(self):
        """
        Tests get_interface method when no interface can be found
        because interface is active
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface(has_monitor_mode=True)

    def test_get_interface_no_ap_available_error(self):
        """
        Tests get_interface method when interface with specified mode
        can't be found
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_ap_mode = False
        adapter.has_monitor_mode = False
        self.network_manager._name_to_object[interface_name] = adapter

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface(True)

    def test_get_interface_1_ap_monitor_interface(self):
        """
        Tests get_interface method when interface with both AP and
        monitor mode are given as input
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.has_ap_mode = True
        adapter.has_monitor_mode = True
        self.network_manager._name_to_object[interface_name] = adapter

        expected = interface_name
        actual = self.network_manager.get_interface(True, True)

        self.assertEqual(expected, actual)

    def test_get_interface_automatically_no_interface_error(self):
        """
        Tests get_interface_automatically method when no interface
        is found
        """

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface_automatically()

    def test_get_interface_automatically_monitor_only_interface_error(self):
        """
        Tests get_interface_automatically method when only monitor
        interface is found
        """

        interface_name_0 = "wlan0"
        interface_name_1 = "wlan1"
        interface_object = "Card Object"
        adapter_0 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_1 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_0.has_monitor_mode = True
        adapter_1.has_monitor_mode = True
        self.network_manager._name_to_object[interface_name_0] = adapter_0
        self.network_manager._name_to_object[interface_name_1] = adapter_1

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface_automatically()

    def test_get_interface_automatically_ap_only_interface_error(self):
        """
        Tests get_interface_automatically method when only AP interface
        is found
        """

        interface_name_0 = "wlan0"
        interface_name_1 = "wlan1"
        interface_object = "Card Object"
        adapter_0 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_1 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_0.has_ap_mode = True
        adapter_1.has_ap_mode = True
        self.network_manager._name_to_object[interface_name_0] = adapter_0
        self.network_manager._name_to_object[interface_name_1] = adapter_1

        with self.assertRaises(interfaces.InterfaceCantBeFoundError):
            self.network_manager.get_interface_automatically()

    def test_get_interface_automatically_1_ap_1_mon_interfaces(self):
        """
        Tests get_interface_automatically method when 1 AP and 1
        monitor interface are given as inputs
        """

        interface_name_0 = "wlan0"
        interface_name_1 = "wlan1"
        interface_object = "Card Object"
        adapter_0 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_1 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_0.has_monitor_mode = True
        adapter_1.has_ap_mode = True
        self.network_manager._name_to_object[interface_name_0] = adapter_0
        self.network_manager._name_to_object[interface_name_1] = adapter_1

        expected = (interface_name_0, interface_name_1)
        actual = self.network_manager.get_interface_automatically()

        self.assertEqual(expected, actual)

    def test_get_interface_automatically_1_ap_mon_1_mon_interfaces(self):
        """
        Tests get_interface_automatically method when 1 AP and monitor
        and 1 monitor interface are given as inputs
        """

        interface_name_0 = "wlan0"
        interface_name_1 = "wlan1"
        interface_object = "Card Object"
        adapter_0 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_1 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_0.has_ap_mode = True
        adapter_0.has_monitor_mode = True
        adapter_1.has_ap_mode = True
        self.network_manager._name_to_object[interface_name_0] = adapter_0
        self.network_manager._name_to_object[interface_name_1] = adapter_1

        expected = (interface_name_0, interface_name_1)
        actual = self.network_manager.get_interface_automatically()

        self.assertEqual(expected, actual)

    def test_get_interface_automatically_1_ap_1_mon_ap_interfaces(self):
        """
        Tests get_interface_automatically method when 1 AP and 1
        monitor and AP interface are given as inputs
        """

        interface_name_0 = "wlan0"
        interface_name_1 = "wlan1"
        interface_object = "Card Object"
        adapter_0 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_1 = interfaces.NetworkAdapter(interface_name_0, interface_object, self.mac_address)
        adapter_0.has_monitor_mode = True
        adapter_1.has_ap_mode = True
        adapter_1.has_monitor_mode = True
        self.network_manager._name_to_object[interface_name_0] = adapter_0
        self.network_manager._name_to_object[interface_name_1] = adapter_1

        expected = (interface_name_0, interface_name_1)
        actual = self.network_manager.get_interface_automatically()

        self.assertEqual(expected, actual)

    def test_is_interface_wired_is_wired_none(self):
        """
        Tests is_interface_wired when interface is wired
        """

        interface_name = "lan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.is_wireless = False
        self.network_manager._name_to_object[interface_name] = adapter

        self.network_manager.is_interface_wired(interface_name)

    def test_is_interface_wired_is_wireless_error(self):
        """
        Tests is_interface_wired when interface is wireless
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        adapter.is_wireless = True
        self.network_manager._name_to_object[interface_name] = adapter

        with self.assertRaises(interfaces.InvalidInternetInterfaceError):
            self.network_manager.is_interface_wired(interface_name)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_unblock_interface_is_blocked_none(self, pyric):
        """
        Tests unblock_interface when the interface is blocked
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter

        pyric.isblocked.return_value = True

        self.network_manager.unblock_interface(interface_name)

        pyric.isblocked.assert_called_once_with(interface_object)
        pyric.unblock.assert_called_once_with(interface_object)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_unblock_interface_not_blocked_none(self, pyric):
        """
        Tests unblock_interface when the interface is blocked
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter

        pyric.isblocked.return_value = False

        self.network_manager.unblock_interface(interface_name)

        pyric.isblocked.assert_called_once_with(interface_object)
        pyric.unblock.assert_not_called()

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_set_interface_channel_normal_none(self, pyric):
        """
        Tests set_interface_channel method when setting a channel
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        channel = 4
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter

        self.network_manager.set_interface_channel(interface_name, channel)

        pyric.chset.assert_called_once_with(interface_object, channel)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_start_no_interface_none(self, pyric):
        """
        Tests start method when no interface is found
        """

        pyric.interfaces.return_value = []

        self.network_manager.start()

        expected = dict()
        actual = self.network_manager._name_to_object
        self.assertDictEqual(actual, expected)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_start_has_interface_none(self, pyric):
        """
        Tests start method when interface(s) has been found
        """

        interface_name = "wlan0"
        pyric.interfaces.return_value = [interface_name]

        self.network_manager.start()

        interfaces = self.network_manager._name_to_object
        self.assertIn(interface_name, interfaces)

    @mock.patch("wifiphisher.common.interfaces.pyw.getcard")
    def test_start_interface_not_compatible_none(self, pyw):
        """
        Tests start method when interface is not supported
        """

        pyw.side_effect = pyric.error(93, "Device does not support nl80211")
        self.network_manager.start()

    @mock.patch("wifiphisher.common.interfaces.pyw.getcard")
    def test_start_interface_no_such_device_none(self, pyw):
        """
        Tests start method when there is no such interface
        """

        pyw.side_effect = pyric.error(19, "No such device")
        self.network_manager.start()

    @mock.patch("wifiphisher.common.interfaces.pyw.getcard")
    def test_start_interface_unidentified_error_error(self, pyw):
        """
        Tests start method when an unidentified error has happened
        while getting the card
        """

        pyw.side_effect = pyric.error(2220, "This is a fake error")

        with self.assertRaises(pyric.error) as error:
            self.network_manager.start()

        the_exception = error.exception
        self.assertEqual(the_exception[0], 2220, "The error was not caught.")

    def test_on_exit_no_active_none(self):
        """
        Tests on_exit method when there are no active interfaces
        """

        self.network_manager.on_exit()

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_on_exit_has_active_none(self, pyric):
        """
        Tests on_exit method when there are active interfaces
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        mode = "managed"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        self.network_manager.on_exit()

        pyric.modeset.assert_called_once_with(interface_object, mode)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_set_interface_invalid_mac_error(self, pyw):
        """
        Test set_interface_mac with an invalid MAC address to raise an
        error
        """

        pyw.macset.side_effect = pyric.error(22, "Invalid mac address")

        interface_name = "wlan0"
        interface_object = "Card Object"
        mac_address = "1"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        with self.assertRaises(interfaces.InvalidMacAddressError):
            self.network_manager.set_interface_mac(interface_name, mac_address)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_set_interface_valid_mac_none(self, pyw):
        """
        Test set_interface_mac with an valid MAC address to simulate
        normal operation
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        mac_address = "11:22:33:44:55:66"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        self.network_manager.set_interface_mac(interface_name, mac_address)

    @mock.patch("wifiphisher.common.interfaces.pyw")
    def test_set_interface_unexpected_error(self, pyw):
        """
        Test set_interface_mac when an unexpected error occurs
        """

        pyw.macset.side_effect = pyric.error(5534, "Unexpected error")

        interface_name = "wlan0"
        interface_object = "Card Object"
        mac_address = "11:22:33:44:55:66"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        with self.assertRaises(pyric.error) as error:
            self.network_manager.set_interface_mac(interface_name, mac_address)

        self.assertEqual(error.exception[0], 5534, "Unexpected error")

    @mock.patch("wifiphisher.common.interfaces.generate_random_address")
    def test_set_interface_mac_random_none(self, generator):
        """
        Test set_interface_mac_random under normal conditions
        """

        mac_address = "11:22:33:44:55:66"
        generator.return_value = mac_address

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        with mock.patch.object(interfaces.NetworkManager, "set_interface_mac") as mac_method:
            self.network_manager.set_interface_mac_random(interface_name)

            mac_method.assert_called_once_with(interface_name, mac_address)

    def test_get_interface_mac_address(self):
        """
        Test get_interface_mac under normal conditions
        """

        interface_name = "wlan0"
        interface_object = "Card Object"
        adapter = interfaces.NetworkAdapter(interface_name, interface_object, self.mac_address)
        self.network_manager._name_to_object[interface_name] = adapter
        self.network_manager._active.add(interface_name)

        self.assertEqual(self.network_manager.get_interface_mac(interface_name), self.mac_address)


class TestGenerateRandomAddress(unittest.TestCase):
    """ Test generate_random_address function """

    @mock.patch("wifiphisher.common.interfaces.random")
    def test_generate_random_address(self, random_module):
        """
        Test generate_random_address function to make sure that the
        values are correctly returned
        """

        random_module.randint.side_effect = [10, 100, 200]

        expected = "00:00:00:0a:64:c8"
        actual = interfaces.generate_random_address()
        self.assertEqual(actual, expected)
