# Setup and Execution Instructions

## 1. Install Dependencies
Ensure you have Python 3.12 installed. Then, install the required packages using pip:
```bash
pip install -r requirements.txt
```

## 2. Configure OpenBB API Keys
The application uses the OpenBB Platform, which requires API keys for data providers like Alpha Vantage (for stock data) and NewsAPI (for news).

### Option A: Using OpenBB Hub (Recommended)
1.  Sign up for an account at [my.openbb.co](https://my.openbb.co/).
2.  On the Hub, navigate to the "Keys" section and add your API keys for **Alpha Vantage** and **NewsAPI**.
3.  Generate a Personal Access Token (PAT) from the Hub.
4.  In your Windsurf terminal, set the PAT as an environment variable:
    ```bash
    export OPENBB_HUB_PAT="your_pat_here"
    ```
    This will securely sync your keys to the environment.

### Option B: Local Configuration
If you prefer not to use the Hub, you can configure keys locally.
1.  Create the necessary directory:
    ```bash
    mkdir -p ~/.openbb_platform
    ```
2.  Create the `user_settings.json` file:
    ```bash
    touch ~/.openbb_platform/user_settings.json
    ```
3.  Add your credentials to the file in the following format:
    ```json
    {
        "credentials": {
            "alpha_vantage": {
                "api_key": "YOUR_ALPHA_VANTAGE_KEY"
            },
            "news_api": {
                "api_key": "YOUR_NEWSAPI_KEY"
            }
        }
    }
    ```

## 3. Run the Backend Server
Open a terminal in your Windsurf IDE and start the FastAPI server:
```bash
uvicorn mci_server_new:app --host 0.0.0.0 --port 8000
```
The server will be accessible at `http://127.0.0.1:8000`.

## 4. Run the Frontend Application

### Streamlit Dashboard (Primary)
Open a **new terminal** in Windsurf and run the Streamlit app:
```bash
streamlit run dashboard.py
```
The dashboard will be available at the URL provided by Streamlit (usually `http://localhost:8501`).

### Fallback HTML Dashboard
If Streamlit is not preferred or supported, you can serve the `dashboard.html` file. A simple way to do this is using Python's built-in HTTP server from the project directory:
```bash
python3 -m http.server 8001
```
Navigate to `http://localhost:8001/dashboard.html` in your browser. Note that for the API call to work from this page, you might need to handle CORS or serve it via a more robust method in a production scenario. For this demo, running both servers locally should suffice.
