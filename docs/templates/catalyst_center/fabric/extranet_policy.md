# Extranet Policy

*Location in GUI*:
`Provision` » `SD-Access` » `Extranet Policies`

{{ doc_gen }}

Extranet Policies enable controlled inter-VN communication within the SD-Access fabric, allowing specific [Layer 3 Virtual Networks](/docs/data_models/catalyst_center/fabric/layer_3_virtual_network) to share resources while maintaining overall segmentation. Policies define a provider VN and one or more subscriber VNs, and can be scoped to specific [Fabric Sites](/docs/data_models/catalyst_center/fabric/fabric_site). This resource is **SDA fabric only**.

### Examples

Example-1: Basic Extranet Policy for Single Fabric Site

This example demonstrates how to create a basic extranet policy that enables communication between a provider virtual network and subscriber virtual networks within a specific SD-Access fabric site. Extranet policies allow controlled inter-VN communication, enabling specific virtual networks to share resources or services while maintaining overall network segmentation.

The extranet policy configuration includes:
* Policy name for identification and management
* Provider virtual network that shares resources or services
* One or more subscriber virtual networks that consume the shared resources
* Fabric site association for policy scope

```yaml
catalyst_center:
  fabric:
    extranet_policies:
      - name: SHARED_SERVICES_POLICY
        provider_virtual_network: SERVICES_VN
        subscriber_virtual_networks:
          - CORPORATE_VN
          - GUEST_VN
        fabric_sites:
          - Global/Campus/Building1
```

Example-2: Multi-Site Extranet Policy

This example shows how to configure an extranet policy that spans multiple fabric sites, enabling consistent inter-VN communication across different locations in the SD-Access deployment. This is useful for enterprise-wide shared services that need to be accessible from multiple sites.

```yaml
catalyst_center:
  fabric:
    extranet_policies:
      - name: ENTERPRISE_SHARED_SERVICES
        provider_virtual_network: SHARED_SERVICES_VN
        subscriber_virtual_networks:
          - FINANCE_VN
          - HR_VN
          - ENGINEERING_VN
        fabric_sites:
          - Global/North_America/HQ
          - Global/North_America/Branch_Office
          - Global/Europe/London_Office
```


### Important Considerations

:::note[Provider and Subscriber Virtual Networks]
* **Provider Virtual Network**: The virtual network that shares resources or services with other virtual networks. Only one provider VN can be specified per extranet policy.
* **Subscriber Virtual Networks**: The virtual networks that consume resources or services from the provider VN. Multiple subscriber VNs can be specified in a single extranet policy.
* All virtual networks (provider and subscribers) must exist and be assigned to the specified fabric sites before creating the extranet policy.
:::
