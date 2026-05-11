# Network-as-Code Catalyst Center

Manage Cisco Catalyst Center following Infrastructure as Code principles. Codify Catalyst Center into declarative configuration files.

## Documentation

Documentation is available [here](https://netascode.cisco.com).

## Related Repositories

There are three different `nac-catalystcenter` repositories:

*   **Internal Source of Truth (SoT):**
    `https://wwwin-github.cisco.com/netascode/nac-catalystcenter`
    This internal `nac-catalystcenter` repo serves as the SoT for schema, validation rules, post deployment tests, defaults, documentation templates, integration tests, and more. The `schemas/schema.yaml` file, `validation/rules/` and `/templates/catalyst_center/test` directories from this SoT are automatically copied to the internal Terraform example repository.

*   **Internal Terraform Example:**
    `https://wwwin-github.cisco.com/netascode/nac-catalystcenter-terraform`
    This internal repository provides an example configuration and pipeline templates, serving as a starting point for new projects. It automatically receives schema, rules and tests from the internal `nac-catalystcenter` repo.

*   **External Terraform Module (Terraform Registry):**
    `https://wwwin-github.cisco.com/netascode/terraform-catalystcenter-nac-catalystcenter`
    This external repository hosts the Terraform Module, which is published in the Terraform Registry. The defaults file from the internal `nac-catalystcenter` repo is copied to this repository.
