# Azure AI Setup (Azure OpenAI-compatible)

This app can use any Azure-hosted chat model deployed behind an **Azure OpenAI-compatible endpoint**.

Earlier iterations of this project used **Phi** as a low-cost model, so you may still see older references. The current recommended deployment for this repo is **`gpt-5-nano`** (as configured in App Service).

## Step 1: Create Azure AI Studio Project

1. Go to https://ai.azure.com/
2. Sign in with your Azure account
3. Click **"+ New project"**
4. Fill in:
   - Project name: `triathlon-ai`
   - Resource group: `triathlon-rg` (use existing or create new)
   - Location: `Sweden Central` (or your preferred region)
5. Click **Create**

## Step 2: Deploy a Model

### Option A: Via Azure AI Studio (Recommended)

1. In your project, go to **Deployments** → **+ Deploy model** → **Deploy base model**
2. Search for your preferred model (for example: **`gpt-5-nano`**, or a Phi model)
3. Click **Deploy**
4. Configure deployment:
   - Deployment name: `gpt-5-nano` (recommended)
   - Model: match what you selected in the UI
   - Deployment type: Standard
5. Click **Deploy**
6. Wait 2-3 minutes for deployment

### Option B: Via Azure CLI

```bash
# Login to Azure
az login

# Create Azure AI Studio hub
az ml workspace create \
  --name triathlon-ai-hub \
  --resource-group triathlon-rg \
  --location swedencentral \
  --kind hub

# Deploy Phi model (this will be available soon via CLI)
```

## Step 3: Get Connection Details

After deployment completes:

1. Go to **Deployments** in Azure AI Studio
2. Click on your deployment (for example `gpt-5-nano`)
3. Copy these values:
   - **Target URI** (endpoint): `https://your-endpoint.openai.azure.com/`
   - **Deployment name**: `gpt-5-nano`

If your environment is configured like Azure AI Foundry where **API keys are disabled**, you must use **Entra ID** (Managed Identity / workload identity) instead of an API key.

## Step 4: Configure Your App

Update `.env` file:

```bash
LLM_PROVIDER=azure_ai
AZURE_AI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_AI_DEPLOYMENT_NAME=gpt-5-nano

# Auth (choose one):
# Option 1: Entra ID (recommended for App Service / Foundry)
AZURE_AI_AUTH=entra_id
# Optional: if using a *user-assigned* managed identity
# AZURE_AI_MANAGED_IDENTITY_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Option 2: API key (only if enabled for your resource)
# AZURE_AI_AUTH=api_key
# AZURE_AI_API_KEY=your_api_key_here

# API version used by the OpenAI-compatible endpoint
AZURE_AI_API_VERSION=2024-02-15-preview
DATABASE_URL=sqlite:///./workouts.db
```

## Step 5: Test Locally

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the app
python app/main.py

# Visit http://localhost:8000 and generate a program
```

## Step 6: Deploy to Azure App Service

```powershell
# Set environment variables in Azure (Entra ID / Managed Identity)
az webapp config appsettings set \
  --resource-group triathlon-rg \
  --name triathlon-program-generator \
   --settings \
      LLM_PROVIDER="azure_ai" \
      AZURE_AI_ENDPOINT="https://your-endpoint.openai.azure.com/" \
      AZURE_AI_DEPLOYMENT_NAME="gpt-5-nano" \
      AZURE_AI_AUTH="entra_id" \
      AZURE_AI_API_VERSION="2024-02-15-preview" \
      DATABASE_URL="sqlite:///./workouts.db"

# Deploy updated code
Compress-Archive -Path app,requirements.txt,startup.sh,.deployment -DestinationPath deploy.zip -Force
az webapp deployment source config-zip --resource-group triathlon-rg --name triathlon-program-generator --src deploy.zip
```

## Notes on model differences

- Some models (including parts of the GPT-5 family) may reject non-default sampling parameters (e.g. explicit `temperature`) and require `max_completion_tokens` instead of `max_tokens`.
- The app code includes compatibility handling, but if you switch models and get parameter errors, check the App Service logs.

## Troubleshooting

### Error: "Resource not found"
- Make sure deployment is complete (check Azure AI Studio → Deployments)
- Verify endpoint URL includes `/openai/` path if required
- Check deployment name matches exactly

### Error: "Authentication failed"
- If using API key auth: verify the API key is correct (regenerate if needed)
- If using Entra ID auth: ensure the App Service managed identity has RBAC on the Azure AI resource (typically **Cognitive Services OpenAI User**)

### Error: "Model not available"
- Phi models might not be available in all regions
- Try different Azure regions (Sweden Central, East US 2, UK South usually have Phi)
- Check quota limits in Azure portal

### Check Azure logs:
```powershell
az webapp log tail --resource-group triathlon-rg --name triathlon-program-generator
```

## Benefits of Using Azure AI with Phi

✅ **Cost-effective**: 10-30x cheaper than Claude  
✅ **Fast**: Optimized for Azure infrastructure  
✅ **No credit limits**: Pay-as-you-go with Azure credits  
✅ **Integrated**: Same Azure account, billing, and monitoring  
✅ **Scalable**: Auto-scales with your app  
✅ **Compliant**: Azure security and compliance features  

## Next Steps

1. Monitor usage in Azure Portal → Cost Management
2. Set up budget alerts to avoid surprises
3. Consider reserved capacity for production (additional savings)
4. Enable Application Insights for monitoring

---

**Need help?** Check Azure AI Studio documentation: https://learn.microsoft.com/azure/ai-studio/
