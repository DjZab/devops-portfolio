terraform {
  required_version = ">= 1.12"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~>2.9"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.9"
    }
  }
}
resource "random_pet" "pet" {
}

resource "local_file" "file" {
  content  = random_pet.pet.id
  filename = "${path.module}/foo.bar"
}

