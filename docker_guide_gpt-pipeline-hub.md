# 🐳 Docker & Deployment Guide – gpt-pipeline-hub

## 📦 Container Build & Push Workflow

Dieses Projekt nutzt ein Docker-Image, das in AWS Elastic Container Registry (ECR) gepusht und via App Runner deployed wird.

---

## 🔧 Voraussetzungen

- AWS CLI konfiguriert (`aws configure`)
- ECR-Login durchgeführt
- Repository: `145023107911.dkr.ecr.us-east-1.amazonaws.com/gpt-pipeline-hub`
- Docker installiert

---

## 📁 Projektstruktur (wichtig für Docker-Kontext)

Stelle sicher, dass folgende Verzeichnisse **im Build-Kontext** liegen:
```
/app
├── main.py
├── upload_routes.py
├── templates/       ← wichtig für HTML!
├── static/          ← (optional)
├── prompts/
├── evals/
└── Dockerfile
```

---

## 🚀 Docker Befehle (Build → Push → Deploy)

### 1. Build lokal erzeugen

```bash
docker build -t gpt-pipeline-hub:late .
```

### 2. Tagging für AWS ECR

```bash
docker tag gpt-pipeline-hub:late 145023107911.dkr.ecr.us-east-1.amazonaws.com/gpt-pipeline-hub:late
```

### 3. Bei ECR einloggen

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 145023107911.dkr.ecr.us-east-1.amazonaws.com
```

### 4. Image pushen

```bash
docker push 145023107911.dkr.ecr.us-east-1.amazonaws.com/gpt-pipeline-hub:late
```

---

## 🧪 Lokale Tests (optional)

```bash
docker run -p 8080:8080 gpt-pipeline-hub:late
```

Dann aufrufen: [http://localhost:8080](http://localhost:8080)

---

## 🛠️ Nach Push: App Runner aktualisiert automatisch (wenn verbunden)

Stelle sicher:
- App Runner ist mit dem richtigen ECR-Image verlinkt
- Deployment-Trigger: *"Automatically deploy latest image on push"*

---

## 📁 Ergebnis

Nach erfolgreichem Push kannst du dein Dashboard unter folgendem Link prüfen:

```
https://kuupjj6exw.us-east-1.awsapprunner.com
```

---

## 🧼 Cleanup (lokale Images)

```bash
docker image rm gpt-pipeline-hub:late
```

---

## 📌 Hinweis

Wenn sich `index.html` oder Templates ändern, **muss immer ein neuer Build gemacht und gepusht werden** – sonst bleibt die UI alt.

```
docker build ... && docker push ...
```