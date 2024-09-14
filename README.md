
# Barbershop Django Application

This is a Django-based Barbershop Scheduling Application. It can be deployed on Kubernetes and managed using ArgoCD.

## Prerequisites

- Docker installed on your machine
- Kubernetes cluster (minikube, local, or cloud-based like GKE, EKS, AKS)
- kubectl configured to access your Kubernetes cluster
- ArgoCD installed and configured in your Kubernetes cluster
- GitHub repository for storing your application source code and Kubernetes manifests

## Steps

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/barbershop-django-argocd.git
cd barbershop-django-argocd
```

### 2. Build the Docker Image

Build the Docker image for your Django application:

```bash
docker build -t your-dockerhub-username/django-app:latest .
```

Push the image to your Docker registry:

```bash
docker push your-dockerhub-username/django-app:latest
```

### 3. Kubernetes Setup

#### 3.1 Create Kubernetes Secrets for Django

Generate a `DJANGO_SECRET_KEY`:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Create the `django-secrets.yaml` file:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secrets
type: Opaque
data:
  DJANGO_SECRET_KEY: <your-secret-key-base64-encoded>
```

Apply the secret to your cluster:

```bash
kubectl apply -f django-secrets.yaml
```

#### 3.2 Persistent Volume for SQLite

Create a PersistentVolumeClaim (PVC) for SQLite:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sqlite-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

Apply the PVC:

```bash
kubectl apply -f sqlite-pvc.yaml
```

### 4. Deploy the Application to Kubernetes

Create a `deployment.yaml` file for the Django app:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
spec:
  replicas: 1  # Use one replica for SQLite (SQLite is not built for concurrent writes)
  selector:
    matchLabels:
      app: django
  template:
    metadata:
      labels:
        app: django
    spec:
      containers:
      - name: django
        image: your-dockerhub-username/django-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DJANGO_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: DJANGO_SECRET_KEY
        volumeMounts:
        - mountPath: /app/db
          name: sqlite-storage
      volumes:
      - name: sqlite-storage
        persistentVolumeClaim:
          claimName: sqlite-pvc
```

Apply the deployment:

```bash
kubectl apply -f deployment.yaml
```

Expose the service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: django-service
spec:
  type: LoadBalancer
  selector:
    app: django
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

Apply the service:

```bash
kubectl apply -f service.yaml
```

### 5. Set Up ArgoCD for Continuous Deployment

1. Install ArgoCD in your cluster (if you haven't yet):
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. Access the ArgoCD UI:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

3. Login to ArgoCD:
   ```bash
   argocd login localhost:8080
   ```

4. Create an ArgoCD application pointing to your GitHub repo:

   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: django-app
     namespace: argocd
   spec:
     destination:
       namespace: default
       server: https://kubernetes.default.svc
     project: default
     source:
       path: k8s
       repoURL: 'https://github.com/yourusername/barbershop-django-argocd'
       targetRevision: HEAD
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```

   Apply the ArgoCD application:

   ```bash
   kubectl apply -f argocd-app.yaml
   ```

5. **ArgoCD will now manage your deployments**, syncing your application from GitHub automatically.

### 6. (Optional) Enable Image Tag Syncing in GitHub Actions

In your GitHub Actions pipeline, you can include a step to dynamically update the image tag in `kustomization.yaml` and commit the changes to trigger ArgoCD sync.

Example GitHub Action step to update image tag:

```yaml
- name: Update kustomization.yaml
  run: |
    sed -i "s|image: your-dockerhub-username/django-app:.*|image: your-dockerhub-username/django-app:${{ github.sha }}|" k8s/kustomization.yaml
    git config --global user.email "github-actions@github.com"
    git config --global user.name "GitHub Actions"
    git commit -am "Update image tag to ${{ github.sha }} [skip ci]"
    git push
```

This will push the updated image tag to your GitHub repository, and ArgoCD will automatically deploy the new version.

## Conclusion

You have successfully set up a Django application running on Kubernetes, managed by ArgoCD for continuous delivery.

For any issues or improvements, feel free to create an issue in the GitHub repository.
