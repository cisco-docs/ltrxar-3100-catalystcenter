# SSID Mapping to VLAN

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `Wireless SSIDs`

{{ doc_gen }}

SSID to VLAN Mapping defines how wireless [SSIDs](/docs/data_models/catalyst_center/wireless/ssid) are mapped to VLANs within an SD-Access [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site). This enables wireless clients to be placed into specific VLANs based on the SSID they connect to, providing segmentation and policy enforcement aligned with the fabric's [Anycast Gateway](/docs/data_models/catalyst_center/fabric/anycast_gateway) addressing. This resource is **SDA fabric only**.

### Examples

Example-1: Basic SSID to VLAN Mapping Configuration

This example demonstrates how to configure basic SSID to VLAN mapping within an SD-Access fabric site for wireless network segmentation. SSID mapping enables wireless clients to be placed into specific VLANs based on the SSID they connect to, providing network segmentation and policy enforcement for different user groups.

The SSID to VLAN mapping configuration includes:
* Fabric site specification (Global/Canada) for geographic organization
* SSID name (SSID_1) for wireless network identification
* VLAN name mapping (VLAN_GUEST) for network segmentation and traffic isolation
* The VLAN name used are VLANs defined as part of the Fabric Anycast gateway configuration, and should have `wireless_pool: true`
* Direct association between wireless access and wired VLAN infrastructure
* Foundation for wireless policy enforcement and security controls

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        wireless_ssids:
          - name: SSID_1
            vlan_name: VLAN_GUEST
```

Example-2: Multiple SSID Mappings for Different User Types

This example shows how to configure multiple SSID to VLAN mappings within a single fabric site for comprehensive wireless network segmentation supporting different user categories and access requirements.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North_America/Corporate_Campus
        wireless_ssids:
          - name: CORPORATE_WIFI
            vlan_name: CORPORATE_USERS
          - name: GUEST_WIFI
            vlan_name: GUEST_ACCESS
          - name: IOT_DEVICES
            vlan_name: IOT_NETWORK
          - name: CONTRACTOR_WIFI
            vlan_name: CONTRACTOR_ACCESS
```

Example-3: Department-Based SSID to VLAN Mapping

This example demonstrates how to configure SSID to VLAN mappings organized by department or functional area for enterprise environments requiring departmental wireless network isolation.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Europe/Corporate_HQ
        wireless_ssids:
          - name: FINANCE_SECURE
            vlan_name: FINANCE_VLAN
          - name: HR_PRIVATE
            vlan_name: HR_VLAN
          - name: ENGINEERING_LAB
            vlan_name: ENGINEERING_VLAN
          - name: MARKETING_TEAM
            vlan_name: MARKETING_VLAN
          - name: EXECUTIVE_ACCESS
            vlan_name: EXECUTIVE_VLAN
```

Example-4: Multi-Site SSID Mapping with Consistent Naming

This example shows how to configure consistent SSID to VLAN mappings across multiple fabric sites for standardized wireless deployment in distributed enterprise environments.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North_America/New_York_Office
        wireless_ssids:
          - name: EMPLOYEE_SECURE
            vlan_name: EMPLOYEE_NETWORK
          - name: VISITOR_ACCESS
            vlan_name: VISITOR_NETWORK
          - name: BYOD_DEVICES
            vlan_name: BYOD_NETWORK
      - name: Global/Europe/London Office
        wireless_ssids:
          - name: EMPLOYEE_SECURE
            vlan_name: EMPLOYEE_NETWORK
          - name: VISITOR_ACCESS
            vlan_name: VISITOR_NETWORK
          - name: BYOD_DEVICES
            vlan_name: BYOD_NETWORK
      - name: Global/Asia Pacific/Tokyo Office
        wireless_ssids:
          - name: EMPLOYEE_SECURE
            vlan_name: EMPLOYEE_NETWORK
          - name: VISITOR_ACCESS
            vlan_name: VISITOR_NETWORK
```

Example-5: Security Zone SSID Mapping Configuration

This example demonstrates how to configure SSID to VLAN mappings based on security zones and trust levels for environments requiring strict wireless security segmentation and compliance.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Security/HighSecurityFacility
        wireless_ssids:
          - name: CLASSIFIED_NETWORK
            vlan_name: SECURE_ZONE_VLAN
          - name: INTERNAL_STAFF
            vlan_name: INTERNAL_ZONE_VLAN
          - name: VENDOR_LIMITED
            vlan_name: DMZ_ZONE_VLAN
          - name: QUARANTINE_NET
            vlan_name: QUARANTINE_VLAN
```

Example-6: Service Provider Multi-Tenant SSID Mapping

This example shows how to configure SSID to VLAN mappings for service provider environments with customer-specific wireless networks and tenant isolation requirements.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Service_Provider/Shared_Building
        wireless_ssids:
          - name: TENANT_A_CORPORATE
            vlan_name: TENANT_A_PRODUCTION
          - name: TENANT_A_GUEST
            vlan_name: TENANT_A_GUEST_VLAN
          - name: TENANT_B_CORPORATE
            vlan_name: TENANT_B_PRODUCTION
          - name: TENANT_B_GUEST
            vlan_name: TENANT_B_GUEST_VLAN
          - name: SHARED_SERVICES
            vlan_name: SHARED_SERVICES_VLAN
```

Example-7: Educational Institution SSID Mapping

This example demonstrates how to configure SSID to VLAN mappings for educational environments with different access requirements for students, faculty, staff, and guests.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Education/University_Campus
        wireless_ssids:
          - name: STUDENT_WIFI
            vlan_name: STUDENT_NETWORK
          - name: FACULTY_SECURE
            vlan_name: FACULTY_NETWORK
          - name: STAFF_ADMIN
            vlan_name: STAFF_NETWORK
          - name: RESEARCH_LAB
            vlan_name: RESEARCH_NETWORK
          - name: CAMPUS_GUEST
            vlan_name: CAMPUS_GUEST_VLAN
          - name: LIBRARY_PUBLIC
            vlan_name: LIBRARY_ACCESS_VLAN
```