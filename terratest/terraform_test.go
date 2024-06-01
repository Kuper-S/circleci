package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerraformExample(t *testing.T) {
	t.Parallel()

	// Define the Terraform options
	terraformOptions := &terraform.Options{
		// The path to where your Terraform code is located
		TerraformDir: "../terraform",

		// Variables to pass to our Terraform code using -var options
		Vars: map[string]interface{}{
			"AWS_ACCESS_KEY_ID":     "<your-access-key-id>",
			"AWS_SECRET_ACCESS_KEY": "<your-secret-access-key>",
		},

		// Disable colors in Terraform commands so its easier to parse stdout/stderr
		NoColor: true,
	}

	// Clean up resources with "terraform destroy" at the end of the test
	defer terraform.Destroy(t, terraformOptions)

	// Run "terraform init" and "terraform apply". Fail the test if there are any errors.
	terraform.InitAndApply(t, terraformOptions)

	// Run "terraform output" to get the values of output variables
	vpcId := terraform.Output(t, terraformOptions, "vpc_id")

	// Verify we're getting back the outputs we expect
	assert.NotEmpty(t, vpcId)
}
