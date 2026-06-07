
- sudo apt-get update
- sudo apt-get upgrade

- Required Packages
  
      sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

- Docker's Official GPG Key
  
      sudo mkdir -p /etc/apt/keyrings
      curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

- Docker Repository

      echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

- Docker Engine
  
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

- Verify Installation
  
      sudo docker run hello-world

- Manage Docker as a Non-Root User
  
      sudo usermod -aG docker $USER
      Uscita e rientro account utente per applicazione modifiche

- Verify Installation
  
      docker run hello-world

- sudo systemctl start docker
- sudo systemctl restart docker
- sudo systemctl status docker

- Docker null containers/images removal

      docker container prune    # <none> container
      docker image prune        # <none> images
      docker image prune -a     # unused images