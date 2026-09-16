# Containers and Kubernetes

Container and cluster follow-up work that did not belong buried inside Linux local-privesc notes.
This page is intentionally compact but operational: quick triage first, then privilege and secret review.

## Docker and Container Triage

```bash
id
groups
ls -l /var/run/docker.sock
docker ps
docker images
docker inspect <container>
```

## Kubernetes Quick Checks

```bash
ls -l /var/run/secrets/kubernetes.io/serviceaccount
cat /var/run/secrets/kubernetes.io/serviceaccount/token
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace
kubectl auth can-i --list
kubectl get pods -A
kubectl get secrets -A
kubectl get nodes -o wide
```

## Common Abuse Paths

- Mounted Docker socket or container runtime access from inside a container.
- Overprivileged service accounts in Kubernetes.
- Secret harvesting from environment variables, mounted files, or Kubernetes secrets.
- HostPath mounts, privileged pods, or node-level access that collapses isolation.
