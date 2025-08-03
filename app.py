import streamlit as st
import pandas as pd
import joblib
import os
import requests

file_url = "https://drive.google.com/uc?id=1uGs1yBLbaFqTAmw1-uz6zztp4r17hQZP"
file_path = "item_similarity.pkl"

# Download only if not present
if not os.path.exists(file_path):
    with open(file_path, "wb") as f:
        print("Downloading large model file...")
        response = requests.get(file_url)
        f.write(response.content)


# Load pre-saved models
item_similarity_df = pd.read_pickle('item_similarity.pkl')  # Product similarity matrix
product_map = pd.read_csv('product_code_to_name.csv')  # Optional: mapping StockCode → Description

# Streamlit UI Configuration
st.set_page_config(page_title="Product Recommender", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("Menu", ["Home", "Clustering", "Recommendation"])

# Home Page
if menu == "Home":
    st.title("Shopper Spectrum")
    st.markdown("Welcome to the Customer Segmentation & Product Recommendation system!")

# Recommendation Page
elif menu == "Recommendation":
    st.markdown("### **Product Recommender**")
    st.write("Enter Product Name")

    # Input box for product name
    input_product = st.text_input("Enter Product Name", value="", key="product_input")

    # Recommend button
    if st.button("Recommend"):
        # Convert to uppercase to match dataset
        input_product = input_product.upper()

        # Map product name to stock code (if using mapping CSV)
        if input_product in product_map['Description'].values:
            stock_code = product_map[product_map['Description'] == input_product]['StockCode'].values[0]

            try:
                # Get similar products
                similar_codes = item_similarity_df[stock_code].sort_values(ascending=False)[1:6].index
                recommended_names = product_map[product_map['StockCode'].isin(similar_codes)]['Description'].unique()

                st.markdown("#### Recommended Products:")
                for name in recommended_names:
                    st.write(f"- {name}")
            except Exception as e:
                st.error("Product found in list, but similarity data is missing.")
        else:
            st.error("Product not found. Please check the spelling or use a known product name.")

# Clustering Page (placeholder)
elif menu == "Clustering":
    st.markdown("### Clustering")
    st.write("This section is under development or handles RFM-based customer segmentation.")
