package test

import (
  "testing"
  "github.com/gruntwork-io/terratest/modules/terraform"
  "github.com/gruntwork-io/terratest/modules/k8s"
  "github.com/stretchr/testify/assert"
)

func TestEKSCluster(t *testing.T) {
  t.Parallel()

  terraformOptions := &terraform.Options{
    TerraformDir: "../path/to/your/terraform/code",

    Vars: map[string]interface{}{
      "variable_name": "value",
    },
  }
  
  defer terraform.Destroy(t, terraformOptions)
  terraform.InitAndApply(t, terraformOptions)

  kubeconfig := terraform.Output(t, terraformOptions, "kubeconfig")
  options := k8s.NewKubectlOptions("", kubeconfig, "default")

  // Verify the EKS cluster is running 
  nodes := k8s.GetNodes(t, options)
  assert.NotEmpty(t, nodes)
}
