# Kubernetes Deployment

## Prerequisite
- Local Kubernetes cluster such as [Docker-Desktop Kubernetes](https://docs.docker.com/desktop/kubernetes/), [Minikube](https://minikube.sigs.k8s.io/docs/start/), etc.
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/#kubectl)

## Local Cluster
### Deploy
- `kubectl apply -k deploy/services/kustomize/db/base/` # Deploy database
- `kubectl apply -k deploy/services/kustomize/app/base/` # Deploy DSS
### Destroy
- `kubectl delete -k deploy/services/kustomize/app/base/` # Destroy DSS
- `kubectl delete -k deploy/services/kustomize/db/base/` # Destroy database
