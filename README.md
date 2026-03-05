# Tax Calculator — Cloud Native Final Project

A Python/Flask web application that calculates federal income tax using configurable, progressive tax brackets. The project demonstrates Cloud Native, DevOps, Agile, and NoSQL skills.

## Project Structure

```
FinalProject6/
├── app.py                        # Flask web application
├── tax_calculator/
│   ├── __init__.py
│   ├── tax.py                    # Core tax calculation logic
│   └── config.json               # Externalized tax brackets (not hard-coded)
├── templates/
│   └── index.html                # Frontend UI
├── tests/
│   ├── __init__.py
│   └── test_tax.py               # Unit tests (pytest)
├── Dockerfile                    # Multi-stage: test → production
├── .dockerignore
├── requirements.txt
├── docs/
│   └── EPIC_AND_STORIES.md       # Part A: Epic & user stories
├── .tekton/
│   ├── pipeline.yaml             # Tekton CI/CD pipeline
│   ├── tasks.yaml                # Custom Tekton tasks (lint, test, deploy)
│   └── pipeline-run.yaml         # Sample PipelineRun
└── deploy/
    └── code-engine-service.yaml  # IBM Cloud Code Engine manifest
```

## Quick Start (Local)

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## Run Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Build & Run with Docker

```bash
# Build (tests run automatically in the build stage)
docker build -t tax-calculator .

# Run
docker run -p 5000:5000 tax-calculator
```

## Deploy to IBM Cloud Code Engine

```bash
# 1. Build and push the image
docker build -t us.icr.io/<namespace>/tax-calculator:latest .
docker push us.icr.io/<namespace>/tax-calculator:latest

# 2. Deploy via Code Engine CLI
ibmcloud ce application create \
  --name tax-calculator \
  --image us.icr.io/<namespace>/tax-calculator:latest \
  --port 5000
```

## Tekton Pipeline

Apply the pipeline resources to your cluster:

```bash
kubectl apply -f .tekton/tasks.yaml
kubectl apply -f .tekton/pipeline.yaml
kubectl create -f .tekton/pipeline-run.yaml
```

The pipeline flow: **Clone → Lint → Test → Build Image → Deploy**

Deployment only proceeds when all unit tests pass.

## Configuration

Tax brackets are externalized in [`tax_calculator/config.json`](tax_calculator/config.json). You can modify rates, brackets, and the standard deduction without changing code.
