#!/bin/bash

apt update
apt upgrade -y

# Instalar dependencias para Docker
apt install -y ca-certificates curl

# Añadir la clave GPG de Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Añadir el repositorio de Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
> /etc/apt/sources.list.d/docker.list

apt update

# Instalar Docker y plugins
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar el conector MySQL para Python
apt install -y python3-mysql.connector

# Instalar node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs

# Instalar compilador de MJML
sudo npm install -g mjml