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

  yaml_directories      = ["../standard", "../standard_single_state"]
  templates_directories = ["../standard/templates/"]
}