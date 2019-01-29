# Copyright (C) 2019 NTT DATA
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import sys

from openstack.cloud.openstackcloud import _OpenStackCloudMixin
import openstack.config
from openstack import connection

from masakari.tests import base


#: Defines the OpenStack Client Config (OCC) cloud key in your OCC config
#: file, typically in /etc/openstack/clouds.yaml. That configuration
#: will determine where the functional tests will be run and what resource
#: defaults will be used to run the functional tests.
TEST_CLOUD_NAME = os.getenv('OS_CLOUD', 'devstack-admin')
TEST_CLOUD_REGION = openstack.config.get_cloud_region(cloud=TEST_CLOUD_NAME)


class BaseFunctionalTest(base.TestCase):

    def setUp(self):
        super(BaseFunctionalTest, self).setUp()
        _log_stream = sys.stdout

        handler = logging.StreamHandler(_log_stream)
        formatter = logging.Formatter('%(asctime)s %(name)-32s %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger('openstack')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        # Enable HTTP level tracing
        logger = logging.getLogger('keystoneauth')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False

        self.conn = connection.Connection(config=TEST_CLOUD_REGION)

        self.hypervisors = self._hypervisors()

    def _hypervisors(self):
        hypervisors = _OpenStackCloudMixin.list_hypervisors(
            connection.from_config(cloud_name=TEST_CLOUD_NAME))
        return hypervisors
