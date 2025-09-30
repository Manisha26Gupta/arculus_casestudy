terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_manifest" "orders" {
  manifest = yamldecode(file("${path.module}/k8s/deployment.yaml"))
}

resource "kubernetes_manifest" "orders_svc" {
  manifest = yamldecode(file("${path.module}/k8s/service.yaml"))
}

resource "kubernetes_manifest" "orders_ing" {
  manifest = yamldecode(file("${path.module}/k8s/ingress.yaml"))
}

resource "kubernetes_manifest" "orders_secret" {
  manifest = yamldecode(file("${path.module}/k8s/secret.yaml"))
}
