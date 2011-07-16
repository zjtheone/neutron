# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Cisco Systems, Inc.  All rights reserved.
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
#
# @author: Ying Liu, Cisco Systems, Inc.
#

import logging
import webob.dec
from quantum.common import wsgi
from webob import exc

from quantum.api import api_common as common

from cisco_extensions import pprofiles as pprofiles_view
from cisco_extensions import exceptions as exception
from cisco_extensions import faults as faults

LOG = logging.getLogger('quantum.api.portprofiles')


class Controller(common.QuantumController):
    """ portprofile API controller
        based on QuantumController """

    _portprofile_ops_param_list = [{
        'param-name': 'portprofile-name',
        'required': True}, {
        'param-name': 'vlan-id',
        'required': True}, {
        'param-name': 'assignment',
        'required': False}]
    
    _assignprofile_ops_param_list = [{
        'param-name': 'network-id',
        'required': True}, {
        'param-name': 'port-id',
        'required': True}]
    
    _serialization_metadata = {
        "application/xml": {
            "attributes": {
                "portprofile": ["id", "name"],
            },
        },
    }

    def __init__(self, plugin):
        self._resource_name = 'portprofile'
        super(Controller, self).__init__(plugin)
             
    def index(self, request, tenant_id):
        """ Returns a list of portprofile ids """
        #TODO: this should be for a given tenant!!!
        return self._items(request, tenant_id, is_detail=False)

    def _items(self, request, tenant_id, is_detail):
        """ Returns a list of portprofiles. """
        portprofiles = self._plugin.get_all_portprofiles(tenant_id)
        builder = pprofiles_view.get_view_builder(request)
        result = [builder.build(portprofile, is_detail)['portprofile']
                  for portprofile in portprofiles]
        return dict(portprofiles=result)

    def show(self, request, tenant_id, id):
        """ Returns portprofile details for the given portprofile id """
        try:
            portprofile = self._plugin.get_portprofile_details(
                            tenant_id, id)
            builder = pprofiles_view.get_view_builder(request)
            #build response with details
            result = builder.build(portprofile, True)
            return dict(portprofiles=result)
        except exception.PortprofileNotFound as e:
            return faults.Fault(faults.PortprofileNotFound(e))
            #return faults.Fault(e)

    def create(self, request, tenant_id):
        """ Creates a new portprofile for a given tenant """
        #look for portprofile name in request
        try:
            req_params = \
                self._parse_request_params(request, 
                                           self._portprofile_ops_param_list)
        except exc.HTTPError as e:
            return faults.Fault(e)
        portprofile = self._plugin.\
                       create_portprofile(tenant_id,
                                          req_params['portprofile-name'],
                                          req_params['vlan-id'])
        builder = pprofiles_view.get_view_builder(request)
        result = builder.build(portprofile)
        return dict(portprofiles=result)

    def update(self, request, tenant_id, id):
        """ Updates the name for the portprofile with the given id """
        try:
            req_params = \
                self._parse_request_params(request, 
                                           self._portprofile_ops_param_list)
        except exc.HTTPError as e:
            return faults.Fault(e)
        try:
            portprofile = self._plugin.\
            rename_portprofile(tenant_id,
                        id, req_params['portprofile-name'])

            builder = pprofiles_view.get_view_builder(request)
            result = builder.build(portprofile, True)
            return dict(portprofiles=result)
        except exception.PortprofileNotFound as e:
            return faults.Fault(faults.PortprofileNotFound(e))

    def delete(self, request, tenant_id, id):
        """ Destroys the portprofile with the given id """
        try:
            self._plugin.delete_portprofile(tenant_id, id)
            return exc.HTTPAccepted()
        except exception.PortprofileNotFound as e:
            return faults.Fault(faults.PortprofileNotFound(e))
         
    #added for cisco's extension
    def associate_portprofile(self, request, tenant_id, portprofile_id):
        content_type = request.best_match_content_type()
        print "Content type:%s" % content_type
        
        try:
            req_params = \
                self._parse_request_params(request,
                                           self._assignprofile_ops_param_list)
        except exc.HTTPError as e:
            return faults.Fault(e)
        net_id = req_params['network-id'].strip()
        #print "*****net id "+net_id
        port_id = req_params['port-id'].strip()
        try:
            self._plugin.associate_portprofile(tenant_id,
                                                net_id, port_id,
                                                portprofile_id)
            return exc.HTTPAccepted()
        except exception.PortprofileNotFound as e:
            return faults.Fault(faults.PortprofileNotFound(e))
        except exception.PortNotFound as e:
            return faults.Fault(faults.PortNotFound(e))
        
     #added for Cisco extension
    def disassociate_portprofile(self, request, tenant_id, portprofile_id):
        content_type = request.best_match_content_type()
        print "Content type:%s" % content_type
        
        try:
            req_params = \
                self._parse_request_params(request,
                                           self._assignprofile_ops_param_list)
        except exc.HTTPError as e:
            return faults.Fault(e)
        net_id = req_params['network-id'].strip()
        #print "*****net id "+net_id
        port_id = req_params['port-id'].strip()
        try:
            self._plugin. \
            disassociate_portprofile(tenant_id,
                                    net_id, port_id, portprofile_id)
            return exc.HTTPAccepted()
        except exception.PortprofileNotFound as e:
            return faults.Fault(faults.PortprofileNotFound(e))
        except exception.PortNotFound as e:
            return faults.Fault(faults.PortNotFound(e))
