set -e  # Exit on any error

echo " creating K3s namespace and deploying sample Python application..."
kubectl apply -f namespace.yaml

echo" Create deployment......"
kubectl apply -f deployment.yaml

echo" Create service....."
kubectl apply -f service.yaml

echo" Verify deployment...."
kubectl get all -n sample-python-app