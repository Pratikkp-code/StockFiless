from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta
import yfinance as yf
import requests
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, max_error
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Flatten, TimeDistributed, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import L1, L2
from tensorflow.keras.metrics import RootMeanSquaredError
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Global variables
model = None
scaler = None
sequence_length = 100  # Changed to match notebook
model_performance = {}

def calculate_technical_indicators(data):
    """Calculate various technical indicators based on notebook approach"""
    indicators = {}
    
    if 'Close' in data.columns:
        close = data['Close']
        high = data['High'] if 'High' in data.columns else close
        low = data['Low'] if 'Low' in data.columns else close
        volume = data['Volume'] if 'Volume' in data.columns else None
        
        # Moving averages (from notebook)
        ma_days = [10, 50, 100]
        for ma in ma_days:
            column_name = f"MA_{ma}_days"
            indicators[column_name] = close.rolling(window=ma).mean().tolist()
        
        # Enhanced moving averages
        indicators['SMA_20'] = close.rolling(window=20).mean().tolist()
        indicators['SMA_50'] = close.rolling(window=50).mean().tolist()
        indicators['EMA_12'] = close.ewm(span=12).mean().tolist()
        indicators['EMA_26'] = close.ewm(span=26).mean().tolist()
        
        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        indicators['MACD'] = (ema12 - ema26).tolist()
        indicators['MACD_Signal'] = (ema12 - ema26).ewm(span=9).mean().tolist()
        indicators['MACD_Histogram'] = ((ema12 - ema26) - (ema12 - ema26).ewm(span=9).mean()).tolist()
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['RSI'] = (100 - (100 / (1 + rs))).tolist()
        
        # Bollinger Bands
        sma20 = close.rolling(window=20).mean()
        std20 = close.rolling(window=20).std()
        indicators['BB_Upper'] = (sma20 + (std20 * 2)).tolist()
        indicators['BB_Lower'] = (sma20 - (std20 * 2)).tolist()
        indicators['BB_Middle'] = sma20.tolist()
        indicators['BB_Width'] = ((sma20 + (std20 * 2)) - (sma20 - (std20 * 2))).tolist()
        
        # Volume indicators
        if volume is not None:
            indicators['Volume_SMA'] = volume.rolling(window=20).mean().tolist()
            indicators['Volume'] = volume.tolist()
            indicators['Volume_Ratio'] = (volume / volume.rolling(window=20).mean()).tolist()
        
        # Price change percentages (from notebook)
        indicators['Daily_Return'] = close.pct_change().tolist()
        indicators['Cumulative_Return'] = ((close / close.iloc[0]) - 1).tolist()
        
        # Additional indicators from notebook
        indicators['Price_Change'] = close.diff().tolist()
        indicators['Price_Change_Pct'] = (close.diff() / close.shift(1) * 100).tolist()
        
        # Volatility indicators
        indicators['Volatility_20'] = close.rolling(window=20).std().tolist()
        indicators['Volatility_50'] = close.rolling(window=50).std().tolist()
        
    return indicators

def create_advanced_cnn_lstm_model(input_shape):
    """Create advanced CNN-LSTM model based on notebook architecture"""
    model = Sequential()
    
    # CNN layers with TimeDistributed (from notebook)
    model.add(TimeDistributed(Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape)))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Conv1D(128, kernel_size=3, activation='relu')))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Conv1D(64, kernel_size=3, activation='relu')))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Flatten()))
    
    # LSTM layers (from notebook)
    model.add(Bidirectional(LSTM(100, return_sequences=True)))
    model.add(Dropout(0.5))
    model.add(Bidirectional(LSTM(100, return_sequences=False)))
    model.add(Dropout(0.5))
    
    # Final layers
    model.add(Dense(1, activation='linear'))
    
    # Compile with metrics from notebook
    model.compile(
        optimizer='adam', 
        loss='mse', 
        metrics=['mse', 'mae', RootMeanSquaredError()]
    )
    
    return model

def prepare_advanced_data(data, sequence_length):
    """Prepare data using notebook approach with window-based sequences"""
    X, y = [], []
    
    # Use Close prices for prediction
    if 'Close' in data.columns:
        prices = data['Close'].values
    else:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            prices = data[numeric_cols[-1]].values
        else:
            return np.array([]), np.array([])
    
    # Create sequences using notebook approach
    for i in range(1, len(prices) - sequence_length - 1, 1):
        first = prices[i]
        temp = []
        temp2 = []
        
        # Create input sequence
        for j in range(sequence_length):
            temp.append((prices[i + j] - first) / first)
        
        # Create target (next value)
        temp2.append((prices[i + sequence_length] - first) / first)
        
        X.append(np.array(temp).reshape(sequence_length, 1))
        y.append(np.array(temp2).reshape(1, 1))
    
    return np.array(X), np.array(y)

