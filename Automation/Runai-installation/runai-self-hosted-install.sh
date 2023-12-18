#!/bin/bash
#description : This script will help to install Run:ai in a self hosted environment
#author	     : Steve Blow
#date        : 12/2023
#version     : 1.0
#usage       : Please make sure to run this script as ROOT or with ROOT permissions
#==============================================================================
NC='\033[0m'
PINK='\033[0;95m'
GREEN='\033[0;32m'
RED='\033[0;31m'

# *** Install Prometheus
function prom-install {
        echo  -e "${GREEN} Installing Prometheus...${NC}"
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm repo update
        helm install prometheus prometheus-community/kube-prometheus-stack \
        -n monitoring --create-namespace --set grafana.enabled=false
}

# *** Install Nginx-Ingress
function nginx-install {
        echo  -e "${GREEN} Installing nginx-ingress...${NC}"
        helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
        helm repo update
        helm upgrade -i nginx-ingress ingress-nginx/ingress-nginx   \
        --namespace nginx-ingress --create-namespace \
        --set controller.kind=DaemonSet \
        --set controller.admissionWebhooks.enabled=false \
        --set controller.service.externalIPs="{${int_ip}}"
}

# *** Install Helm
function install-helm {
	if [ -x "$(command -v helm)" ]
    then
        echo -e "${GREEN} Helm already installed ${NC}"
    else
		echo -e "${GREEN} Installing Helm ${NC}"
        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
        sudo chmod 700 get_helm.sh
        sudo ./get_helm.sh
	fi
}

# ***  install nvidia gpu operator
function install-gpu-operator {
	   echo  -e "${GREEN} Installing NVIDIA GPU operator...${NC}"
	   helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
       helm install --wait --generate-name -n gpu-operator --create-namespace nvidia/gpu-operator
       sleep 300
       kubectl wait pods -n gpu-operator  -l app=nvidia-operator-validator --for condition=Ready --timeout=1200s
       echo  -e "${GREEN}NVIDIA GPU Operator deployed${NC}"
}

# *** install Run:ai Control Plane
function runai-cp-install {
        echo  -e "${GREEN} Installing Run:ai control plane...${NC}"
        kubectl create namespace runai-backend
        kubectl apply -f "${gcr_secret}"
        kubectl create secret tls runai-backend-tls -n runai-backend \
        --cert "${cert}" --key "${key}"
        helm repo add runai-backend https://backend-charts.storage.googleapis.com
        helm repo update
        if [ -z "$version" ];
        then
            helm upgrade -i runai-backend -n runai-backend runai-backend/control-plane \
            --set global.domain="${domain}"
        else
            helm upgrade -i runai-backend -n runai-backend runai-backend/control-plane \
            --set global.domain="${domain}" --version="${version}"
        fi
}

# *** add cluster to control plane and pull values yaml
function runai-token-values {
    token=$(curl --insecure --location --request POST "https://$cpdomain/auth/realms/runai/protocol/openid-connect/token" \
        --header 'Content-Type: application/x-www-form-urlencoded' \
        --data-urlencode 'grant_type=password' \
        --data-urlencode 'client_id=runai' \
        --data-urlencode 'username=test@run.ai' \
        --data-urlencode 'password=Abcd!234' \
        --data-urlencode 'scope=openid' \
        --data-urlencode 'response_type=id_token' | jq -r .access_token)
    uuid=$(curl --insecure -X 'POST' \
        "https://$cpdomain/v1/k8s/clusters" \
        -H 'accept: application/json' \
        -H "Authorization: Bearer $token" \
        -H 'Content-Type: application/json' \
        -d "{
    \"name\": \"${cluster_name}\",
    \"description\": \"group-a-cluster\"
  }" | jq -r .uuid)
          curl --insecure "https://$cpdomain/v1/k8s/clusters/$uuid/installfile?cloud=op" \
            -H 'accept: application/json' \
            -H "Authorization: Bearer $token" \
            -H 'Content-Type: application/json' > "${cluster_name}".yaml
}

