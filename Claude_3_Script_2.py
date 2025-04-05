import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import anthropic
import os
from statistics import median

# User-defined variables
CSV_LOCATION = "C:\\Users\\bandg\\Downloads\\Iron_Industry_Sales_Data.csv"  # Path to your CSV file
ANTHROPIC_API_KEY = os.environ.get("DEMO_KEY")  # Your Anthropic API key from environment variables

def load_data(file_path):
    """Load CSV data from the specified file path."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        exit(1)

def select_product(df):
    """Let the user select a product column to analyze."""
    # Get columns excluding the quarter column
    columns = [col for col in df.columns if col.lower() != 'quarter']
    
    if not columns:
        print("Error: No product columns found in CSV.")
        exit(1)
    
    print("\nAvailable products:")
    for i, col in enumerate(columns, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            selection = int(input("\nEnter the number of the product to analyze: "))
            if 1 <= selection <= len(columns):
                return columns[selection-1]
            else:
                print(f"Please enter a number between 1 and {len(columns)}.")
        except ValueError:
            print("Please enter a valid number.")

def analyze_product(df, product_col):
    """Analyze the selected product's quarterly sales."""
    # Ensure 'quarter' column exists
    quarter_col = next((col for col in df.columns if col.lower() == 'quarter'), None)
    if not quarter_col:
        print("Error: 'Quarter' column not found in CSV.")
        exit(1)
    
    # Calculate statistics
    min_value = df[product_col].min()
    min_quarter = df.loc[df[product_col] == min_value, quarter_col].iloc[0]
    
    max_value = df[product_col].max()
    max_quarter = df.loc[df[product_col] == max_value, quarter_col].iloc[0]
    
    median_value = median(df[product_col])
    # Find the quarter(s) closest to the median
    closest_to_median = df.iloc[(df[product_col] - median_value).abs().argsort()[0]]
    median_quarter = closest_to_median[quarter_col]
    
    stats = {
        "product": product_col,
        "min_value": min_value,
        "min_quarter": min_quarter,
        "max_value": max_value,
        "max_quarter": max_quarter,
        "median_value": median_value,
        "median_quarter": median_quarter
    }
    
    return stats

def plot_sales(df, product_col):
    """Create a bar chart of the selected product's quarterly sales."""
    quarter_col = next((col for col in df.columns if col.lower() == 'quarter'), None)
    
    plt.figure(figsize=(10, 6))
    plt.bar(df[quarter_col], df[product_col], color='skyblue')
    plt.title(f'Quarterly Sales for {product_col}')
    plt.xlabel('Quarter')
    plt.ylabel('Units Sold')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of bars
    for i, value in enumerate(df[product_col]):
        plt.text(i, value + (max(df[product_col]) * 0.02), str(value), 
                 ha='center', va='bottom', fontweight='bold', rotation=90)
    
    plt.tight_layout()
    plt.show()

def ask_claude(df, stats):
    """Query Claude 3.7 with the data and statistics."""
    if not ANTHROPIC_API_KEY:
        print("Error: Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
        return
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Prepare data context
    csv_content = df.to_csv(index=False)
    stats_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
    
    # Get user's question for Claude
    print("\nWhat would you like to ask Claude about this data?")
    user_question = input("> ")
    
    # Construct the message for Claude
    system_prompt = """You are analyzing quarterly sales data. 
    The user has provided a CSV file of quarterly product sales and some basic statistics.
    Analyze the data to provide insights and answer the user's question.
    If appropriate, suggest actions based on the trends you observe.
    """
    
    user_message = f"""
    Here is the quarterly sales data:
    
    {csv_content}
    
    Here are the basic statistics for {stats['product']}:
    {stats_text}
    
    My question is: {user_question}
    """
    
    print("\nQuerying Claude 3.7, please wait...")
    
    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            system=system_prompt,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        print("\nClaude's Response:")
        print(message.content[0].text)
        
    except Exception as e:
        print(f"Error querying Claude: {e}")

def main():
    print("Quarterly Sales Data Analysis")
    print("============================")
    
    # Load data
    print(f"Loading data from {CSV_LOCATION}...")
    df = load_data(CSV_LOCATION)
    
    # Display basic info
    print(f"\nData loaded successfully. Found {len(df)} rows and {len(df.columns)} columns.")
    print("Column names:", ", ".join(df.columns))
    
    # Select product to analyze
    product_col = select_product(df)
    print(f"\nAnalyzing sales for: {product_col}")
    
    # Analyze the selected product
    stats = analyze_product(df, product_col)
    
    # Display statistics
    print("\nAnalysis Results:")
    print(f"Minimum sales: {stats['min_value']} units in {stats['min_quarter']}")
    print(f"Maximum sales: {stats['max_value']} units in {stats['max_quarter']}")
    print(f"Median sales: {stats['median_value']} units (closest in {stats['median_quarter']})")
    
    # Plot the data
    plot_sales(df, product_col)
    
    # Ask Claude for further analysis
    ask_claude(df, stats)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()