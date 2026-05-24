# Milestone 2: Salesforce Sends Incident To Zentom API

## Goal

```text
Salesforce Apex
-> External Callout
-> Zentom API
-> Incident stored in DB
-> Risk + Policy created
```

## Local API

From `services/zentom-api`:

```powershell
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Public Tunnel

Start ngrok:

```powershell
ngrok http 8000
```

Use the HTTPS forwarding URL:

```text
https://abc123.ngrok-free.app
```

## Replace Placeholder URL

Replace this placeholder in both files when a new tunnel URL is generated:

```text
https://replace-with-ngrok-url.ngrok-free.app
```

Current quick tunnel URL:

```text
https://accepted-proposals-crowd-star.trycloudflare.com
```

Files:

- `force-app/main/default/classes/ZentomIncidentClient.cls`
- `force-app/main/default/remoteSiteSettings/Zentom_API.remoteSite-meta.xml`

The final Apex endpoint must look like:

```text
https://abc123.ngrok-free.app/api/incidents/receive
```

The Remote Site URL must look like:

```text
https://abc123.ngrok-free.app
```

## Anonymous Apex Test

```apex
ZentomIncidentClient.sendIncident(
    'FLOW_FAILURE',
    'Salesforce Flow',
    'production',
    'Flow failed due to missing Account Owner'
);
```

## Expected Result

- FastAPI receives request
- Incident row is created
- Risk score row is created
- Policy decision row is created
- Policy requires human approval because environment is `production`
