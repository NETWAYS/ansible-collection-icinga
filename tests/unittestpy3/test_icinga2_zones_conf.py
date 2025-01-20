#!/usr/bin/python3

import sys
sys.path.insert(0,'plugins/action')

import unittest
from unittest.mock import patch, Mock, MagicMock, call

import requests
from requests.exceptions import SSLError, RequestException
from ansible.parsing.yaml.objects import AnsibleSequence, AnsibleMapping


#from icinga2_zones_conf import ActionModule
from icinga2_zones_conf import get_sub_hierarchy
from icinga2_zones_conf import get_best_endpoint_attrs


class TestActionPlugin(unittest.TestCase):
    def test_get_sub_hierarchy(self):
        test_hierarchy = {
            "master": {
                "master-child": None,
                "eu": {
                    "germany": {
                        "berlin": None,
                        "nuremberg": None
                    },
                    "france": {
                        "paris": None,
                    }
                },
                "us": {
                    "washington": None,
                }
            }
        }
        test_cases = [
            # name, groups, expected
            ( "master",       [], {"master": {"master-child": None, "eu": {"germany": {"berlin": None, "nuremberg": None}, "france": {"paris": None}}, "us": {"washington": None}}} ),
            ( "master-child", [], {"master": {"master-child": None}} ),
            ( "eu",           [], {"master": {"eu": {"germany": {"berlin": None, "nuremberg": None}, "france": {"paris": None}}}} ),
            ( "us",           [], {"master": {"us": {"washington": None}}} ),
            ( "germany",      [], {"eu": {"germany": {"berlin": None, "nuremberg": None}}} ),
            ( "berlin",       [], {"germany": {"berlin": None}} ),
            ( "nuremberg",    [], {"germany": {"nuremberg": None}} ),
            ( "washington",   [], {"us": {"washington": None}} ),

            ( "master1",   ["some-ansible-group", "master"], {"master": {"master-child": None, "eu": {"germany": {"berlin": None, "nuremberg": None}, "france": {"paris": None}}, "us": {"washington": None}}} ),
            ( "master2",   ["master"],                       {"master": {"master-child": None, "eu": {"germany": {"berlin": None, "nuremberg": None}, "france": {"paris": None}}, "us": {"washington": None}}} ),
            ( "sat-ger-1", ["germany"],                      {"eu": {"germany": {"berlin": None, "nuremberg": None}}} ),
            ( "sat-ger-2", ["germany"],                      {"eu": {"germany": {"berlin": None, "nuremberg": None}}} ),
            ( "sat-ber-1", ["berlin"],                       {"germany": {"berlin": None}} ),

            ( "not-found", [],                               {} ),

        ]

        for name, groups, expected in test_cases:
            self.assertEqual(get_sub_hierarchy(test_hierarchy, name, groups), expected)


    def test_get_best_endpoint_attrs(self):
        test_inventory = {
            "hostvars": {
                "host1": {
                    "inventory_hostname": "host1",
                    "ansible_host": "192.168.122.10",
                    "custom_host_var1": "10.0.1.10",
                    "custom_host_var2": "10.0.2.10",
                },
                "host2": {
                    "inventory_hostname": "host2",
                    "ansible_host": "192.168.122.20",
                    "custom_host_var1": "10.0.1.20",
                    "custom_port_var": "6556",
                },
            }
        }
        test_cases = [
            # name, host_options, port_variable, expected
            ( "host1", [],                                       None,              {"host": "192.168.122.10", "port": "5665"} ),
            ( "host1", ["custom_host_var1", "custom_host_var2"], None,              {"host": "10.0.1.10", "port": "5665"} ),
            ( "host1", ["custom_host_var2", "custom_host_var1"], None,              {"host": "10.0.2.10", "port": "5665"} ),
            ( "host1", ["var_does_not_exist"],                   None,              {"host": "192.168.122.10", "port": "5665"} ),
            ( "host1", [],                                       "custom_port_var", {"host": "192.168.122.10", "port": "5665"} ),

            ( "host2", [],                                       None,              {"host": "192.168.122.20", "port": "5665"} ),
            ( "host2", ["custom_host_var1", "custom_host_var2"], None,              {"host": "10.0.1.20", "port": "5665"} ),
            ( "host2", ["custom_host_var2", "custom_host_var1"], None,              {"host": "10.0.1.20", "port": "5665"} ),
            ( "host2", [],                                       "custom_port_var", {"host": "192.168.122.20", "port": "6556"} ),

        ]

        for name, host_options, port_variable, expected in test_cases:
            self.assertEqual(get_best_endpoint_attrs(test_inventory, name, host_options, port_variable), expected)



## WIP
#def test_get_best_endpoint_attrs(inventory, name, host_options=list(), port_variable=None)
#def test_get_endpoints_from_zones(zones, name, inventory, upper_host_options=list(), middle_host_options=list(), lower_host_options=list(), port_variable=None)
#def test_get_zones_from_hierarchy(hierarchy, groups, parent=None)
