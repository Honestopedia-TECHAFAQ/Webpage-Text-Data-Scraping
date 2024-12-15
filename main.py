import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = []
        for product in soup.find_all('div', class_='product-item'):
            sku = product.get('data-sku')
            title = product.find('h2', class_='product-title').text.strip()
            price = product.find('span', class_='product-price').text.strip()
            product_url = product.find('a')['href']
            data.append([sku, title, price, product_url])

        return data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Web Scraping App for Online Retail Store")
    url = st.text_input("Enter the URL of the landing page with items on sale:")
    site_url = st.text_input("Enter the URL of the entire site:")
    download_all = st.button("Scrape All Items on Sale")
    download_site = st.button("Scrape Entire Site")

    if download_all and url:
        data = scrape_data(url)
        if data:
            df = pd.DataFrame(data, columns=["SKU", "Product Name", "Price", "Product URL"])
            st.download_button(label="Download All Items on Sale", data=df.to_csv(index=False).encode('utf-8'), file_name='items_on_sale.csv', mime='text/csv')

    if download_site and site_url:
        data = scrape_data(site_url)
        if data:
            df = pd.DataFrame(data, columns=["SKU", "Product Name", "Price", "Product URL"])
            st.download_button(label="Download Entire Site Data", data=df.to_csv(index=False).encode('utf-8'), file_name='entire_site.csv', mime='text/csv')

if __name__ == "__main__":
    main()
