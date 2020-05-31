# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates a Compute Engine Instance."""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Generate configuration."""

    NAME = "bookshelf-" + context.env['deployment']
    SERVICE = "bookshelf-" + context.env['deployment'] + "-frontend"
    resources = []

    # [END use_basic_template]
    # [START use_template_with_variables]
    resources.append({
        'name': NAME,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join([COMPUTE_URL_BASE, 'projects/',
                                    context.env['project'], '/zones/',
                                    context.properties['zone'], '/machineTypes/f1-micro']),
            'tags': {
                'items': ['http-server']
            },
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'diskSizeGb': 10,
                'initializeParams': {
                    'sourceImage':
                        'projects/debian-cloud/global/images/family/debian-9'
                }
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': 'startup-script.sh'
                }]
            },
            'serviceAccounts':[{
                'email': 'default',
                'scopes': context.properties['scopes']

            }],
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }]
        }

    })
# [END use_template_with_variables]
  return {'resources': resources}