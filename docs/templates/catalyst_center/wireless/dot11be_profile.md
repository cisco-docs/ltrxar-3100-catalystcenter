# 802.11be Profile (Wi-Fi 7)

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `802.11be Profiles`

{{ doc_gen }}

802.11be Profiles configure Wi-Fi 7 features such as OFDMA and MU-MIMO for enhanced wireless performance. They are referenced by [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles) via the `dot11be_profile_name` field in `ssid_details` and are applicable to both SDA fabric and non-fabric deployments. Requires IOS-XE controllers running version 17.15 or later.

### Examples

Example-1: Basic 802.11be profile with default OFDMA and MU-MIMO settings enabled for standard Wi-Fi 7 deployments:

```yaml
catalyst_center:
  wireless:
    dot11be_profiles:
      - name: WIFI7_STANDARD
        ofdma_down_link: true
        ofdma_up_link: true
        mu_mimo_down_link: true
        mu_mimo_up_link: true
```

Example-2: High-performance 802.11be profile with all advanced features enabled including OFDMA Multi-RU for maximum throughput in high-density environments:

```yaml
catalyst_center:
  wireless:
    dot11be_profiles:
      - name: WIFI7_HIGH_PERFORMANCE
        ofdma_down_link: true
        ofdma_up_link: true
        mu_mimo_down_link: true
        mu_mimo_up_link: true
        ofdma_multi_ru: true
```

Example-3: Minimal 802.11be profile with only downlink features enabled for environments with asymmetric traffic patterns:

```yaml
catalyst_center:
  wireless:
    dot11be_profiles:
      - name: WIFI7_DOWNLINK_ONLY
        ofdma_down_link: true
        ofdma_up_link: false
        mu_mimo_down_link: true
        mu_mimo_up_link: false
        ofdma_multi_ru: false
```

> **Note**: 802.11be profiles are supported only on IOS-XE controllers running device version 17.15 or later. The profile will be pushed to the device's "default-dot11be-profile".
