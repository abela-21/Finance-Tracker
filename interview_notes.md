# Interview Talking Points: MCI Application

### How the Application Meets the Job Requirements

This application is a tailored demonstration of the key skills required for the Investor Relations Analyst role at Befesa.

1.  **Data Collection and Analysis:**
    *   The backend fetches historical stock prices and volumes using the `openbb` library, a standard tool in quantitative finance, demonstrating proficiency with financial data APIs.
    *   It calculates critical KPIs (average price, volatility, price change, average volume, and Sharpe ratio), which are fundamental metrics for assessing stock performance and risk.

2.  **Market and Competitive Research:**
    *   The core feature is the competitive analysis, allowing a direct comparison of Befesa (e.g., `BEF.SG`) against its competitors (e.g., `AUR.AX`).
    *   The benchmark table provides a clear, at-a-glance view of how the tickers stack up against each other, which is crucial for competitive positioning.

3.  **Tracking Key Performance Indicators (KPIs):**
    *   The application is built around tracking the exact KPIs that an analyst would monitor. The backend calculates them, and both the HTML report and the dashboard visualize them, showing an understanding of what drives investor perception.

4.  **Stock Price and Investor Sentiment Analysis:**
    *   It analyzes stock price trends visually through an interactive Plotly chart, an industry-standard visualization library.
    *   Sentiment analysis is performed on news headlines and simulated X posts using a Hugging Face transformer model. This showcases an ability to leverage modern AI techniques to gauge market sentiment, a key part of understanding investor perspectives.

5.  **Creating Investor-Ready Outputs:**
    *   The application generates a clean, professional HTML report inspired by Inverno's minimalist design. This report is a tangible output that could be shared with management or used in presentations.
    *   The Streamlit dashboard provides an interactive, user-friendly interface for real-time analysis, demonstrating skills in creating internal decision-making tools.

### Highlighting Technical Proficiency

*   **OpenBB Terminal Inspiration:** "I chose to build the data fetching component inspired by the **OpenBB Terminal** because it is a powerful, open-source platform widely respected in the finance community. Using the `openbb` library shows that I am comfortable with professional-grade financial data tools and can integrate them into custom workflows."

*   **Inverno-Inspired Reporting:** "For the reporting, I drew inspiration from **Inverno's** lightweight and clean HTML reporting. In an analyst role, clarity and conciseness are key. This approach avoids bloated PDFs and delivers information in a universally accessible format, demonstrating an understanding of effective communication."

*   **Hugging Face for AI-Powered Insights:** "To go beyond simple quantitative data, I integrated a **Hugging Face transformer model** for sentiment analysis. This shows my ability to apply cutting-edge AI to financial analysis, providing deeper insights into market and investor sentiment that are not immediately apparent from price charts alone."

*   **Modern Tech Stack (FastAPI & Streamlit):** "The choice of **FastAPI** for the backend ensures a high-performance, scalable API, while **Streamlit** allows for the rapid development of interactive data applications. This demonstrates proficiency in modern Python frameworks relevant to building data-centric tools."

By presenting this application, I am not just showing that I can code; I am demonstrating that I understand the specific needs of an Investor Relations Analyst and can build targeted, effective tools to meet those needs.
