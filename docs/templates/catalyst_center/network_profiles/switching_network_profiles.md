# Switching Network Profiles

*Location in GUI*:
`Design` » `Network Profiles`

{{ doc_gen }}

Switching Network Profiles associate CLI [Templates](/docs/data_models/catalyst_center/templates/template) (onboarding and Day-N) with sites for wired device provisioning. They define which configuration templates are applied to switches during initial onboarding and ongoing management. Applicable to both SDA fabric and non-fabric deployments.

### Examples


Example-1: A simple switching network profile that applies "SDA SWITCH PROFILE" as the unique identifier, uses "onboarding_template" for initial device provisioning, applies "aaa_template" for ongoing AAA (Authentication, Authorization, Accounting) configuration, and deploys across four different building locations in the United States:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: SDA SWITCH PROFILE
        onboarding_templates:
          - onboarding_template
        dayn_templates: 
          - aaa_template
        sites:
          - Global/United States/Golden Hills Campus/Sunset Tower
          - Global/United States/Lakefront Tower/Windy City Plaza
          - Global/United States/Oceanfront Mansion/Art Deco Mansion
          - Global/United States/Desert Oasis Branch/Desert Oasis Tower
```



Example-2: An enterprise campus profile using device-specific on boarding templates for Catalyst 9300 and 9500 switches, with multiple day-N templates for ongoing configuration management across AAA, QoS, VLAN, and monitoring domains, deployed to European corporate locations:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: ENTERPRISE_CAMPUS_PROFILE
        onboarding_templates:
          - C9300_switch_config
          - C9500_switch_config
        dayn_templates:
          - aaa_config
          - qos_policy
          - vlan_management
          - monitoring_config
        sites:
          - Global/Europe/Germany/Munich/Corporate Campus
          - Global/Europe/United Kingdom/London/Financial District
          - Global/Europe/France/Paris/Innovation Center
```



Example-3: Two distinct profiles optimized for different deployment scenarios: a branch office profile for smaller remote locations with specific WAN and security requirements, and a headquarters profile designed for core campus infrastructure with comprehensive management and monitoring capabilities:

```yaml
catalyst_center:
  network_profiles:
    switching:
      - name: BRANCH_OFFICE_PROFILE
        onboarding_templates:
          - branch_base_config
        dayn_templates:
          - branch_security
          - wan_optimization
        sites:
          - Global/Asia Pacific/Australia/Sydney/Branch Office
          - Global/Americas/Brazil/Sao Paulo/Regional Office
          - Global/Europe/Netherlands/Amsterdam/Distribution Center   
      - name: HEADQUARTERS_PROFILE
        onboarding_templates:
          - hq_core_switch_onboarding
          - hq_access_switch_onboarding
        dayn_templates:
          - hq_advanced_security
          - hq_qos_enterprise
          - hq_monitoring_full
          - hq_compliance
        sites:
          - Global/Americas/USA/Headquarters/New York/Main Campus
          - Global/Asia Pacific/Singapore/Regional HQ
          - Global/Europe/Switzerland/Zurich/Executive Office
```

