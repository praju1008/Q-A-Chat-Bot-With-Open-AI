# Quick Start

## TL;DR: 3 Steps to Run

### 1. Set API Key (pick one)

**Option A: Environment Variable (Permanent)**
```powershell
setx OPENAI_API_KEY "sk-your-key-here"
# restart PowerShell
```

**Option B: Temporary**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Option C: Paste in App**
Just enter your key in the sidebar when the app starts.

### 2. Install Dependencies
```powershell
pip install -r requirement.txt
```

### 3. Run the App
```powershell
streamlit run app.py
```

---

## Where to Get API Key
👉 https://platform.openai.com/account/api-keys

## Where to Add Payment
👉 https://platform.openai.com/account/billing/overview

## Check Your Quota/Usage
👉 https://platform.openai.com/account/billing/usage

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| **Quota exceeded** | No credits or on free tier | Add payment method |
| **invalid_api_key** | Wrong key or expired | Get fresh key from dashboard |
| **Rate limit (429)** | Too many requests | Wait a few seconds, app auto-retries |
| **No API key found** | Not set anywhere | Set env var or paste in sidebar |
| **Model not found** | Model unavailable | Pick different model from dropdown |
| **Request timed out** | Server slow | Reduce Max Tokens, try again |

---

## Cost Breakdown (approximate)

- **gpt-3.5-turbo**: $0.0005 per 1K tokens ⭐ **cheapest**
- **gpt-4o-mini**: $0.00015 per 1K tokens
- **gpt-4o**: $0.03 per 1K tokens
- **gpt-4**: $0.01+ per 1K tokens

💡 **Tip**: Reduce Max Tokens to 100-150 to save money.

---

For detailed troubleshooting, see `SETUP.md`
