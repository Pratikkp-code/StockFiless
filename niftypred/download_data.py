#!/usr/bin/env python3
"""
Data Download Script for NIFTY Prediction Project
Downloads additional stock market data for enhanced model training
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import time

def download_nifty_data():
    """Download NIFTY 50 data"""
    print("Downloading NIFTY 50 data...")
    
    try:
        # Download NIFTY 50 data for the last 5 years
        start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        nifty = yf.download('^NSEI', start=start_date, end=end_date, progress=False)
        
        if not nifty.empty:
            # Save to CSV
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            output_path = os.path.join(data_dir, 'NIFTY50_yfinance.csv')
            nifty.to_csv(output_path)
            print(f"✅ Downloaded {len(nifty)} records to {output_path}")
            return True
        else:
            print("❌ Failed to download NIFTY 50 data")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading NIFTY 50 data: {e}")
        return False

def download_bank_nifty_data():
    """Download Bank NIFTY data"""
    print("Downloading Bank NIFTY data...")
    
    try:
        start_date = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        bank_nifty = yf.download('^NSEBANK', start=start_date, end=end_date, progress=False)
        
        if not bank_nifty.empty:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            output_path = os.path.join(data_dir, 'BANKNIFTY_yfinance.csv')
            bank_nifty.to_csv(output_path)
            print(f"✅ Downloaded {len(bank_nifty)} records to {output_path}")
            return True
        else:
            print("❌ Failed to download Bank NIFTY data")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading Bank NIFTY data: {e}")
        return False

def download_top_stocks():
    """Download top NIFTY 50 stocks data"""
    print("Downloading top NIFTY 50 stocks data...")
    
    # Top 10 NIFTY 50 stocks by market cap
    top_stocks = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'AXISBANK.NS'
    ]
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    successful_downloads = 0
    
    for stock in top_stocks:
        try:
            print(f"  Downloading {stock}...")
            stock_data = yf.download(stock, start=start_date, end=end_date, progress=False)
            
            if not stock_data.empty:
                output_path = os.path.join(data_dir, f'{stock.replace(".NS", "")}_yfinance.csv')
                stock_data.to_csv(output_path)
                successful_downloads += 1
                print(f"    ✅ Downloaded {len(stock_data)} records")
            else:
                print(f"    ❌ No data for {stock}")
                
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ❌ Error downloading {stock}: {e}")
    
    print(f"✅ Successfully downloaded {successful_downloads}/{len(top_stocks)} stocks")
    return successful_downloads > 0

def download_global_indices():
    """Download global market indices for correlation analysis"""
    print("Downloading global market indices...")
    
    global_indices = {
        '^GSPC': 'SP500',      # S&P 500
        '^DJI': 'DOW',         # Dow Jones
        '^IXIC': 'NASDAQ',     # NASDAQ
        '^FTSE': 'FTSE100',    # FTSE 100
        '^N225': 'NIKKEI',     # Nikkei 225
        '^HSI': 'HANG_SENG'    # Hang Seng
    }
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    successful_downloads = 0
    
    for symbol, name in global_indices.items():
        try:
            print(f"  Downloading {name} ({symbol})...")
            index_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if not index_data.empty:
                output_path = os.path.join(data_dir, f'{name}_yfinance.csv')
                index_data.to_csv(output_path)
                successful_downloads += 1
                print(f"    ✅ Downloaded {len(index_data)} records")
            else:
                print(f"    ❌ No data for {name}")
                
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ❌ Error downloading {name}: {e}")
    
    print(f"✅ Successfully downloaded {successful_downloads}/{len(global_indices)} indices")
    return successful_downloads > 0

def create_data_summary():
    """Create a summary of all downloaded data"""
    print("\n📊 Creating data summary...")
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    if not os.path.exists(data_dir):
        print("❌ Data directory not found")
        return
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in data directory")
        return
    
    summary = []
    
    for csv_file in csv_files:
        try:
            file_path = os.path.join(data_dir, csv_file)
            df = pd.read_csv(file_path)
            
            # Get basic info
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            date_range = f"{df.index[0]} to {df.index[-1]}" if len(df) > 0 else "No data"
            
            summary.append({
                'File': csv_file,
                'Records': len(df),
                'Columns': len(df.columns),
                'Size (MB)': round(file_size, 2),
                'Date Range': date_range
            })
            
        except Exception as e:
            summary.append({
                'File': csv_file,
                'Records': 'Error',
                'Columns': 'Error',
                'Size (MB)': 'Error',
                'Date Range': str(e)
            })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary)
    
    # Save summary
    summary_path = os.path.join(data_dir, 'data_summary.csv')
    summary_df.to_csv(summary_path, index=False)
    
    print(f"✅ Data summary saved to {summary_path}")
    print("\n📋 Data Summary:")
    print(summary_df.to_string(index=False))

def main():
    """Main function to download all data"""
    print("🚀 Starting data download for NIFTY Prediction Project...")
    print("=" * 60)
    
    # Download different types of data
    downloads = [
        ("NIFTY 50", download_nifty_data),
        ("Bank NIFTY", download_bank_nifty_data),
        ("Top Stocks", download_top_stocks),
        ("Global Indices", download_global_indices)
    ]
    
    successful_downloads = 0
    
    for name, download_func in downloads:
        print(f"\n📥 {name}")
        print("-" * 40)
        
        if download_func():
            successful_downloads += 1
        
        print()
    
    # Create data summary
    create_data_summary()
    
    print("=" * 60)
    print(f"🎉 Download completed! {successful_downloads}/{len(downloads)} data sources successful")
    
    if successful_downloads > 0:
        print("\n💡 Next steps:")
        print("1. Start the Flask backend: python app/app.py")
        print("2. Train the model using the API")
        print("3. Make predictions with the React frontend")
    else:
        print("\n⚠️  No data was downloaded. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
