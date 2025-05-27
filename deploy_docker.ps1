# deploy_docker.ps1
# Build, tag, and push Docker image to AWS ECR

# Define variables
$ecrRepo = "145023107911.dkr.ecr.us-east-1.amazonaws.com/gpt-pipeline-hub"
$imageTag = "late"

# Build Docker image
Write-Host "🔨 Building Docker image..."
docker build -t gpt-pipeline-hub:$imageTag .

# Authenticate with AWS ECR
Write-Host "🔐 Logging into AWS ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ecrRepo

# Tag the image
Write-Host "🏷️ Tagging image..."
docker tag gpt-pipeline-hub:$imageTag ${ecrRepo}:$imageTag

# Push the image to ECR
Write-Host "🚀 Pushing image to ECR..."
docker push ${ecrRepo}:$imageTag

Write-Host "✅ Done!"
