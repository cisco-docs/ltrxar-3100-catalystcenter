# Layer 3 Virtual Network

*Location in GUI*:
`Provision` » `SD-Access` » `Virtual Networks` » `Layer 3 Virtual Networks`

{{ doc_gen }}

Layer 3 Virtual Networks provide isolated routing domains within the SD-Access fabric for network segmentation. They are created globally and assigned to [Fabric Sites](/docs/data_models/catalyst_center/fabric/fabric_site), where they host [Anycast Gateways](/docs/data_models/catalyst_center/fabric/anycast_gateway) for endpoint connectivity. L3 VNs are handed off to external networks via [Layer 3 Handoffs](/docs/data_models/catalyst_center/fabric/layer_3_handoff) on [Border Devices](/docs/data_models/catalyst_center/fabric/border_device). This resource is **SDA fabric only**.

### Examples

Example-1: Basic Layer 3 Virtual Network Creation and Assignment

This example demonstrates how to create Layer 3 virtual networks at the global level and assign them to specific fabric sites. Layer 3 virtual networks enable network segmentation and micro-segmentation within SD-Access fabric, providing isolated routing domains for different user groups, applications, or security zones.

The Layer 3 virtual network configuration includes:
* Global L3 VN creation (SDA_VN_USERS, SDA_VN_PRINTERS, SDA_VN_CORPORATE) for reusable network segments
* Virtual network names that reflect organizational structure and traffic types
* Site-specific assignment enabling selective deployment across fabric sites
* Flexible assignment allowing different combinations per site based on requirements

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: SDA_VN_USERS
      - name: SDA_VN_PRINTERS
      - name: SDA_VN_CORPORATE
```

Next, you need to assign the L3 VN to a Fabric Site:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: No Authentication
        l3_virtual_networks:
          - SDA_VN_USERS
          - SDA_VN_PRINTERS
          - SDA_VN_CORPORATE

      - name: Global/United States
        authentication_template:
          name: No Authentication
        l3_virtual_networks:
          - SDA_VN_CORPORATE
          - SDA_VN_PRINTERS
```

Example-2: Department-Based Layer 3 Virtual Networks

This example shows how to create Layer 3 virtual networks organized by department or functional area for enterprise environments requiring departmental isolation and security policies.

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: FINANCE_VN
      - name: HR_VN
      - name: ENGINEERING_VN
      - name: MARKETING_VN
      - name: GUEST_VN
```

Site assignment with department-specific virtual networks:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North_America/Corporate HQ
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - FINANCE_VN
          - HR_VN
          - ENGINEERING_VN
          - MARKETING_VN
          - GUEST_VN

      - name: Global/Europe/Branch Office
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - ENGINEERING_VN
          - GUEST_VN
```

Example-3: Service-Based Layer 3 Virtual Networks

This example demonstrates how to create Layer 3 virtual networks based on network services and application types for service-oriented network architectures.

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: WEB_SERVICES_VN
      - name: DATABASE_SERVICES_VN
      - name: APPLICATION_SERVICES_VN
      - name: MANAGEMENT_SERVICES_VN
      - name: BACKUP_SERVICES_VN
```

Service-oriented site assignment:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Data Center/Primary
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - WEB_SERVICES_VN
          - DATABASE_SERVICES_VN
          - APPLICATION_SERVICES_VN
          - MANAGEMENT_SERVICES_VN
          - BACKUP_SERVICES_VN

      - name: Global/Data Center/DR Site
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - DATABASE_SERVICES_VN
          - BACKUP_SERVICES_VN
```

Example-4: Security Zone Layer 3 Virtual Networks

This example shows how to create Layer 3 virtual networks based on security zones and trust levels for environments requiring strict security segmentation and compliance.

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: SECURE_ZONE_VN
      - name: DMZ_ZONE_VN
      - name: INTERNAL_ZONE_VN
      - name: PUBLIC_ZONE_VN
      - name: QUARANTINE_ZONE_VN
```

Security zone site assignment:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Security/High_Security_Facility
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - SECURE_ZONE_VN
          - INTERNAL_ZONE_VN
          - QUARANTINE_ZONE_VN

      - name: Global/Security/Public_Access_Area
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - DMZ_ZONE_VN
          - PUBLIC_ZONE_VN
          - QUARANTINE_ZONE_VN
```

Example-5: Multi-Tenant Layer 3 Virtual Networks

This example demonstrates how to create Layer 3 virtual networks for multi-tenant environments with customer isolation and service provider deployments.

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: TENANT_A_PROD_VN
      - name: TENANT_A_DEV_VN
      - name: TENANT_B_PROD_VN
      - name: TENANT_B_DEV_VN
      - name: SHARED_SERVICES_VN
```

Multi-tenant site assignment:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Service Provider/CustomerA_Site
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - TENANT_A_PROD_VN
          - TENANT_A_DEV_VN
          - SHARED_SERVICES_VN

      - name: Global/Service Provider/CustomerB_Site
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - TENANT_B_PROD_VN
          - TENANT_B_DEV_VN
          - SHARED_SERVICES_VN
```

Example-6: Environment-Based Layer 3 Virtual Networks

This example shows how to create Layer 3 virtual networks based on environment types for development life-cycle management and application deployment stages.

```yaml
catalyst_center:
  fabric:
    l3_virtual_networks:
      - name: PRODUCTION_VN
      - name: STAGING_VN
      - name: DEVELOPMENT_VN
      - name: TESTING_VN
      - name: SANDBOX_VN
```

Environment-based site assignment:

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Development/Primary_Lab
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - DEVELOPMENT_VN
          - TESTING_VN
          - SANDBOX_VN

      - name: Global/Production/Data_Center
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - PRODUCTION_VN
          - STAGING_VN
```