# *** install run:ai cluster
function runai-cluster-install {
        echo  -e "${GREEN} Installing Run:ai cluster...${NC}"
        helm repo add runai https://run-ai-charts.storage.googleapis.com
        helm repo update
        if [ -z "$clversion" ];
        then
            helm upgrade -i runai-cluster runai/runai-cluster -n runai -f "${cluster_name}".yaml --create-namespace
        else
            helm upgrade -i runai-cluster runai/runai-cluster -n runai -f "${cluster_name}".yaml --create-namespace --version="${clversion}"
        fi
}

###START HERE###

echo -e "${PINK}Welcome to the Run:ai installer for self hosted deployments \n\nPlease select a task \n\n1. install prometheus, \n2. install nginx-ingress, \n3. install nvidia gpu-operator, \n4. install run:ai control plane, \n5. install a run:ai cluster, \n6. exit${NC}"
read -r task
if [ "${task}" == "1" ]
then
    echo -e "${GREEN} *** Please make sure kubeconfig is set for your cluster *** ${NC}"
    sleep 3
    install-helm
    prom-install
elif [ "${task}" == "2" ]
then
    echo -e "${GREEN} *** Please make sure kubeconfig is set for your cluster *** ${NC}"
    sleep 3
    install-helm
    defaultint=$(kubectl get nodes -o wide | grep control-plane | head -n 1 | awk '{print $6}')
    read -r -p "$(echo -e "${PINK}Please enter an ip for ingress or accept default choice (${defaultint}):${NC}")" int_ip
    int_ip=${int_ip:-"${defaultint}"}
    nginx-install
elif [ "${task}" == "3" ]
then
    echo -e "${GREEN} *** Please make sure kubeconfig is set for your cluster *** ${NC}"
    sleep 3
    install-helm
    install-gpu-operator
elif [ "${task}" == "4" ]
then
    echo -e "${GREEN} *** Please make sure kubeconfig is set for your cluster  *** ${NC}"
    sleep 3
    install-helm
    read -r -p "$(echo -e "${PINK}Please enter the full path to runai-gcr-secret.yaml (e.g. /path/to/runai-gcr-secret.yaml):${NC}")" gcr_secret
    read -r -p "$(echo -e "${PINK}Please enter the full path to the ssl certificate private key (e.g. /path/to/private.pem):${NC}")" key
    read -r -p "$(echo -e "${PINK}Please enter the full path to the ssl certificate (e.g. /path/to/fullchain.pem):${NC}")" cert
    read -r -p "$(echo -e "${PINK}Please enter the domain url for the Run:ai control plane (e.g. runai.domain.com):${NC}")" domain
    read -r -p "$(echo -e "${PINK}Enter required version or leave blank for latest:${NC}")" version
    runai-cp-install
    kubectl wait --for=condition=Ready pods --all -n runai-backend --timeout=10m
    echo  -e "${GREEN} \nRun:ai Control Plane Installed.\n${NC}"
elif [ "${task}" == "5" ]
then
    echo -e "${GREEN} *** Please make sure kubeconfig is set for your cluster  *** ${NC}"
    sleep 3
    install-helm
    read -r -p "$(echo -e "${PINK}Please enter a name for the Run:ai cluster ([a-z] Lowercase only. Numbers/Symbols/spaces/special characters are not allowed here):${NC}")" cluster_name
    read -r -p "$(echo -e "${PINK}Enter required version or leave blank for latest:${NC}")" clversion
    cpdomain=$(kubectl get ing -n runai-backend | grep runai-backend-ingress | awk '{print $3}')
    runai-token-values
    runai-cluster-install
    kubectl wait --for=condition=Ready pods --all -n runai --timeout=10m
    echo  -e "${GREEN} \nRun:ai Cluster ${cluster_name} Installed.\n${NC}"
elif [ "${task}" == "6" ]
then
    exit
fi
exec /bin/bash "$0" "$@"