def fetch_nifty_data():
    """Fetch latest NIFTY data using yfinance"""
    try:
        # Fetch NIFTY 50 data
        nifty = yf.download('^NSEI', start=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'), 
                           end=datetime.now().strftime('%Y-%m-%d'))
        
        if not nifty.empty:
            # Fix multi-index column names from yfinance
            if isinstance(nifty.columns, pd.MultiIndex):
                nifty.columns = nifty.columns.get_level_values(0)
            print(f"Data fetched successfully: {nifty.shape}, columns: {nifty.columns.tolist()}")
            return nifty
        
        # Fallback to CSV data
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'NIFTY50_all.csv')
        if os.path.exists(csv_path):
            nifty = pd.read_csv(csv_path)
            nifty['Date'] = pd.to_datetime(nifty['Date'])
            nifty = nifty.set_index('Date')
            nifty = nifty.sort_index()
            print(f"Using CSV fallback data: {nifty.shape}, columns: {nifty.columns.tolist()}")
            return nifty
        
        print("No data available from any source")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def train_model():
    """Train the advanced CNN-LSTM model"""
    global model, scaler, model_performance
    
    # Fetch data
    data = fetch_nifty_data()
    if data is None:
        return False
    
    # Use Close prices
    if 'Close' in data.columns:
        prices = data['Close'].values.reshape(-1, 1)
    else:
        # If no Close column, use the last numeric column
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            prices = data[numeric_cols[-1]].values.reshape(-1, 1)
        else:
            return False
    
    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(prices)
    
    # Prepare sequences using advanced method
    X, y = prepare_advanced_data(data, sequence_length)
    
    if len(X) == 0:
        return False
    
    # Split data
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Reshape for TimeDistributed CNN + LSTM
    X_train = X_train.reshape((X_train.shape[0], 1, sequence_length, 1))
    X_test = X_test.reshape((X_test.shape[0], 1, sequence_length, 1))
    
    # Create and train model
    model = create_advanced_cnn_lstm_model((sequence_length, 1))
    history = model.fit(
        X_train, y_train, 
        epochs=40, 
        batch_size=40, 
        validation_data=(X_test, y_test), 
        verbose=0,
        shuffle=True
    )
    
    # Calculate comprehensive performance metrics (from notebook)
    y_pred = model.predict(X_test, verbose=0)
    
    # Inverse transform predictions
    y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, 1))
    y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Calculate all metrics from notebook
    model_performance = {
        'mse': float(mean_squared_error(y_test_original, y_pred_original)),
        'mae': float(mean_absolute_error(y_test_original, y_pred_original)),
        'r2': float(r2_score(y_test_original, y_pred_original)),
        'rmse': float(np.sqrt(mean_squared_error(y_test_original, y_pred_original))),
        'explained_variance': float(explained_variance_score(y_test_original, y_pred_original)),
        'max_error': float(max_error(y_test_original, y_pred_original)),
        'training_loss': float(history.history['loss'][-1]),
        'validation_loss': float(history.history['val_loss'][-1]),
        'training_mse': float(history.history['mse'][-1]),
        'validation_mse': float(history.history['val_mse'][-1]),
        'training_mae': float(history.history['mae'][-1]),
        'validation_mae': float(history.history['val_mae'][-1]),
        'training_epochs': len(history.history['loss'])
    }
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'nifty_model.h5')
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'scaler.pkl')
    performance_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'performance.pkl')
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(model_performance, performance_path)
    
    return True

