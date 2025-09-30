Orders API
PARt 1 & PART 2
1. A minimal Flask + SQLAlchemy Orders API with:
   /orders API for creating and retrieving orders
   /health endpoint for health checks
   /metrics endpoint for Prometheus metrics
   Simple UI to view and create orders
   CI/CD with linting, tests, Docker builds
   Deployment to Kubernetes with Prometheus + Grafana monitoring

2. Local Setup
   Prerequisites
     Python 3.11+
     pip / venv
     Docker (for Postgres & container builds)

3. Run Locally (SQLite)
    pip install -r requirements.txt
    python app.py
    App runs on http://127.0.0.1:5000

4. Testing and Linting
   Run Unit + Integration Tests
   Run Linting
   flake8 .

5. I created the CI using Github action path .github/workflows/ci.yml
   Pipeline ncludes:
   Linting
   Unit and Integration test(Pytest + Coverage)
   Docker build( multi stage, non-root user)
   Push to the DockerHub with tags using github action secrets


PART 3 & PART 4


1. Run Locally (Postgres via Docker)
2. Export DB connection string:
   export DATABASE_URL="postgresql://orders:orderspass@localhost:5432/ordersdb"
    python app.py 
3. Installed the Kind clusters locally
4. Installed Ingress controller
5. Created Manifest file for kubernets deployment
    deployment.yaml 
    service.yaml
    Ingress.yaml
    secrets.yaml ( To store db secrets)

4. Deployed manifest using Terraform 
    main.tf - Created the resource of every object using in k8s cluster

5. for Monitoring install Helm charts of prometheus, Grafan and Loki.
   Confuigure Data souce in Grafana of Promotheus and Loki
   Add app Prometheus client and metrics expoter in app.py( application code)
   Deployed Manifest file of service monitring  - orders-api-servicemonitor.yml
   and also created prometheous alert using manifest file - orders-api-alerts.yaml



