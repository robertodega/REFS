
#   Kubectl installation

    sudo apt update && sudo apt install -y apt-transport-https curl
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt update && sudo apt install -y kubectl

    #   if Linux version is too recent:
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
    kubectl version --client

    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube start
    kubectl config use-context minikube


#   Kubernetes Project creation

    mkdir kubernetes-example
    cd kubernetes-example
    touch deployment.yaml service.yaml

    nano deployment.yaml            #   Pod management

        apiVersion: apps/v1
        kind: Deployment
        metadata:
        name: nginx-deployment
        labels:
            app: nginx
        spec:
        replicas: 2
        selector:
            matchLabels:
            app: nginx
        template:
            metadata:
            labels:
                app: nginx
            spec:
            containers:
            - name: nginx
                image: nginx:1.21
                ports:
                - containerPort: 80

    nano service.yaml               #   Pod exposure outside Kubernetes cluster

        apiVersion: v1
        kind: Service
        metadata:
        name: nginx-service
        spec:
        selector:
            app: nginx
        ports:
            - protocol: TCP
            port: 80
            targetPort: 80
        type: NodePort

#   Configuration apply

    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    kubectl get pods                #   Pod execution check
    kubectl get service             #   Service check

#   Node Ip check

    kubectl get nodes -o wide

#   Application access

    http://<NODE-IP>:32000

#   Deployment & Service removal

    kubectl delete -f deployment.yaml
    kubectl delete -f service.yaml

