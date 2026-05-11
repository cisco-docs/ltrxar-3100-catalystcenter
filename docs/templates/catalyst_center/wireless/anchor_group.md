# Anchor Group

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `Anchor Groups`

{{ doc_gen }}

Anchor Groups are used in **non-SDA-fabric** (traditional/FlexConnect) deployments for guest traffic tunneling via the foreign-anchor WLC architecture. In SDA fabric deployments, guest traffic is handled natively by the fabric and anchor groups are not needed. Anchor Groups are referenced by Wireless Profiles via the `anchor_group_name` field in `ssid_details` — see [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles).

### Examples

Example-1: Anchor group with a single managed anchor WLC (controller managed by Catalyst Center):

```yaml
catalyst_center:
  wireless:
    anchor_groups:
      - name: AG_Guest
        mobility_anchors:
          - device_name: C9800-CL-WLC
            ip_address: 10.0.0.1
            anchor_priority: PRIMARY
            managed_anchor_wlc: true
```

Example-2: Anchor group with multiple managed anchors for redundancy:

```yaml
catalyst_center:
  wireless:
    anchor_groups:
      - name: AG_Guest_HA
        mobility_anchors:
          - device_name: WLC-ANCHOR-1
            ip_address: 10.0.0.1
            anchor_priority: PRIMARY
            managed_anchor_wlc: true
          - device_name: WLC-ANCHOR-2
            ip_address: 10.0.0.2
            anchor_priority: SECONDARY
            managed_anchor_wlc: true
```

Example-3: Anchor group with an external (unmanaged) anchor WLC requiring additional mobility fields:

```yaml
catalyst_center:
  wireless:
    anchor_groups:
      - name: AG_External
        mobility_anchors:
          - device_name: EXT-WLC-ANCHOR
            ip_address: 172.16.0.1
            anchor_priority: PRIMARY
            managed_anchor_wlc: false
            peer_device_type: IOS-XE
            mac_address: "aa:bb:cc:00:00:01"
            mobility_group_name: default
```

> **Note**: Anchor groups support up to 3 mobility anchors per group. When `managed_anchor_wlc` is `false` (external anchor), the fields `peer_device_type`, `mac_address`, and `mobility_group_name` are required by the API. For managed anchors, the `device_name` can be the short hostname — the module automatically resolves it to the FQDN from the Catalyst Center inventory.
