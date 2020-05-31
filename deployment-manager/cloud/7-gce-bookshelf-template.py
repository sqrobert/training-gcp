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
                                    context.properties['zone'], '/machineTypes/', context.properties['machineType']]),
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

    resources.append({
        "name" : ''.join([NAME, "-frontend-group"]),
        "type" : "compute.v1.insanceGroupManagers",
        "properties": {
            "instanceTemplate" : '$(ref.{}.selfLink)'.format(NAME),
            "baseInstanceGroup" : 'frontend-group',
            "targetSize" : 3,
            "zone" : context.properties['zone'],
            "namedPorts" : {
                "name" : "http",
                "port" : 8080
            }
        }
    })

    # Load Balancer Setup
    #

    # A complete HTTP load balancer is structured as follows:
    #
    # 1) A global forwarding rule directs incoming requests to a target HTTP proxy.
    # 2) The target HTTP proxy checks each request against a URL map to determine the
    #    appropriate backend service for the request.
    # 3) The backend service directs each request to an appropriate backend based on
    #    serving capacity, zone, and instance health of its attached backends. The
    #    health of each backend instance is verified using either a health check.
    #
    # We'll create these resources in reverse order:
    # service, health check, backend service, url map, proxy.

    # Create a health check
    # The load balancer will use this check to keep track of which instances to send traffic to.
    # Note that health checks will not cause the load balancer to shutdown any instances.
    resources.append({
        "name" : ''.join([NAME, "-health-check"]),
        "type" : "compute.v1.httpHealthCheck",
        "properties" : {
            "requestPath" : "/_ah/health",
            "port" : 8080
        }
    })

    resources.append({
        "name" : ''.join([NAME, "-health-check"]),
        "type" : "compute.v1.httpHealthCheck",
        "properties" : {
            "requestPath" : "/_ah/health",
            "port" : 8080
        }
    })

    resources.append({
        "name" : SERVICE,
        "type" : "compute.v1.backendService",
        "properties" : {
            "healthChecks" : '$(ref.{}-health-check.selfLink)'.format(NAME),
            "portName" : "http",
            "backend" : {
                "group" : "$(ref.{}-froentend-group.selfLink)".format(NAME),
                "zone" : context.properties['zone']
            }
        }
    })

    resources.append({
        "name" : "".join([SERVICE,"-map"]),
        "type" : "compute.v1.urlMap",
        "properties": {
            "defaultService" : "$(ref.{}.selfLink)".format(SERVICE,)
        }
    })

    resources.append({
        "name" : "".join([SERVICE,"-proxy"]),
        "type" : "compute.v1.targetHttpProxy",
        "properties": {
            "urlMap" : "$(ref.{}-map.selfLink)".format(SERVICE)
        }
    })

    resources.append({
        "name" : "".join([SERVICE,"-http-rule"]),
        "type" : "compute.v1.globalForwardingRule",
        "properties": {
            "target" : "$(ref.{}-proxy.selfLink)".format(SERVICE),
            "port" : 80
        }
    })

    # Creates an autoscaler resource (note that when using the gcloud CLI,
    # autoscaling is set as a configuration of the managed instance group
    # but autoscaler is a resource so in deployment manager we explicitly
    # define it
    resources.append({
        "name" : "".join([SERVICE,"-autoscaler"]),
        "type" : "compute.v1.autoscaler",
        "properties": {
            "zone": context.properties['zone'],
            "target" : "$(ref.{}-frontend-group).selfLink".format(NAME),
            "autoscalingPolicy" : {
                "minNumReplicas" : context.properties['min-instances'],
                "maxNumReplicas" : context.properties['max-instances'],
                "loadBalancingUtilization" : {
                    "utilizationTarget" : context.properties['target-utilization']
                }
            }
        }
    })


    resources.append({
        "name" : "".join([NAME,"-http-allow"]),
        "type" : "compute.v1.firewall",
        "properties": {
            "allowed" : {
                "IPProtocol" : "tcp",
                "ports" : [8080]
            },
            "sourceRanges" : ["0.0.0.0/0"],
            "targetTags" : "http-server",
            "description" : "Allow port 8080 access to http-server"
        }
    })

    # [END use_template_with_variables]
    return {'resources': resources}