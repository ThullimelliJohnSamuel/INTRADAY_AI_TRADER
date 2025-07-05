import os
import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Create folders for each class
os.makedirs("dataset/buy", exist_ok=True)
os.makedirs("dataset/sell", exist_ok=True)
os.makedirs("dataset/hold", exist_ok=True)

# Generate fake price data
def generate_fake_data(trend="buy"):
    base = 100
    if trend == "buy":
        prices = [base + i + random.uniform(-1, 1) for i in range(30)]
    elif trend == "sell":
        prices = [base - i + random.uniform(-1, 1) for i in range(30)]
    else:
        prices = [base + random.uniform(-2, 2) for _ in range(30)]

    dates = [datetime.now() - timedelta(minutes=5 * i) for i in range(30)][::-1]
    df = pd.DataFrame({"Date": dates, "Close": prices})
    return df

# Save line chart image
def save_chart(df, label, idx):
    plt.figure(figsize=(5, 3))
    plt.plot(df['Date'], df['Close'], color='black')  # ✅ fixed
    plt.title(label)
    plt.xticks([]); plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"dataset/{label}/{label}_{idx}.png")
    plt.close()

# Generate 100 samples per class
for label in ["buy", "sell", "hold"]:
    for i in range(100):
        df = generate_fake_data(trend=label)
        save_chart(df, label, i)

print("✅ Dataset generation complete.")