import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF
import datetime

# Load Groq API key
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Load product data
with open("product_data.json") as f:
    products = json.load(f)

# Filter products
def filter_products(category, min_price=0, max_price=9999):
    filtered = [p for p in products if category.lower() in p["category"].lower()]
    filtered = [
        p for p in filtered
        if min_price <= int(p["price"].replace("$", "")) <= max_price
    ]
    return filtered

# Get LLM summary
def get_llm_summary(reviews):
    prompt = f"""
You are a helpful e-commerce assistant. Analyze the following product reviews and return:

- 🔼 Pros (as a bullet list)
- 🔽 Cons (as a bullet list)
- 🧠 Verdict: One-line buying advice for shoppers

Reviews: {reviews}
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Export summary to PDF
def export_summary_to_pdf(category, min_price, max_price, summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ShopGPT AI Summary", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Category: {category}", ln=True)
    pdf.cell(0, 10, f"Price Range: ${min_price} - ${max_price}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 10, summary_text)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ShopGPT_Summary_{timestamp}.pdf"
    pdf.output(filename)
    return filename

# UI
st.set_page_config(page_title="ShopGPT Pro", page_icon="🛍️")
st.title("🛍️ ShopGPT Pro – AI-Powered Product Advisor")

category = st.selectbox("Choose a product category", sorted(list(set(p["category"] for p in products))))

col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("Min Price ($)", min_value=0, value=0)
with col2:
    max_price = st.number_input("Max Price ($)", min_value=1, value=500)

# Run filtering and summary
if st.button("Show Products"):
    matches = filter_products(category, min_price, max_price)
    if not matches:
        st.warning("No matching products found.")
    else:
        all_reviews = []
        for i, p in enumerate(matches, 1):
            st.subheader(f"{i}. {p['product_name']}")
            st.write(f"💲 Price: {p['price']}")
            st.write("📝 Reviews:")
            for r in p["reviews"]:
                st.markdown(f"- {r}")
                all_reviews.append(r)

        st.markdown("---")
        st.subheader("🤖 AI Summary & Buying Advice")
        with st.spinner("Generating summary using Groq AI..."):
            summary = get_llm_summary(all_reviews)
        st.success("AI Summary generated!")
        st.write(summary)

        if st.button("Download Summary as PDF"):
            file_path = export_summary_to_pdf(category, min_price, max_price, summary)
            st.success(f"✅ PDF saved as: {file_path}")
