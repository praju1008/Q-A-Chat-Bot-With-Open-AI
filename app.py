import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

# Keep tracing/project metadata but don't try to overwrite unrelated env vars
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "Q&A chat bot with OPENAI")

prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps people find information."),
    ("user", "Question: {question}")
])

def generate_response(question, api_key, llm, temperature, max_tokens):
    """Generate a response using OpenAI via LangChain."""
    
    # Validate inputs
    if not api_key or not api_key.strip():
        raise ValueError("API key is empty. Provide a valid OpenAI API key.")
    
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Set the API key in environment so ChatOpenAI can find it
    os.environ["OPENAI_API_KEY"] = api_key.strip()

    # Create the LLM with the specified model and temperature
    try:
        llm_client = ChatOpenAI(model=llm, temperature=temperature, timeout=30)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}") from e

    output_parser = StrOutputParser()
    chain = prompt | llm_client | output_parser

    # Try invoking with retry logic for rate-limits and transient errors
    max_retries = 3
    backoff = 1
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            answer = chain.invoke({"question": question})
            return answer

        except Exception as e:
            last_error = e
            err_str = str(e).lower()

            # Quota/billing issues (not retriable)
            if "insufficient_quota" in err_str or ("quota" in err_str and "exceeded" in err_str):
                # Attempt to fallback to a cheaper model once (gpt-3.5-turbo)
                if llm != "gpt-3.5-turbo":
                    try:
                        fallback_model = "gpt-3.5-turbo"
                        fallback_client = ChatOpenAI(model=fallback_model, temperature=temperature, timeout=30)
                        fallback_chain = prompt | fallback_client | output_parser
                        answer = fallback_chain.invoke({"question": question})
                        # Append a small note so the user knows a fallback was used
                        try:
                            return answer + "\n\n(Note: response generated using fallback model gpt-3.5-turbo due to quota limits.)"
                        except Exception:
                            return answer
                    except Exception:
                        # Fallback failed; continue to raise original quota error below
                        pass

                raise RuntimeError(
                    "insufficient_quota: Your OpenAI account has reached its quota. "
                    "Check billing at https://platform.openai.com/account/billing/overview"
                ) from e

            # Rate limit (retriable with backoff)
            if "error code: 429" in err_str or "rate_limit" in err_str or "rate limit" in err_str:
                if attempt == max_retries:
                    raise RuntimeError(
                        "Rate limit exceeded after retries. Try again in a few moments."
                    ) from e
                time.sleep(backoff)
                backoff *= 2
                continue

            # Authentication issues (not retriable)
            if "invalid_api_key" in err_str or "authentication" in err_str or "unauthorized" in err_str:
                raise RuntimeError(
                    "invalid_api_key: The API key provided is invalid or expired. "
                    "Get a new key from https://platform.openai.com/account/api-keys"
                ) from e

            # Model not found (not retriable)
            if "model_not_found" in err_str or "does not exist" in err_str:
                raise RuntimeError(
                    f"Model error: The selected model '{llm}' is not available or not found. "
                    "Try a different model."
                ) from e

            # Timeout (retriable)
            if "timeout" in err_str or "timed out" in err_str:
                if attempt == max_retries:
                    raise RuntimeError(
                        "Request timed out after retries. Try again or reduce Max Tokens."
                    ) from e
                time.sleep(backoff)
                backoff *= 2
                continue

            # Generic OpenAI API error
            raise RuntimeError(f"OpenAI API error: {str(e)}") from e

    # Fallback (should not reach here)
    if last_error:
        raise RuntimeError(f"Failed after {max_retries} attempts: {str(last_error)}") from last_error


st.title("Q&A Chat Bot with OPENAI")

st.sidebar.title("⚙️ Settings")

# Try to get API key from environment or sidebar
env_key = os.getenv("OPENAI_API_KEY", "").strip()
api_key = st.sidebar.text_input(
    "Enter your OPENAI API Key",
    value=env_key if env_key else "",
    type="password",
    help="Get your key from https://platform.openai.com/account/api-keys"
)

llm = st.sidebar.selectbox(
    "Select openAI Model",
    ("gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4"),
    help="gpt-3.5-turbo is fastest and cheapest; gpt-4o is more capable"
)

temperature = st.sidebar.slider(
    "Select Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    help="Lower = deterministic, Higher = creative"
)

max_tokens = st.sidebar.slider(
    "Select Max Tokens",
    min_value=50,
    max_value=300,
    value=150,
    help="Max words in response (~4 chars per token)"
)

# Show setup guidance if no key present
if not api_key and not env_key:
    st.warning(
        "🔑 **No OpenAI API key found!**\n\n"
        "**Options:**\n"
        "1. **Paste your key** in the sidebar (top-left) → 'Enter your OPENAI API Key'\n"
        "2. **Set environment variable** (Windows PowerShell):\n"
        "   ```\n"
        "   setx OPENAI_API_KEY \"sk-your-key-here\"\n"
        "   ```\n"
        "   Then restart PowerShell.\n\n"
        "**Get your key:** https://platform.openai.com/account/api-keys\n\n"
        "**Check your quota:** https://platform.openai.com/account/billing/usage"
    )
    st.stop()

# Show quota/billing reminder
st.sidebar.markdown("---")
st.sidebar.markdown(
    "📊 [Check Quota & Billing](https://platform.openai.com/account/billing/usage)"
)

st.write("Ask any question and get answers using OPENAI models.")
user_input = st.text_input("Your Question:", placeholder="e.g., What is machine learning?")

if user_input:
    try:
        with st.spinner("Generating response..."):
            response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.success("✅ Response generated!")
        st.write(response)
    except ValueError as e:
        st.error(f"⚠️ Input Error: {e}")
    except RuntimeError as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg.lower():
            st.error(
                f"💳 **{error_msg}**\n\n"
                "**Solutions:**\n"
                "1. Add a payment method at https://platform.openai.com/account/billing/overview\n"
                "2. Check for overage limits at https://platform.openai.com/account/billing/usage\n"
                "3. Try a different API key (different organization)\n"
                "4. Use a cheaper model like `gpt-3.5-turbo`"
            )
        else:
            st.error(f"❌ Error: {error_msg}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
else:
    st.info("👉 Enter a question above to get started.")
