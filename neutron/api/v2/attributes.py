# Copyright (c) 2012 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from debtcollector import moves
from neutron_lib.api import converters as lib_converters
from neutron_lib.api import validators as lib_validators
from neutron_lib import constants
import six
import webob.exc

from neutron._i18n import _
from neutron.common import _deprecate
from neutron.common import constants as n_const


# Defining a constant to avoid repeating string literal in several modules
SHARED = 'shared'

_deprecate._DeprecateSubset.and_also('UNLIMITED', lib_validators)

# TODO(HenryG): use DB field sizes (neutron-lib 0.1.1)
NAME_MAX_LEN = 255
TENANT_ID_MAX_LEN = 255
DESCRIPTION_MAX_LEN = 255
LONG_DESCRIPTION_MAX_LEN = 1024
DEVICE_ID_MAX_LEN = 255
DEVICE_OWNER_MAX_LEN = 255


def _lib(old_name):
    """Deprecate a function moved to neutron_lib.api.converters/validators."""
    new_func = getattr(lib_validators, old_name, None)
    if not new_func:
        # Try non-private name (without leading underscore)
        new_func = getattr(lib_validators, old_name[1:], None)
    if not new_func:
        # If it isn't a validator, maybe it's a converter
        new_func = getattr(lib_converters, old_name, None)
    assert new_func
    return moves.moved_function(new_func, old_name, __name__,
                                message='moved to neutron_lib',
                                version='mitaka', removal_version='ocata')


_verify_dict_keys = _lib('_verify_dict_keys')
is_attr_set = _lib('is_attr_set')
_validate_list_of_items = _lib('_validate_list_of_items')
_validate_values = _lib('_validate_values')
_validate_not_empty_string_or_none = _lib('_validate_not_empty_string_or_none')
_validate_not_empty_string = _lib('_validate_not_empty_string')
_validate_string_or_none = _lib('_validate_string_or_none')
_validate_string = _lib('_validate_string')
validate_list_of_unique_strings = _lib('validate_list_of_unique_strings')
_validate_boolean = _lib('_validate_boolean')
_validate_range = _lib('_validate_range')
_validate_no_whitespace = _lib('_validate_no_whitespace')
_validate_mac_address = _lib('_validate_mac_address')
_validate_mac_address_or_none = _lib('_validate_mac_address_or_none')
_validate_ip_address = _lib('_validate_ip_address')
_validate_ip_pools = _lib('_validate_ip_pools')
_validate_fixed_ips = _lib('_validate_fixed_ips')
_validate_nameservers = _lib('_validate_nameservers')
_validate_hostroutes = _lib('_validate_hostroutes')
_validate_ip_address_or_none = _lib('_validate_ip_address_or_none')
_validate_subnet = _lib('_validate_subnet')
_validate_subnet_or_none = _lib('_validate_subnet_or_none')
_validate_subnet_list = _lib('_validate_subnet_list')
_validate_regex = _lib('_validate_regex')
_validate_regex_or_none = _lib('_validate_regex_or_none')
_validate_subnetpool_id = _lib('_validate_subnetpool_id')
_validate_subnetpool_id_or_none = _lib('_validate_subnetpool_id_or_none')
_validate_uuid = _lib('_validate_uuid')
_validate_uuid_or_none = _lib('_validate_uuid_or_none')
_validate_uuid_list = _lib('_validate_uuid_list')
_validate_dict_item = _lib('_validate_dict_item')
_validate_dict = _lib('_validate_dict')
_validate_dict_or_none = _lib('_validate_dict_or_none')
_validate_dict_or_empty = _lib('_validate_dict_or_empty')
_validate_dict_or_nodata = _lib('_validate_dict_or_nodata')
_validate_non_negative = _lib('_validate_non_negative')