def load_model_from_disk():
    """Load pre-trained model from disk"""
    global model, scaler, model_performance
    
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'nifty_model.h5')
        scaler_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'scaler.pkl')
        performance_path = os.path.join(os.path.dirname(__file__), '..', 'saved_model', 'performance.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = load_model(model_path)
            scaler = joblib.load(scaler_path)
            
            if os.path.exists(performance_path):
                model_performance = joblib.load(performance_path)
            
            return True
    except Exception as e:
        print(f"Error loading model: {e}")
    
    return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'NIFTY Prediction API is running'})

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Get information about the current model"""
    try:
        if model is None:
            if not load_model_from_disk():
                return jsonify({
                    'status': 'error',
                    'message': 'No model available',
                    'model_loaded': False
                })
        
        model_summary = []
        if model:
            model.summary(print_fn=lambda x: model_summary.append(x))
        
        return jsonify({
            'status': 'success',
            'model_loaded': model is not None,
            'model_summary': model_summary,
            'sequence_length': sequence_length,
            'performance': model_performance if model_performance else None
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train():
    """Train the model endpoint"""
    try:
        success = train_model()
        if success:
            return jsonify({
                'status': 'success', 
                'message': 'Model trained successfully',
                'performance': model_performance
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to train model'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make price predictions endpoint"""
    try:
        # Load model if not loaded
        if model is None:
            if not load_model_from_disk():
                return jsonify({'status': 'error', 'message': 'Model not available. Please train first.'}), 400
        
        # Get prediction days from request
        data = request.get_json()
        days = data.get('days', 7)
        
        # Fetch recent data
        recent_data = fetch_nifty_data()
        if recent_data is None:
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), 500
        
        # Use Close prices
        if 'Close' in recent_data.columns:
            prices = recent_data['Close'].values.reshape(-1, 1)
        else:
            numeric_cols = recent_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                prices = recent_data[numeric_cols[-1]].values.reshape(-1, 1)
            else:
                return jsonify({'status': 'error', 'message': 'No valid price data found'}), 500
        
        # Scale data
        scaled_prices = scaler.transform(prices)
        
        # Prepare input sequence using advanced method
        last_sequence = scaled_prices[-sequence_length:].reshape(1, 1, sequence_length, 1)
        
        # Make predictions
        predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(days):
            # Predict next value
            next_pred = model.predict(current_sequence, verbose=0)
            predictions.append(next_pred[0, 0])
            
            # Update sequence for next prediction
            current_sequence = np.roll(current_sequence, -1, axis=2)
            current_sequence[0, 0, -1, 0] = next_pred[0, 0]
        
        # Inverse transform predictions
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        
        # Generate dates
        last_date = recent_data.index[-1]
        if isinstance(last_date, str):
            last_date = pd.to_datetime(last_date)
        
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        
        # Format results
        results = []
        for i, (date, pred) in enumerate(zip(prediction_dates, predictions)):
            results.append({
                'date': date.strftime('%Y-%m-%d'),
                'predicted_price': float(pred[0]),
                'day': i + 1
            })
        
        return jsonify({
            'status': 'success',
            'predictions': results,
            'current_price': float(prices[-1][0]),
            'last_date': last_date.strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/historical', methods=['GET'])
def get_historical_data():
    """Get historical NIFTY data with technical indicators"""
    try:
        data = fetch_nifty_data()
        if data is None:
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), 500
        
        # Calculate technical indicators
        indicators = calculate_technical_indicators(data)
        
        # Convert to JSON serializable format
        if 'Close' in data.columns:
            prices = data['Close']
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                prices = data[numeric_cols[-1]]
            else:
                return jsonify({'status': 'error', 'message': 'No valid price data found'}), 500
        
        historical_data = []
        for i, (date, price) in enumerate(prices.items()):
            if pd.notna(price):
                data_point = {
                    'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                    'price': float(price),
                    'index': i
                }
                
                # Add technical indicators
                for indicator_name, values in indicators.items():
                    if i < len(values) and pd.notna(values[i]):
                        data_point[indicator_name] = float(values[i])
                
                historical_data.append(data_point)
        
        return jsonify({
            'status': 'success',
            'data': historical_data[-200:],  # Last 200 data points
            'indicators': list(indicators.keys())
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/market-links', methods=['GET'])
def get_market_links():
    """Get external stock market links"""
    links = [
        {
            'name': 'NSE India',
            'url': 'https://www.nseindia.com/',
            'description': 'Official National Stock Exchange website'
        },
        {
            'name': 'Money Control',
            'url': 'https://www.moneycontrol.com/india/stockpricequote/',
            'description': 'Comprehensive stock market information'
        },
        {
            'name': 'Yahoo Finance',
            'url': 'https://finance.yahoo.com/quote/%5ENSEI/',
            'description': 'NIFTY 50 on Yahoo Finance'
        },
        {
            'name': 'Trading View',
            'url': 'https://www.tradingview.com/symbols/NSE-NIFTY/',
            'description': 'Advanced charting and analysis'
        },
        {
            'name': 'Investing.com',
            'url': 'https://in.investing.com/indices/s-p-cnx-nifty',
            'description': 'Real-time NIFTY data and news'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'links': links
    })

if __name__ == '__main__':
    # Try to load existing model
    load_model_from_disk()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
