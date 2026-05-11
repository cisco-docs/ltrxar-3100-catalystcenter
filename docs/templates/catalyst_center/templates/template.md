# Template

*Location in GUI*:
`Design` » `CLI Templates`

{{ doc_gen }}

Templates define CLI configuration snippets using Jinja or Velocity templating languages that are pushed to network devices during provisioning. Templates belong to a [Project](/docs/data_models/catalyst_center/templates/project) and can target specific device families and software versions. They support parameterized variables, conditional logic, and can be tagged with [Tags](/docs/data_models/catalyst_center/templates/tag) for organization. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Day-N template configuration for ongoing network management using JINJA templating language to create access list templates targeting Catalyst 9300 series switches:

```yaml
catalyst_center:
  templates:
    projects:
      - name: Project_DayN
        description: Project_DayN
        dayn_templates:
          - name: access_list_template
            description: Access List Template
            language: JINJA
            composite: false
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9300 Series Switches"
            software_type: IOS-XE
```

The content of the template must be stored in the templates/ directory inside a JINJA file, with the file name matching the template name:

`access_list_template.j2`
```sh
## Access List
ip access-list standard 20
10 permit 10.0.0.0 0.0.0.255
20 permit 20.0.0.0 0.0.0.255
```

Example-2: On-boarding template configuration for initial device provisioning using JINJA templating to automate Day-0 configuration deployment on Catalyst 9300 series switches:

```yaml
catalyst_center:
  templates:
    projects:
      - name: Project_Onboarding
        description: Project_Onboarding
        onboarding_templates:
          - name: onboarding_template
            description: Onboarding Template
            language: JINJA
            composite: false
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9300 Series Switches"
            software_type: IOS-XE
```

Example-3: Composite template configuration combining multiple individual templates into a single deployable unit for complex ACL configurations targeting Catalyst 9300 series switches:

```yaml
catalyst_center:
  templates:
    projects:
      - name: Project_DayN
        description: Project_DayN
        dayn_templates:
          - name: ACL_COMPOSITE
            description: ACL COMPOSITE
            language: JINJA
            composite: true
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9300 Series Switches"
            software_type: IOS-XE
            containing_templates:
              - ACL_41
              - ACL_42
```

Templates content:

ACL_41
```
ip access-list standard 41
10 permit {{acl_ip_address}} 0.0.0.255
```

ACL_42
```
ip access-list standard 42
10 permit {{acl_ip_address}} 0.0.0.255
```

Example-4: Network profile template assignment demonstrating how to associate Day-N templates with switching network profiles for automated deployment across multiple sites:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: SDA SWITCH PROFILE
        dayn_templates:
            - ACL_COMPOSITE
        sites:
          - Global/United States/Golden Hills Campus/Sunset Tower
          - Global/United States/Lakefront Tower/Windy City Plaza
          - Global/United States/Oceanfront Mansion/Art Deco Mansion
          - Global/United States/Desert Oasis Branch/Desert Oasis Tower
```

Example-5: Device-specific template deployment showing how to deploy composite Day-N templates directly to individual devices with template-specific variable assignments:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.com
        device_ip: 192.168.30.64
        serial_number: FOC2644021A
        pid: C9300-24P
        state: PROVISION
        dayn_templates:
          composite:
            - name: ACL_COMPOSITE
              variables:
                - name: acl_ip_address
                  value: 21.21.21.0
                  template_name: ACL_41
                - name: acl_ip_address
                  value: 22.22.22.0
                  template_name: ACL_42
```

Example-6: Template redeployment strategies demonstrating different approaches to template life-cycle management on network devices:

6a. Always redeploy template configuration regardless of content changes:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.com
        device_ip: 192.168.30.64
        serial_number: FOC2644021A
        pid: C9300-24P
        state: PROVISION
        dayn_templates:
          composite:
            - name: ACL_COMPOSITE
              redeploy_template: ALWAYS
              variables:
                - name: acl_ip_address
                  value: 21.21.21.0
                  template_name: ACL_41
                - name: acl_ip_address
                  value: 22.22.22.0
                  template_name: ACL_42
```

6b. Conditional template redeployment only when template content changes:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.com
        device_ip: 192.168.30.64
        serial_number: FOC2644021A
        pid: C9300-24P
        state: PROVISION
        dayn_templates:
          composite:
            - name: ACL_COMPOSITE
              redeploy_template: ON_CHANGE
              variables:
                - name: acl_ip_address
                  value: 21.21.21.0
                  template_name: ACL_41
                - name: acl_ip_address
                  value: 22.22.22.0
                  template_name: ACL_42
```

The `redeploy_template` flag can be applied both at the template level and at the device level:

When defined under a template, it controls how that specific template is redeployed across all devices that use it.

When defined under a device, it controls redeployment of all templates assigned to that device.

This lets you choose whether to consistently redeploy a single template to many devices, or redeploy every template on a specific device.

Example-7: Template-level redeployment when content of template changes, affecting all devices that use this template:

```yaml
catalyst_center:
  templates:
    projects:
      - name: Project_DayN
        description: Project_DayN
        dayn_templates:
          - name: ACL_COMPOSITE
            description: ACL COMPOSITE
            language: JINJA
            redeploy_template: ON_CHANGE
            composite: true
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9300 Series Switches"
            software_type: IOS-XE
            containing_templates:
              - ACL_41
              - ACL_42
```

