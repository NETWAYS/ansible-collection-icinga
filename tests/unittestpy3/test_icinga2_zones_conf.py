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
from icinga2_zones_conf import get_zones_from_hierarchy
from icinga2_zones_conf import get_endpoints_from_zones


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


    def test_get_zones_from_hierarchy(self):
        test_cases = [
            # Hierarchy, ansible groups, expected
            (
                # Hierarchy
                {"master": None},
                # Ansible Groups
                {"master": ["master1"]},
                # Expected list of zones
                [{"name": "master", "endpoints": ["master1"]}]
            ),
            (
                {"master": None},
                {"master": ["master1", "master2"]},
                [{"name": "master", "endpoints": ["master1", "master2"]}]
            ),
            (
                {"inventory-name-master": None},
                {},
                [{"name": "inventory-name-master", "endpoints": ["inventory-name-master"]}]
            ),
            (
                {},
                {"master": ["master1", "master2"], "eu": ["eu1", "eu2"], "us": ["us1", "us2"]},
                []
            ),
            (
                {"master": {"eu": None, "us": None}},
                {"master": ["master1", "master2"], "eu": ["eu1", "eu2"], "us": ["us1", "us2"]},
                [
                    {
                        "name": "master",
                        "endpoints": [
                            "master1",
                            "master2"
                        ]
                    },
                    {
                        "name": "eu",
                        "parent": "master",
                        "endpoints": [
                            "eu1",
                            "eu2"
                        ]
                    },
                    {
                        "name": "us",
                        "parent": "master",
                        "endpoints": [
                            "us1",
                            "us2"
                        ]
                    }
                ]
            ),
            (
                {"master": {"eu": {"germany": {"berlin": None}}}},
                {"master": ["master1", "master2"], "eu": ["eu1", "eu2"], "germany": ["ger1", "ger2"], "berlin": ["ber1"]},
                [
                    {
                        "name": "master",
                        "endpoints": [
                            "master1",
                            "master2"
                        ]
                    },
                    {
                        "name": "eu",
                        "parent": "master",
                        "endpoints": [
                            "eu1",
                            "eu2"
                        ]
                    },
                    {
                        "name": "germany",
                        "parent": "eu",
                        "endpoints": [
                            "ger1",
                            "ger2"
                        ]
                    },
                    {
                        "name": "berlin",
                        "parent": "germany",
                        "endpoints": [
                            "ber1"
                        ]
                    }
                ]
            ),
        ]

        for hierarchy, groups, expected in test_cases:
            self.assertEqual(get_zones_from_hierarchy(hierarchy, groups), expected, "foo: " + str(get_zones_from_hierarchy(hierarchy, groups)))


#def get_endpoints_from_zones(zones, name, inventory, upper_host_options=list(), middle_host_options=list(), lower_host_options=list(), port_variable=None):
    def test_get_endpoints_from_zones(self):
        test_inventory = {
            "hostvars": {
                "master1": {
                    "possible_port": "6556",
                },
                "master2": {
                    "possible_port": "6557",
                },
                "eu1": {
                },
                "ger1": {
                }
            }
        }
        test_cases = [
            # Parameter dict, expected
            (
                {
                    "zones": [],
                    "name": "master1",
                },
                []
            ),
            (
                {
                    "zones": [
                        {
                            "name": "master",
                            "endpoints": [
                                "master1"
                            ]
                        },
                        {
                            "name": "eu",
                            "endpoints": [
                                "eu1"
                            ],
                            "parent": "master"
                        },
                        {
                            "name": "germany",
                            "endpoints": [
                                "ger1"
                            ],
                            "parent": "eu"
                        }
                    ],
                    "name": "master1",
                },
                [{"name": "master1"}, {"host": "eu1", "name": "eu1", "port": "5665"}, {"name": "ger1"}]
            ),
            (
                {
                    "zones": [
                        {
                            "name": "master",
                            "endpoints": [
                                "master1"
                            ]
                        },
                        {
                            "name": "eu",
                            "endpoints": [
                                "eu1"
                            ],
                            "parent": "master"
                        },
                        {
                            "name": "germany",
                            "endpoints": [
                                "ger1"
                            ],
                            "parent": "eu"
                        }
                    ],
                    "name": "eu1",
                },
                [
                    {"host": "master1", "name": "master1", "port": "5665"},
                    {"name": "eu1"},
                    {"host": "ger1", "name": "ger1", "port": "5665"}
                ]
            ),
            (
                {
                    "zones": [
                        {
                            "name": "master",
                            "endpoints": [
                                "master1"
                            ]
                        },
                        {
                            "name": "eu",
                            "endpoints": [
                                "eu1"
                            ],
                            "parent": "master"
                        },
                        {
                            "name": "germany",
                            "endpoints": [
                                "ger1"
                            ],
                            "parent": "eu"
                        }
                    ],
                    "name": "ger1",
                },
                [
                    {"name": "master1"},
                    {"host": "eu1", "name": "eu1", "port": "5665"},
                    {"name": "ger1"}
                ]
            ),
            (
                {
                    "zones": [{"name": "master", "endpoints": ["master1", "master2"]}],
                    "name": "master1",
                },
                [{"name": "master1"}, {"host": "master2", "name": "master2", "port": "5665"}]
            ),
            (
                {
                    "zones": [{"name": "master", "endpoints": ["master1", "master2"]}],
                    "name": "master2",
                },
                [{"host": "master1", "name": "master1", "port": "5665"}, {"name": "master2"}, ]
            ),
            (
                {
                    "zones": [{"name": "master", "endpoints": ["master1", "master2"]}],
                    "name": "master1",
                    "port_variable": "possible_port",
                },
                [{"name": "master1"}, {"host": "master2", "name": "master2", "port": "6557"}]
            ),
            (
                {
                    "zones": [{"name": "master", "endpoints": ["master1", "master2"]}],
                    "name": "master2",
                    "port_variable": "possible_port",
                },
                [{"host": "master1", "name": "master1", "port": "6556"}, {"name": "master2"}, ]
            ),
        ]

        for parameters, expected in test_cases:
            self.assertEqual(get_endpoints_from_zones(inventory=test_inventory, **parameters), expected)
            #self.assertEqual(get_endpoints_from_zones(zones, name, inventory, upper_host_options=list(), middle_host_options=list(), lower_host_options=list(), port_variable=None), expected)
