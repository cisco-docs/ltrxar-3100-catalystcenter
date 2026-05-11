# Project

*Location in GUI*:
`Design` » `CLI Templates`

{{ doc_gen }}

Projects are containers that organize CLI [Templates](/docs/data_models/catalyst_center/templates/template) into logical groups. Each project holds one or more templates that can be of type onboarding (Day-0) or Day-N, and templates within a project can be assigned to [Switching Network Profiles](/docs/data_models/catalyst_center/network_profiles/switching_network_profiles) for device provisioning. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic project configuration with simple Day-N templates for ongoing network device management and configuration updates:

```yaml
catalyst_center:
  templates:
    projects:
      - name: BASIC_NETWORK_PROJECT
        description: Basic network configuration templates
        dayn_templates:
          - name: basic_vlan_config
            description: Basic VLAN configuration template
            language: JINJA
          - name: basic_interface_config
            description: Basic interface configuration template
            language: VELOCITY
```

Example-2: Comprehensive enterprise project with both on-boarding and Day-N templates, including device-specific configurations, variables, tags, and advanced template management for complete network life-cycle automation:

```yaml
catalyst_center:
  templates:
    projects:
      - name: ENTERPRISE_SWITCHING_PROJECT
        description: Enterprise switching templates for campus deployment
        onboarding_templates:
          - name: catalyst_9300_onboarding
            version: "2.1"
            description: Catalyst 9300 series onboarding template
            language: JINJA
            device_types:
              - product_family: Switches and Hubs
                product_series: Catalyst 9300 Series Switches
                product_type: Catalyst 9300-24U
            software_type: IOS-XE
            software_version: "17.09.04a"
            variables:
              - name: HOSTNAME
                field_name: hostname
                required: true
                data_type: STRING
                hint_text: "Enter device hostname"
                additional_info: "Must follow corporate naming convention"
              - name: MGMT_IP
                field_name: management_ip
                required: true
                data_type: IPADDRESS
                hint_text: "Management IP address"
              - name: VLAN_ID
                field_name: vlan_id
                required: false
                data_type: INTEGER
                hint_text: "Management VLAN ID"
            tags:
              - campus
              - switching
              - onboarding
            composite: false
            redeploy_template: ON_CHANGE
          - name: catalyst_9500_onboarding
            version: "1.5"
            description: Catalyst 9500 series core switch onboarding
            language: JINJA
            device_types:
              - product_family: Switches and Hubs
                product_series: Catalyst 9500 Series Switches
                product_type: Catalyst 9500-40X
            software_type: IOS-XE
            software_version: "17.09.04a"
            variables:
              - name: HOSTNAME
                required: true
                data_type: STRING
              - name: MGMT_IP
                required: true
                data_type: IPADDRESS
              - name: HSRP_PRIORITY
                required: false
                data_type: INTEGER
                hint_text: "HSRP priority value"
            tags:
              - core
              - switching
              - onboarding
            redeploy_template: ALWAYS
        dayn_templates:
          - name: vlan_management
            version: "3.2"
            description: VLAN creation and management template
            language: JINJA
            variables:
              - name: VLAN_LIST
                required: true
                data_type: STRING
                hint_text: "Comma-separated VLAN IDs"
              - name: VLAN_NAMES
                required: false
                data_type: STRING
                hint_text: "Comma-separated VLAN names"
            tags:
              - vlan
              - layer2
            redeploy_template: ON_CHANGE
          - name: qos_policy_application
            version: "2.0"
            description: QoS policy application template
            language: VELOCITY
            variables:
              - name: POLICY_NAME
                required: true
                data_type: STRING
              - name: INTERFACE_LIST
                required: true
                data_type: STRING
                hint_text: "Interfaces to apply policy"
            tags:
              - qos
              - policy
            management_device_ips:
              - "192.168.1.10"
              - "192.168.1.11"
            redeploy_template: NEVER
          - name: security_acl_composite
            version: "1.0"
            description: Composite security ACL template
            language: JINJA
            composite: true
            containing_templates:
              - standard_acl_template
              - extended_acl_template
            variables:
              - name: ACL_NAME
                required: true
                data_type: STRING
              - name: PERMIT_NETWORKS
                required: true
                data_type: STRING
                hint_text: "Networks to permit"
            tags:
              - security
              - acl
              - composite
            redeploy_template: ON_CHANGE
      - name: WIRELESS_CONTROLLER_PROJECT
        description: Wireless controller configuration templates
        onboarding_templates:
          - name: c9800_wlc_onboarding
            description: Catalyst 9800 WLC onboarding template
            language: JINJA
            device_types:
              - product_family: Wireless Controller
                product_series: Catalyst 9800 Series Wireless Controllers
                product_type: C9800-CL
            software_type: IOS-XE
            software_version: "17.09.04a"
            variables:
              - name: WLC_HOSTNAME
                required: true
                data_type: STRING
              - name: MGMT_IP
                required: true
                data_type: IPADDRESS
              - name: COUNTRY_CODE
                required: true
                data_type: STRING
                hint_text: "Two-letter country code"
            tags:
              - wireless
              - controller
              - onboarding
        dayn_templates:
          - name: ssid_configuration
            description: SSID configuration and management
            language: JINJA
            variables:
              - name: SSID_NAME
                required: true
                data_type: STRING
              - name: VLAN_ID
                required: true
                data_type: INTEGER
              - name: SECURITY_TYPE
                required: true
                data_type: STRING
                hint_text: "WPA2, WPA3, or OPEN"
            tags:
              - wireless
              - ssid
```
