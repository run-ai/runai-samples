# AWS ECR Credential Renewal Cronjob

## Table of Contents

- [Why?](#why)
- [Solution](#solution)
- [Instructions](#instructions)

## Why?

AWS ECR provides login credentials that are valid for 12 hours. Over time, these credentials will become outdated, so the existing ECR secrets will become invalid.

## Solution

To address this issue, the following Kubernetes cronjob automatically renews the AWS ECR secret. 

This cronjob performs the following tasks:

- Renews the AWS ECR secret by running `aws ecr get-login` under the hood.
- Deletes the current ECR secret.
- Creates a new ECR secret.
- Labels the ECR secret to be available for all RunAI projects.

## Instructions

Follow these steps to set up and use the AWS ECR Credential Renewal Cronjob:

1. Edit the relevant fields in the `renew-ecr-secret-cronjob.yaml` file:

   - `serviceAccountName`
   - `AWS_ACCOUNT`
   - `AWS_REGION`
   - `schedule` (optional) - Change the interval time, currently set to every 8 hours, to ensure 24/7 availability.

2. Apply the cronjob to your Kubernetes cluster:

   ```bash
   kubectl apply -f renew-ecr-secret-cronjob.yaml

3. You are now ready to use the cronjob. When you submit a job that requires an ECR image, the image will be pulled seamlessly with the renewed credentials.

You can also manually trigger the cronjob to run with a manual job:

`kubectl create job --from=cronjob/aws-registry-credential-cron my-manually-job-name`
