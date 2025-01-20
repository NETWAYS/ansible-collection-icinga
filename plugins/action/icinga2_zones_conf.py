# -*- coding: utf-8 -*-

# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from datetime import datetime
from ansible.utils.vars import merge_hash



def get_sub_hierarchy(hierarchy, name, groups, parent=None):
    # Traverses a nested dictionary in search of a specific key (name)
    # If found, returns sub-dictionary as value for key of name "name"
    # If recursion was needed, result will be a dict with key equal to own parent key
    # E.g.
    # dict={ "master": { "europe": { "germany": {
    #                                  "berlin": None,
    #                                  "nuremberg": None
    #                                },
    #                                "france": {
    #                                  "paris": None
    #                                },
    #                              },
    #                    "usa": None
    #                  }
    #      }
    # Name="master" -> Returned: {'master': {'europe': {'germany': {'berlin': None, 'nuremberg': None}, 'france': {'paris': None}}, 'usa': None}}
    # Name="germany" -> Returned: {'europe': {'germany': {'berlin': None, 'nuremberg': None}}}


    top_level_keys = list(hierarchy.keys())

    # Check if inventory name or any group name matches top level keys of dictionary
    for possible_name in [name] + groups:
        if possible_name in top_level_keys:
            name = possible_name

    # If name is toplevel key, e.g. master
    if name in top_level_keys:
        if parent:
            # Only return the relevant sub-tree of the hierarchy
            hierarchy = {parent: {name: hierarchy[name]}}
        return hierarchy

    # If name is subkey of toplevel key
    for top_level_key in top_level_keys:
        sub_hierarchy = hierarchy[top_level_key]
        if isinstance(sub_hierarchy, dict):
            new_hierarchy = get_sub_hierarchy(sub_hierarchy, name, groups, top_level_key)
            if new_hierarchy:
                return new_hierarchy

    # Return empty dict if name not found anywhere within hierarchy
    return dict()



def get_best_endpoint_attrs(inventory, name, host_options=list(), port_variable=None):
    # Return inventory hostname and port 5665 by default
    attrs = dict()
    attrs["host"] = name
    attrs["port"] = "5665"

    for host_option in host_options + [
        #"ansible_fqdn",
        "ansible_host",
        "inventory_hostname",
    ]:
        if host_option in inventory["hostvars"][name]:
            attrs["host"] = inventory["hostvars"][name][host_option]
            break

    # WIP
    if port_variable in inventory["hostvars"][name]:
        attrs["port"] = inventory["hostvars"][name][port_variable]

    return attrs



def get_endpoints_from_zones(zones, name, inventory, upper_host_options=list(), middle_host_options=list(), lower_host_options=list(), port_variable=None):
    # Return emtpy list if no zones are given
    if not zones:
        return list()

    endpoints = list()

    own_zone             = [zone for zone in zones if name in zone["endpoints"]][0]
    own_zone_name        = own_zone["name"]
    own_parent_zone_name = own_zone["parent"] if "parent" in own_zone else None

    for zone in zones:
        for endpoint_name in zone["endpoints"]:
            endpoint = dict()
            endpoint["name"] = endpoint_name

            # If connection to own parent
            if zone["name"] == own_parent_zone_name:
                host_attributes = get_best_endpoint_attrs(inventory, endpoint_name, upper_host_options, port_variable)

            # If connection to HA partner
            elif zone["name"] == own_zone_name and endpoint_name != name:
                host_attributes = get_best_endpoint_attrs(inventory, endpoint_name, middle_host_options, port_variable)

            # If connection to direct children
            elif "parent" in zone and zone["parent"] == own_zone_name:
                host_attributes = get_best_endpoint_attrs(inventory, endpoint_name, lower_host_options, port_variable)
                print("HIER", endpoint_name, name)
                print(host_attributes)

            # If no direct connection needed
            else:
                host_attributes = None

            if host_attributes:
                endpoint.update(host_attributes)

            endpoints.append(endpoint)

    return endpoints



def get_zones_from_hierarchy(hierarchy, groups, parent=None):
    if not hierarchy:
        return list()

    zone_list = list()
    zone_name = list(hierarchy.keys())[0]

    this_zone = dict()
    this_zone["name"] = zone_name

    if parent:
        this_zone["parent"] = parent


    # get_endpoints(name, inventory, groups)
    endpoints = list()
    if zone_name in groups:
        for host in groups[zone_name]:
            endpoints.append(host)
    else:
        endpoints.append(zone_name)

    this_zone["endpoints"] = endpoints
    zone_list.append(this_zone)


    if isinstance(hierarchy[zone_name], dict):
        for key, value in hierarchy[zone_name].items():
            # Recursion step: combine current list (single zone) with each child zone
            zone_list += get_zones_from_hierarchy({key: value}, groups, parent=zone_name)

    return zone_list



class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp

        module_args = self._task.args.copy()
        #module_return = self._execute_module(
        #    module_name="setup",
        #    module_args=module_args,
        #    task_vars=task_vars, tmp=tmp
        #)

        #### Variables needed for processing
        hierarchy                  = merge_hash(module_args.pop("hierarchy", dict()), dict())
        global_zones               = module_args.pop("global_zones", list())

        # Get connection variables for host attribute
        upper_host_variables     = module_args.pop("upper", list())
        if isinstance(upper_host_variables, str):
            upper_host_variables = [upper_host_variables]

        middle_host_variables    = module_args.pop("middle", list())
        if isinstance(middle_host_variables, str):
            middle_host_variables = [middle_host_variables]

        lower_host_variables     = module_args.pop("lower", list())
        if isinstance(lower_host_variables, str):
            lower_host_variables = [lower_host_variables]

        ansible_inventory_hostname = task_vars["inventory_hostname"]
        ansible_groups             = task_vars["groups"]
        ansible_host_groups        = list(task_vars["group_names"])

        if "all" in ansible_host_groups:
            ansible_host_groups.remove("all")
        if "ungrouped" in ansible_host_groups:
            ansible_host_groups.remove("ungrouped")


        # Get sub portion of the given hierarchy starting at own parent, or self if no parent
        sub_hierarchy = get_sub_hierarchy(hierarchy, ansible_inventory_hostname, ansible_host_groups)

        # Get all zones this node needs to know (parent and all (sub-)children)
        icinga2_zones = get_zones_from_hierarchy(sub_hierarchy, ansible_groups)

        # Get all endpoints for each known zone
        icinga2_endpoints = get_endpoints_from_zones(
            icinga2_zones,
            ansible_inventory_hostname,
            task_vars,
            upper_host_options=upper_host_variables,
            middle_host_options=middle_host_variables,
            lower_host_options=lower_host_variables
        )

        # Get all global zones
        for zone in global_zones:
            zone_object = {
                "name": zone,
                "global": True
            }
            icinga2_zones.append(zone_object)

        # TO BE DONE: Global zones
        # get them from another input instead of hierarchy (e.g. global_zones: ['director-global'])
        # ...

        # Return results
        result["icinga2_zones"]     = icinga2_zones
        result["icinga2_endpoints"] = icinga2_endpoints

        return result
