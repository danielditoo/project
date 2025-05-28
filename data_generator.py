import pandas as pd
import numpy as np

def generate_laptop_data(n_samples=100):
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate dummy data
    brands = ['Lenovo', 'HP', 'Dell', 'Asus', 'Acer', 'Apple', 'MSI']
    processors = ['Intel i3', 'Intel i5', 'Intel i7', 'Intel i9', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9']
    gpu = ['Integrated', 'NVIDIA GTX 1650', 'NVIDIA RTX 3050', 'NVIDIA RTX 3060', 'AMD Radeon']
    
    data = {
        'Brand': np.random.choice(brands, n_samples),
        'Processor': np.random.choice(processors, n_samples),
        'RAM_GB': np.random.choice([4, 8, 16, 32, 64], n_samples),
        'Storage_GB': np.random.choice([256, 512, 1024, 2048], n_samples),
        'GPU': np.random.choice(gpu, n_samples),
        'Screen_Size': np.random.uniform(13, 17, n_samples).round(1),
        'Price_USD': np.zeros(n_samples)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate prices based on specifications
    base_price = 500
    for idx, row in df.iterrows():
        price = base_price
        
        # Brand premium
        brand_premium = {
            'Apple': 800,
            'Dell': 300,
            'Lenovo': 250,
            'HP': 200,
            'Asus': 200,
            'MSI': 300,
            'Acer': 150
        }
        price += brand_premium[row['Brand']]
        
        # RAM price
        price += row['RAM_GB'] * 10
        
        # Storage price
        price += (row['Storage_GB'] / 256) * 100
        
        # GPU price
        gpu_premium = {
            'Integrated': 0,
            'NVIDIA GTX 1650': 200,
            'NVIDIA RTX 3050': 400,
            'NVIDIA RTX 3060': 600,
            'AMD Radeon': 300
        }
        price += gpu_premium[row['GPU']]
        
        # Processor price
        processor_premium = {
            'Intel i3': 100,
            'Intel i5': 200,
            'Intel i7': 400,
            'Intel i9': 700,
            'AMD Ryzen 5': 250,
            'AMD Ryzen 7': 450,
            'AMD Ryzen 9': 750
        }
        price += processor_premium[row['Processor']]
        
        # Add some random variation
        price *= np.random.uniform(0.9, 1.1)
        
        df.at[idx, 'Price_USD'] = round(price, 2)
    
    return df

# Generate and save the dataset
if __name__ == "__main__":
    df = generate_laptop_data(200)
    df.to_csv("laptop_data.csv", index=False)
