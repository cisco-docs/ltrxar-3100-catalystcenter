# Power Profile

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `Power Profiles`

{{ doc_gen }}

Power Profiles define power management rules for Access Points, controlling radio states, spatial streams, Ethernet speeds, and USB interfaces. They are referenced by [AP Profiles](/docs/data_models/catalyst_center/wireless/ap_profile) via the `power_profile` field (always-on) and `calendar_power_profiles` entries (scheduled) and are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Power profile that disables the 6 GHz radio to reduce power consumption on APs with limited PoE budget:

```yaml
catalyst_center:
  wireless:
    power_profiles:
      - name: DISABLE_6GHZ
        description: Disable 6 GHz radio for low-power APs
        rules:
          - interface_type: RADIO
            interface_id: 6GHZ
            parameter_type: STATE
            parameter_value: DISABLE
```

Example-2: Power profile that limits Ethernet speed and reduces radio spatial streams for energy-efficient deployments:

```yaml
catalyst_center:
  wireless:
    power_profiles:
      - name: LOW_POWER
        description: Low power mode for energy savings
        rules:
          - interface_type: ETHERNET
            interface_id: GIGABITETHERNET0
            parameter_type: SPEED
            parameter_value: 1000MBPS
          - interface_type: RADIO
            interface_id: 5GHZ
            parameter_type: SPATIALSTREAM
            parameter_value: TWO_BY_TWO
          - interface_type: RADIO
            interface_id: 2_4GHZ
            parameter_type: SPATIALSTREAM
            parameter_value: TWO_BY_TWO
```

Example-3: Power profile that disables USB and secondary 5 GHz radio while limiting the primary Ethernet port speed:

```yaml
catalyst_center:
  wireless:
    power_profiles:
      - name: MINIMAL_POWER
        description: Minimal power for constrained PoE environments
        rules:
          - interface_type: ETHERNET
            interface_id: GIGABITETHERNET0
            parameter_type: SPEED
            parameter_value: 100MBPS
          - interface_type: RADIO
            interface_id: SECONDARY_5GHZ
            parameter_type: STATE
            parameter_value: DISABLE
          - interface_type: USB
            interface_id: USB0
            parameter_type: STATE
            parameter_value: DISABLE
```

> **Note**: Power profiles are referenced from AP profiles using `power_profile` for the always-on profile and `power_profile` on each `calendar_power_profiles` entry for scheduled profiles. The order of rules in the list is significant — rules are applied sequentially.
