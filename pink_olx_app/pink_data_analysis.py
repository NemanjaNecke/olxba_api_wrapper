# Data analysis functions (matplotlib, etc.)
# pink_data_analysis.py

import statistics
import matplotlib.pyplot as plt

def plot_price_distribution(listings):
    """
    Creates a simple histogram of listing prices using matplotlib.
    Returns the matplotlib Figure object.
    """
    prices = []
    for item in listings:
        try:
            p = float(item.get("price", 0) or 0)
            if p > 0:
                prices.append(p)
        except:
            pass

    if not prices:
        # Return None or an empty figure if no valid prices
        fig = plt.figure()
        plt.title("No valid prices to plot")
        return fig

    fig = plt.figure()
    plt.hist(prices, bins=10, color='pink', edgecolor='red')
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")

    # Stats in text
    min_p = min(prices)
    max_p = max(prices)
    avg_p = statistics.mean(prices)
    text_str = f"Count: {len(prices)}\nMin: {min_p}\nMax: {max_p}\nAvg: {avg_p:.2f}"
    plt.text(0.95, 0.95, text_str, transform=plt.gca().transAxes,
             ha='right', va='top', bbox=dict(boxstyle="round", fc="white", alpha=0.8))

    return fig
