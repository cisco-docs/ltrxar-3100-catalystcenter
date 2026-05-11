terraform {
  required_providers {
    catalystcenter = {
      source = "CiscoDevNet/catalystcenter"
    }
  }
}

provider "catalystcenter" {
  max_timeout = 600
}

module "catalyst_center" {
  source = "git::https://www.github.com/netascode/terraform-catalystcenter-nac-catalystcenter.git?ref=main"

  yaml_directories      = ["../standard", "../standard_multi_state"]
  templates_directories = ["../standard/templates/"]

  manage_global_settings     = false
  managed_sites              = ["Global/AREA_0"]
  manage_specific_sites_only = false
}