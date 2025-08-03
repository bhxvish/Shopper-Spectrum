import streamlit as st
import pandas as pd
import os
import gdown

# Step 1: Download item_similarity.pkl from Google Drive using gdown
file_id = "1uGs1yBLbaFqTAmw1-uz6zztp4r17hQZP"  # Replace with your actual file ID
file_path = "item_similarity.pkl"
gdown_url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(file_path):
    try:
        st.info("Downloading item_similarity.pkl from Google Drive...")
        gdown.download(gdown_url, file_path, quiet=False)
        st.success("item_similarity.pkl downloaded successfully.")
    except Exception as e:
        st.error("Failed to download item_similarity.pkl.")
        st.stop()

# Step 2: Load pre-saved models and mapping file
try:
    item_similarity_df = pd.read_pickle(file_path)
    product_map = pd.read_csv("product_code_to_name.csv")
except Exception as e:
    st.error("Failed to load required data files.")
    st.stop()

# Step 3: Streamlit UI Configuration
st.set_page_config(page_title="Product Recommender", layout="wide")
st.sidebar.title("Shopper Spectrum")
menu = st.sidebar.radio("Navigate", ["Home", "Clustering", "Recommendation"])

# Home Page
if menu == "Home":
    st.title("Shopper Spectrum")
    st.markdown("""
        Welcome to the Customer Segmentation & Product Recommendation system.

        This app helps you:
        - Understand customer behavior using RFM clustering
        - Suggest similar products based on customer purchase patterns
    """)

# Product Recommendation Page
elif menu == "Recommendation":
    st.title("Product Recommender")
    st.markdown("Enter a product name to get similar item suggestions:")

    input_product = st.text_input("Enter Product Name", value="", key="product_input")

    if st.button("Recommend"):
        input_product = input_product.upper().strip()

        if input_product in product_map['Description'].values:
            stock_code = product_map[product_map['Description'] == input_product]['StockCode'].values[0]

            try:
                similar_codes = item_similarity_df[stock_code].sort_values(ascending=False)[1:6].index
                recommended_names = product_map[product_map['StockCode'].isin(similar_codes)]['Description'].unique()

                if len(recommended_names) > 0:
                    st.markdown("Recommended Products:")
                    for name in recommended_names:
                        st.write(f"- {name}")
                else:
                    st.warning("No recommendations found for this product.")
            except Exception as e:
                st.error("Similarity data missing for this product.")
        else:
            st.error("Product not found. Please check the spelling or use a known product name.")

# Clustering Page (Placeholder)
elif menu == "Clustering":
    st.title("Customer Clustering (Coming Soon)")
    st.info("This section will visualize customer segments based on RFM values.")