convert_to_boolean = _lib('convert_to_boolean')
convert_to_boolean_if_not_none = _lib('convert_to_boolean_if_not_none')
convert_to_int = _lib('convert_to_int')
convert_to_int_if_not_none = _lib('convert_to_int_if_not_none')
convert_to_positive_float_or_none = _lib('convert_to_positive_float_or_none')
convert_kvp_str_to_list = _lib('convert_kvp_str_to_list')
convert_kvp_list_to_dict = _lib('convert_kvp_list_to_dict')
convert_none_to_empty_list = _lib('convert_none_to_empty_list')
convert_none_to_empty_dict = _lib('convert_none_to_empty_dict')
convert_to_list = _lib('convert_to_list')


_deprecate._DeprecateSubset.and_also('MAC_PATTERN', lib_validators)

_deprecate._DeprecateSubset.and_also('validators', lib_validators)


# Define constants for base resource name
NETWORK = 'network'
NETWORKS = '%ss' % NETWORK
PORT = 'port'
PORTS = '%ss' % PORT
SUBNET = 'subnet'
SUBNETS = '%ss' % SUBNET
SUBNETPOOL = 'subnetpool'
SUBNETPOOLS = '%ss' % SUBNETPOOL
# Note: a default of ATTR_NOT_SPECIFIED indicates that an
# attribute is not required, but will be generated by the plugin
# if it is not specified.  Particularly, a value of ATTR_NOT_SPECIFIED
# is different from an attribute that has been specified with a value of
# None.  For example, if 'gateway_ip' is omitted in a request to
# create a subnet, the plugin will receive ATTR_NOT_SPECIFIED
# and the default gateway_ip will be generated.
# However, if gateway_ip is specified as None, this means that
# the subnet does not have a gateway IP.
# The following is a short reference for understanding attribute info:
# default: default value of the attribute (if missing, the attribute
# becomes mandatory.
# allow_post: the attribute can be used on POST requests.
# allow_put: the attribute can be used on PUT requests.
# validate: specifies rules for validating data in the attribute.
# convert_to: transformation to apply to the value before it is returned
# is_visible: the attribute is returned in GET responses.
# required_by_policy: the attribute is required by the policy engine and
# should therefore be filled by the API layer even if not present in
# request body.
# enforce_policy: the attribute is actively part of the policy enforcing
# mechanism, ie: there might be rules which refer to this attribute.

