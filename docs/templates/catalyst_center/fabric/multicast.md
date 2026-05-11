# Fabric Multicast

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `Multicast`

{{ doc_gen }}

Fabric Multicast enables efficient one-to-many communication within the SD-Access fabric for applications like video streaming and real-time collaboration. Multicast is configured per [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site) and [Layer 3 Virtual Network](/docs/data_models/catalyst_center/fabric/layer_3_virtual_network), with support for internal fabric Rendezvous Points (RP), external RPs, and SSM (Source-Specific Multicast) ranges. This resource is **SDA fabric only**.

### Examples

Example-1: Basic Fabric Multicast with Internal Fabric RP

This example demonstrates the simplest multicast configuration within an SD-Access fabric site using an internal fabric Rendezvous Point (RP). Multicast enables efficient one-to-many communication for applications like video streaming and real-time collaboration.

The multicast configuration includes:
* Virtual network specification (Campus) for multicast traffic isolation
* IP pool assignment (Multicast-IPPool) for multicast signaling addresses
* Internal fabric RP using a border device (BN1.example.com)
* Default IPv4 RP configuration for ASM (Any-Source Multicast) with default ranges

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        multicast:
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool
              multicast_rps:
                - name: FABRIC_RP_1
                  rp_location: FABRIC
                  is_default_v4_rp: true
                  fabric_rps:
                    - BN1.example.com
```

Example-2: Fabric Multicast with Dual-Stack RP Support

This example shows how to configure a fabric RP that supports both IPv4 and IPv6 multicast traffic using default ASM ranges for both protocols.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        multicast:
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool1
              multicast_rps:
                - name: FABRIC_RP_1
                  rp_location: FABRIC
                  is_default_v4_rp: true
                  is_default_v6_rp: true
                  fabric_rps:
                    - BN1.example.com
```

Example-3: Fabric Multicast with SSM and Default ASM Ranges

This example demonstrates combining Source-Specific Multicast (SSM) for optimized delivery with Any-Source Multicast (ASM) using default ranges. SSM is ideal for one-to-many applications where the source is known.

Key configuration details:
* SSM range: 232.0.0.0/24 (IPv4 SSM ranges must be within 232.0.0.0/8)
* Default ASM ranges are used (no explicit ipv4_asm_ranges specified)
* Fabric RP supports both IPv4 and IPv6 default ranges

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        multicast:
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool1
              ipv4_ssm_ranges:
                - 232.0.0.0/24
              multicast_rps:
                - name: FABRIC_RP_1
                  rp_location: FABRIC
                  is_default_v4_rp: true
                  is_default_v6_rp: true
                  fabric_rps:
                    - BN1.example.com
```

Example-4: External RP with Custom ASM Ranges and SSM

This example shows how to configure multicast with an external Rendezvous Point located outside the SD-Access fabric, useful for integrating with existing multicast infrastructure. The configuration includes custom ASM ranges for specific multicast groups.

Important notes:
* External RP requires either IPv4 or IPv6 address (not both for a single RP)
* Custom ASM range (239.0.0.0/24) for specific multicast groups
* Non-default RP configuration (is_default_v4_rp: false) allows multiple RPs with different group ranges
* SSM range (232.0.5.0/24) for source-specific multicast traffic

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        multicast:
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool1
              ipv4_ssm_ranges:
                - 232.0.5.0/24
              multicast_rps:
                - name: EXTERNAL_RP_1
                  rp_location: EXTERNAL
                  ipv4_address: 10.1.1.100
                  is_default_v4_rp: false
                  ipv4_asm_ranges:
                    - 239.0.0.0/24
```

Example 5: Multicast Replication Mode — Native Multicast vs Headend Replication

The `replication_mode` attribute controls how multicast traffic is distributed in the overlay network. Two modes are supported:

* **`NATIVE_MULTICAST`** — Uses PIM-based multicast in the overlay to replicate the traffic it within a fabric. Requires multicast-capable underlay infrastructure. More efficient for large-scale deployments with many receivers.

* **`HEADEND_REPLICATION`** — Multicast traffic is replicated at the ingress VTEP and sent as individual unicast copies to each egress VTEP. Simpler to deploy as it does not require multicast in the underlay, but generates more replication traffic at the source.

The following configuration shows two fabric sites — one using Native Multicast with full RP and SSM/ASM configuration, and one using Headend Replication with minimal setup.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      # Site using Native Multicast with fabric and external RPs
      - name: Global/Poland/Krakow
        multicast:
          replication_mode: NATIVE_MULTICAST
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool1
              ipv4_ssm_ranges:
                - 232.0.0.0/24
              multicast_rps:
                - name: FABRIC_RP_1
                  rp_location: FABRIC
                  is_default_v4_rp: false
                  is_default_v6_rp: false
                  fabric_rps:
                    - BN1.example.com
                  ipv4_asm_ranges:
                    - 228.0.0.0/16
                - name: EXTERNAL_RP_1
                  rp_location: EXTERNAL
                  ipv4_address: 10.1.1.100
                  is_default_v4_rp: true

      # Site using Headend Replication — no underlay multicast required
      - name: Global/Poland/Warsaw
        multicast:
          replication_mode: HEADEND_REPLICATION
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool2
```


Example 6: Wireless Fabric Multicast

The `wireless_multicast_enabled` attribute controls whether multicast traffic is forwarded to wireless clients within a fabric site. This requires:
* A Wireless Controller assigned to the fabric site, configured under `catalyst_center.inventory.devices` with one of the following `fabric_roles`:
  * **`WIRELESS_CONTROLLER_NODE`** for a standalone WLC (e.g., Catalyst 9800 series)
  * **`EMBEDDED_WIRELESS_CONTROLLER_NODE`** for an embedded WLC (eWLC) running on a fabric switch (e.g., Catalyst 9300/9400/9500). For eWLC, also set `enable_wireless: true` on the device to activate the embedded wireless capability
* At least one fabric-enabled SSID (with `enable_fabric: true`) assigned to the fabric site

For optimal performance, ensure wired multicast (`replication_mode`) is also configured.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Warsaw
        multicast:
          replication_mode: NATIVE_MULTICAST
          wireless_multicast_enabled: true
          virtual_networks:
            - name: Campus
              ip_pool_name: Multicast-IPPool
              multicast_rps:
                - name: FABRIC_RP_1
                  rp_location: FABRIC
                  is_default_v4_rp: true
                  fabric_rps:
                    - BN1.example.com
```


### Important Limitations and Constraints

:::note[IPv6-Only Multicast Not Supported]
IPv6-only multicast configurations are currently not supported. You must configure IPv4 multicast, optionally with dual-stack (IPv4 + IPv6) support.
:::

:::note[Dual-Stack Pool and Dual RP Limitation]
Dual-stack multicast pools (IPv4 + IPv6) cannot be used with dual fabric RPs (two border devices). You must choose one of the following configurations:
* **Single-stack multicast pool** (IPv4 only) with **dual fabric RPs** (two border devices)
* **Dual-stack multicast pool** (IPv4 + IPv6) with **single fabric RP** (one border device)
:::

:::note[Multicast Replication Mode]
Two replication modes are available via the `replication_mode` attribute:

* **`NATIVE_MULTICAST`** — PIM-based multicast in the overlay. Requires multicast-capable infrastructure. Best for large fabrics with many multicast receivers.
* **`HEADEND_REPLICATION`** — Ingress replication via unicast copies. No underlay multicast required. Simpler to deploy but higher replication overhead at the source VTEP.

When `replication_mode` is omitted, the fabric site defaults to **Headend Replication**.
:::