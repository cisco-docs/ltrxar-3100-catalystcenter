# Tag

*Location in GUI*:
`Design` » `CLI Templates`

{{ doc_gen }}

Tags provide a way to categorize and organize [Templates](/docs/data_models/catalyst_center/templates/template) and devices in Catalyst Center. Tags can be assigned to templates for filtering and grouping, and to devices for targeted template deployment. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic tag creation with name and description for organizing and categorizing templates and devices in Catalyst Center:

```yaml
catalyst_center:
  templates:
    tags:
      - name: DayN_Tag
        description: DayN_Tag
```

Example-2: Template tag assignment demonstrating how to apply tags to Day-N templates for organizational purposes, enabling filtering and management of access list templates targeting Catalyst 9300 series switches:

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
            tags:
              - DayN_Tag
```

Example-3: Device tag assignment showing how to apply multiple tags to network devices for inventory management, enabling grouping and filtering of edge nodes in fabric deployments:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: EDGE02
        fqdn_name: EDGE02.cisco.eu
        device_ip: 198.18.130.2
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        fabric_site: Global/Poland/Krakow
        fabric_roles:
          - EDGE_NODE
        tags:
          - TAG1
          - TAG2
```