RESOURCE_ATTRIBUTE_MAP = {
    NETWORKS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': NAME_MAX_LEN},
                 'default': '', 'is_visible': True},
        'subnets': {'allow_post': False, 'allow_put': False,
                    'default': [],
                    'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': lib_converters.convert_to_boolean,
                           'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        SHARED: {'allow_post': True,
                 'allow_put': True,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': True,
                 'required_by_policy': True,
                 'enforce_policy': True},
    },
    PORTS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {'type:string': NAME_MAX_LEN},
                 'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': lib_converters.convert_to_boolean,
                           'is_visible': True},
        'mac_address': {'allow_post': True, 'allow_put': True,
                        'default': constants.ATTR_NOT_SPECIFIED,
                        'validate': {'type:mac_address': None},
                        'enforce_policy': True,
                        'is_visible': True},
        'fixed_ips': {'allow_post': True, 'allow_put': True,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'convert_list_to':
                          lib_converters.convert_kvp_list_to_dict,
                      'validate': {'type:fixed_ips': None},
                      'enforce_policy': True,
                      'is_visible': True},
        'device_id': {'allow_post': True, 'allow_put': True,
                      'validate': {'type:string': DEVICE_ID_MAX_LEN},
                      'default': '',
                      'is_visible': True},
        'device_owner': {'allow_post': True, 'allow_put': True,
                         'validate': {'type:string': DEVICE_OWNER_MAX_LEN},
                         'default': '', 'enforce_policy': True,
                         'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
    },
    SUBNETS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {'type:string': NAME_MAX_LEN},
                 'is_visible': True},
        'ip_version': {'allow_post': True, 'allow_put': False,
                       'convert_to': lib_converters.convert_to_int,
                       'validate': {'type:values': [4, 6]},
                       'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
        'subnetpool_id': {'allow_post': True,
                          'allow_put': False,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'required_by_policy': False,
                          'validate': {'type:subnetpool_id_or_none': None},
                          'is_visible': True},
        'prefixlen': {'allow_post': True,
                      'allow_put': False,
                      'validate': {'type:non_negative': None},
                      'convert_to': lib_converters.convert_to_int,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'required_by_policy': False,
                      'is_visible': False},
        'cidr': {'allow_post': True,
                 'allow_put': False,
                 'default': constants.ATTR_NOT_SPECIFIED,
                 'validate': {'type:subnet_or_none': None},
                 'required_by_policy': False,
                 'is_visible': True},
        'gateway_ip': {'allow_post': True, 'allow_put': True,
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'validate': {'type:ip_address_or_none': None},
                       'is_visible': True},
        'allocation_pools': {'allow_post': True, 'allow_put': True,
                             'default': constants.ATTR_NOT_SPECIFIED,
                             'validate': {'type:ip_pools': None},
                             'is_visible': True},
        'dns_nameservers': {'allow_post': True, 'allow_put': True,
                            'convert_to':
                                lib_converters.convert_none_to_empty_list,
                            'default': constants.ATTR_NOT_SPECIFIED,
                            'validate': {'type:nameservers': None},
                            'is_visible': True},
        'host_routes': {'allow_post': True, 'allow_put': True,
                        'convert_to':
                            lib_converters.convert_none_to_empty_list,
                        'default': constants.ATTR_NOT_SPECIFIED,
                        'validate': {'type:hostroutes': None},
                        'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'enable_dhcp': {'allow_post': True, 'allow_put': True,
                        'default': True,
                        'convert_to': lib_converters.convert_to_boolean,
                        'is_visible': True},
        'ipv6_ra_mode': {'allow_post': True, 'allow_put': False,
                         'default': constants.ATTR_NOT_SPECIFIED,
                         'validate': {'type:values': n_const.IPV6_MODES},
                         'is_visible': True},
        'ipv6_address_mode': {'allow_post': True, 'allow_put': False,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'validate': {'type:values':
                                           n_const.IPV6_MODES},
                              'is_visible': True},
        SHARED: {'allow_post': False,
                 'allow_put': False,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': False,
                 'required_by_policy': True,
                 'enforce_policy': True},
    },
    SUBNETPOOLS: {
        'id': {'allow_post': False,
               'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True,
                 'allow_put': True,
                 'validate': {'type:not_empty_string': None},
                 'is_visible': True},
        'tenant_id': {'allow_post': True,
                      'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'prefixes': {'allow_post': True,
                     'allow_put': True,
                     'validate': {'type:subnet_list': None},
                     'is_visible': True},
        'default_quota': {'allow_post': True,
                          'allow_put': True,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'is_visible': True},
        'ip_version': {'allow_post': False,
                       'allow_put': False,
                       'is_visible': True},
        'default_prefixlen': {'allow_post': True,
                              'allow_put': True,
                              'validate': {'type:non_negative': None},
                              'convert_to': lib_converters.convert_to_int,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'is_visible': True},
        'min_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'is_visible': True},
        'max_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'is_visible': True},
        'is_default': {'allow_post': True,
                       'allow_put': True,
                       'default': False,
                       'convert_to': lib_converters.convert_to_boolean,
                       'is_visible': True,
                       'required_by_policy': True,
                       'enforce_policy': True},
        SHARED: {'allow_post': True,
                 'allow_put': False,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': True,
                 'required_by_policy': True,
                 'enforce_policy': True},
    }
}

# Identify the attribute used by a resource to reference another resource

RESOURCE_FOREIGN_KEYS = {
    NETWORKS: 'network_id'
}

# Store plural/singular mappings
PLURALS = {NETWORKS: NETWORK,
           PORTS: PORT,
           SUBNETS: SUBNET,
           SUBNETPOOLS: SUBNETPOOL,
           'dns_nameservers': 'dns_nameserver',
           'host_routes': 'host_route',
           'allocation_pools': 'allocation_pool',
           'fixed_ips': 'fixed_ip',
           'extensions': 'extension'}
