# Q&A Chat Bot Setup Guide

## ✅ Prerequisites
- Python 3.8+
- OpenAI account with active API key and billing

## 📋 Step 1: Install Dependencies

```powershell
cd "D:\Gen Ai Course\Classes\Project\Q&A chat bot"
pip install -r requirement.txt
```

If you don't have a `requirement.txt`, create one:
```
streamlit>=1.28.0
langchain>=0.1.0
langchain-openai>=0.0.1
python-dotenv>=1.0.0
```

## 🔑 Step 2: Get Your OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Click **"Create new secret key"**
3. Copy the key (starts with `sk-`)
4. **Save it somewhere secure** (you won't see it again)

## 🚀 Step 3: Set Up API Key

### Option A: Environment Variable (Recommended for Development)

**Temporary (current PowerShell session only):**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
streamlit run app.py
```

**Permanent (all future PowerShell sessions):**
```powershell
setx OPENAI_API_KEY "sk-your-actual-key-here"
```
Then close and reopen PowerShell.

### Option B: Sidebar Input (No Setup Required)
Just paste your key directly into the sidebar input when the app runs.

### Option C: `.env` File
Create a `.env` file in the project folder:
```
OPENAI_API_KEY=sk-your-actual-key-here
```
The app will load it automatically via `python-dotenv`.

## 🎯 Step 4: Run the App

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ⚠️ Troubleshooting

### ❌ Error: "Quota exceeded"
- **Cause**: Your OpenAI account has no credits or is on the free tier.
- **Fix**:
  1. Go to https://platform.openai.com/account/billing/overview
  2. Add a payment method
  3. Check your usage at https://platform.openai.com/account/billing/usage
  4. Try a cheaper model: `gpt-3.5-turbo`

### ❌ Error: "invalid_api_key"
- **Cause**: API key is wrong, expired, or typo.
- **Fix**:
  1. Get a fresh key from https://platform.openai.com/account/api-keys
  2. Double-check there are no extra spaces before/after the key
  3. Make sure it starts with `sk-`

### ❌ Error: "Rate limit exceeded (429)"
- **Cause**: Too many requests too fast.
- **Fix**: Wait a few seconds and try again. The app will auto-retry.

### ❌ Error: "Model not found"
- **Cause**: Model doesn't exist or you don't have access.
- **Fix**: Select a different model from the sidebar (e.g., `gpt-3.5-turbo`)

### ❌ Error: "Request timed out"
- **Cause**: OpenAI servers slow or network issue.
- **Fix**:
  1. Reduce Max Tokens to 100-150
  2. Try a simpler question
  3. Wait and retry

### ❌ Error: "API key not found"
- **Cause**: Environment variable not set and sidebar empty.
- **Fix**:
  1. Set `OPENAI_API_KEY` environment variable (see Step 2)
  2. Or paste your key in the sidebar
  3. Or create a `.env` file

---

## 📊 Monitor Your Usage

- **Real-time usage**: https://platform.openai.com/account/usage
- **Billing & limits**: https://platform.openai.com/account/billing/overview
- **API keys**: https://platform.openai.com/account/api-keys

---

## 💰 Cost Tips

- **gpt-3.5-turbo**: ~$0.0005 per 1K tokens (fastest, cheapest)
- **gpt-4o-mini**: ~$0.00015 per 1K tokens (good balance)
- **gpt-4o**: ~$0.03 per 1K tokens (best quality)
- **gpt-4**: ~$0.01+ per 1K tokens (very capable)

Reduce Max Tokens to save money. Start with 100-150 tokens.

---

## ✨ Tips for Best Results

1. **Be specific**: Ask clear, detailed questions
2. **Adjust temperature**: 
   - Lower (0.0-0.3) for factual/deterministic answers
   - Higher (0.7-1.0) for creative answers
3. **Reduce tokens** if you're hitting quota limits
4. **Check billing regularly** to avoid surprises

---

## 📞 Need Help?

- OpenAI Docs: https://platform.openai.com/docs
- API Status: https://status.openai.com
- Community: https://community.openai.com
