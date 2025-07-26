# shopgpt_pro
 ShopGPT Pro An AI-powered product recommendation and review summarization app built with Streamlit. It filters products by category and price, then uses Groq's LLaMA 3 model to generate a smart summary of user reviews, highlighting pros, cons, and a buying verdict. PDF export included.

📁 Project Files Overview

| File Name           | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `app.py`            | Main Streamlit app that powers the UI and logic                         |
| `product_data.json` | Sample product info and customer reviews                                |
| `requirements.txt`  | List of Python libraries needed to run the app                          |
| `README.md`         | This documentation                                                      |

 # Getting Started

# Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/shopgpt_pro.git
cd shopgpt_pro

#  Install dependencies

pip install -r requirements.txt

# Set up your .env file
GROQ_API_KEY=your_groq_api_key_here

# Run the app

streamlit run app.py

# Features
 Filter products by category and price

 Summarize customer reviews using Groq’s LLaMA 3

 See pros, cons, and a one-line buying recommendation

 Download the AI summary as a PDF report

 Simple and responsive Streamlit interface