# Store singular/plural mappings. This dictionary is populated by
# get_resource_info
REVERSED_PLURALS = {}


def get_collection_info(collection):
    """Helper function to retrieve attribute info.

    :param collection: Collection or plural name of the resource
    """
    return RESOURCE_ATTRIBUTE_MAP.get(collection)


def get_resource_info(resource):
    """Helper function to retrive attribute info

    :param resource: resource name
    """
    plural_name = REVERSED_PLURALS.get(resource)
    if not plural_name:
        for (plural, singular) in PLURALS.items():
            if singular == resource:
                plural_name = plural
                REVERSED_PLURALS[resource] = plural_name
    return RESOURCE_ATTRIBUTE_MAP.get(plural_name)


def fill_default_value(attr_info, res_dict,
                       exc_cls=ValueError,
                       check_allow_post=True):
    for attr, attr_vals in six.iteritems(attr_info):
        if attr_vals['allow_post']:
            if 'default' not in attr_vals and attr not in res_dict:
                msg = _("Failed to parse request. Required "
                        "attribute '%s' not specified") % attr
                raise exc_cls(msg)
            res_dict[attr] = res_dict.get(attr,
                                          attr_vals.get('default'))
        elif check_allow_post:
            if attr in res_dict:
                msg = _("Attribute '%s' not allowed in POST") % attr
                raise exc_cls(msg)


def convert_value(attr_info, res_dict, exc_cls=ValueError):
    for attr, attr_vals in six.iteritems(attr_info):
        if (attr not in res_dict or
                res_dict[attr] is constants.ATTR_NOT_SPECIFIED):
            continue
        # Convert values if necessary
        if 'convert_to' in attr_vals:
            res_dict[attr] = attr_vals['convert_to'](res_dict[attr])
        # Check that configured values are correct
        if 'validate' not in attr_vals:
            continue
        for rule in attr_vals['validate']:
            res = lib_validators.validators[rule](res_dict[attr],
                                                  attr_vals['validate'][rule])
            if res:
                msg_dict = dict(attr=attr, reason=res)
                msg = _("Invalid input for %(attr)s. "
                        "Reason: %(reason)s.") % msg_dict
                raise exc_cls(msg)


def populate_tenant_id(context, res_dict, attr_info, is_create):
    if (('tenant_id' in res_dict and
         res_dict['tenant_id'] != context.tenant_id and
         not context.is_admin)):
        msg = _("Specifying 'tenant_id' other than authenticated "
                "tenant in request requires admin privileges")
        raise webob.exc.HTTPBadRequest(msg)

    if is_create and 'tenant_id' not in res_dict:
        if context.tenant_id:
            res_dict['tenant_id'] = context.tenant_id
        elif 'tenant_id' in attr_info:
            msg = _("Running without keystone AuthN requires "
                    "that tenant_id is specified")
            raise webob.exc.HTTPBadRequest(msg)


def verify_attributes(res_dict, attr_info):
    extra_keys = set(res_dict.keys()) - set(attr_info.keys())
    if extra_keys:
        msg = _("Unrecognized attribute(s) '%s'") % ', '.join(extra_keys)
        raise webob.exc.HTTPBadRequest(msg)


# Shim added to move the following to neutron_lib.constants:
# ATTR_NOT_SPECIFIED
# HEX_ELEM
# UUID_PATTERN

# Neutron-lib migration shim. This will wrap any constants that are moved
# to that library in a deprecation warning, until they can be updated to
# import directly from their new location.
# If you're wondering why we bother saving _OLD_REF, it is because if we
# do not, then the original module we are overwriting gets garbage collected,
# and then you will find some super strange behavior with inherited classes
# and the like. Saving a ref keeps it around.

# WARNING: THESE MUST BE THE LAST TWO LINES IN THIS MODULE
_OLD_REF = sys.modules[__name__]
sys.modules[__name__] = _deprecate._DeprecateSubset(globals(), constants)
# WARNING: THESE MUST BE THE LAST TWO LINES IN THIS MODULE