Example-8: Device-level redeployment when content of template changes, including both composite and regular templates:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.com
        device_ip: 192.168.30.64
        serial_number: FOC2644021A
        pid: C9300-24P
        state: PROVISION
        dayn_templates:
          redeploy_template: ON_CHANGE
          composite:
            - name: ACL_COMPOSITE
              variables:
                - name: acl_ip_address
                  value: 21.21.21.0
                  template_name: ACL_41
                - name: acl_ip_address
                  value: 22.22.22.0
                  template_name: ACL_42
          regular:
            - name: ACL_BLOCK
              variables:
                - name: interface
                  value: GigabtEthernet1/0/1
```

Example-9: Handling duplicate template names across template projects using the `project#name` delimiter format.

When the same template name exists under multiple template projects (e.g. `bfd_interval` in both `PROJECT1` and `PROJECT2`), use the `#` delimiter to specify which project's template to reference. The format is `ProjectName#TemplateName`.

9a. Template definition — two projects each containing a template with the same name (`bfd_interval`):

```yaml
catalyst_center:
  templates:
    projects:
      - name: PROJECT1
        dayn_templates:
          - name: bfd_interval
            description: add bfd interfval of 250 min_rx to Enterprise p2p ISIS interfaces
            language: JINJA
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9000 Series Virtual Switches"
            software_type: IOS-XE

      - name: PROJECT2
        dayn_templates:
          - name: bfd_interval
            description: add bfd interfval of 350 min_rx to Service Provider p2p ISIS interfaces
            language: JINJA
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9000 Series Virtual Switches"
            software_type: IOS-XE
```
> **Note:** The template's Jinja or Velocity file name must also be prefixed with the project name to avoid conflicts. For example, `PROJECT1#bfd_interval.j2` and `PROJECT2#bfd_interval.j2`.


9b. Network profile :  referencing a template that has a duplicate name across projects. Use `ProjectName#TemplateName` to specify the exact template:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: SDA SWITCH PROFILE
        dayn_templates:
          - PROJECT1#bfd_interval
        sites:
          - Global/Poland/Krakow
```

When the template name is unique across all projects, the project prefix is not required:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: SDA SWITCH PROFILE
        dayn_templates:
          - ACL_Block
        sites:
          - Global/Poland/Krakow
```

9c. Device provisioning: deploying templates with duplicate names to specific devices. Use `ProjectName#TemplateName` in the `name` field:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: FIAB
        fqdn_name: FIAB.cisco.eu
        device_ip: 181.1.1.1
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        dayn_templates:
          composite:
            - name: PROJECT2#bfd_interval
              redeploy_template: ALWAYS

      - name: LAN-EN2
        fqdn_name: LAN-EN2.cisco.eu
        device_ip: 181.1.1.43
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        dayn_templates:
          composite:
            - name: PROJECT2#bfd_interval
              redeploy_template: ALWAYS
```

When the template name is unique across all projects, the project prefix is not required:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.eu
        device_ip: 198.18.130.1
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        dayn_templates:
          regular:
            - name: ACL_43
              variables:
                - name: acl_ip_address
                  value: 23.23.23.0
```

Example-10: Backward compatibility:  mixing existing (bare name) and new (`ProjectName#TemplateName`) formats across templates, network profiles, and device provisioning.

The `project#name` delimiter is only required when the same template name exists under multiple projects. All existing YAML without the prefix continues to work unchanged.

10a. Templates — `ACL_Block` is unique to `PROJECT1`, while `Day_N_remove_bfd` exists in both projects:

```yaml
catalyst_center:
  templates:
    projects:
      - name: PROJECT1
        dayn_templates:
          - name: ACL_Block
            description: ACL to block malicious IPs
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9000 Series Virtual Switches"
            software_type: IOS-XE
          - name: Day_N_remove_bfd
            description: Remove BFD from C9kv p2p ISIS interfaces
            language: JINJA
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9000 Series Virtual Switches"
            software_type: IOS-XE

      - name: PROJECT2
        dayn_templates:
          - name: Day_N_remove_bfd
            description: Remove BFD from C9kv p2p ISIS interfaces
            language: JINJA
            device_types:
              - product_family: "Switches and Hubs"
                product_series: "Cisco Catalyst 9000 Series Virtual Switches"
            software_type: IOS-XE
```

10b. Network profiles — `ACL_Block` is unique so bare name works (old format). `Day_N_remove_bfd` is duplicated so `project#name` is required (new format). Both formats coexist in the same list:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: SDA SWITCH PROFILE
        dayn_templates:
          - ACL_Block
          - PROJECT2#Day_N_remove_bfd
        sites:
          - Global/Poland/Krakow
```

10c. Device provisioning — a single device deployed with both a duplicate-name template (`PROJECT2#Day_N_remove_bfd`, new format) and a unique template (`ACL_Block`, old format):

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.eu
        device_ip: 198.18.130.1
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        dayn_templates:
          regular:
            - name: PROJECT2#Day_N_remove_bfd
              redeploy_template: ALWAYS
            - name: ACL_Block
              variables:
                - name: management_interface
                  value: Loopback56
```

In summary — the `project#name` format is additive. Existing templates, network profiles, and device configurations that use unique template names require no changes.

> **Note:** Using `project#name` for a template that is unique across projects is also valid and will not break anything. For example, if `ACL_Block` only exists under `PROJECT1`, both `ACL_Block` and `PROJECT1#ACL_Block` resolve to the same template. The project prefix is only *required* for duplicate names, but it is *accepted* for all templates.