# NIFTY 50 Prediction Dashboard

A comprehensive, AI-powered stock market analysis and prediction platform featuring advanced visualizations, technical indicators, and machine learning predictions.

## 🚀 Features

### 📊 **Advanced Charting & Visualization**
- **Interactive Price Charts**: Real-time NIFTY 50 price data with zoom and pan capabilities
- **Technical Indicators**: Multiple overlay options including SMA, EMA, RSI, MACD, and Bollinger Bands
- **Multi-timeframe Analysis**: Historical data visualization with customizable date ranges
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### 🤖 **AI-Powered Predictions**
- **LSTM + CNN Hybrid Model**: Advanced deep learning architecture combining Convolutional and Recurrent Neural Networks
- **Real-time Predictions**: Generate price forecasts for 1-30 days ahead
- **Model Performance Metrics**: Comprehensive evaluation including MSE, MAE, R² Score, and RMSE
- **Automated Training**: One-click model training with latest market data

### 📈 **Technical Analysis Tools**
- **Moving Averages**: Simple Moving Average (SMA) and Exponential Moving Average (EMA)
- **RSI (Relative Strength Index)**: Momentum oscillator with overbought/oversold levels
- **MACD**: Moving Average Convergence Divergence with signal line
- **Bollinger Bands**: Volatility indicators with upper, middle, and lower bands
- **Volume Analysis**: Trading volume patterns and trends

### 🎯 **Dashboard Features**
- **Real-time Market Data**: Live NIFTY 50 prices and market statistics
- **Performance Monitoring**: Model accuracy and training metrics
- **Interactive Controls**: Toggle technical indicators, adjust prediction parameters
- **Status Monitoring**: API health checks and system status indicators

## 🏗️ Architecture

### Backend (Flask + Python)
- **Flask API**: RESTful endpoints for data and predictions
- **TensorFlow/Keras**: Deep learning model implementation
- **Scikit-learn**: Data preprocessing and performance metrics
- **yfinance**: Real-time market data fetching
- **Joblib**: Model serialization and storage

### Frontend (React + Material-UI)
- **React 18**: Modern React with hooks and functional components
- **Material-UI**: Professional UI components and theming
- **Recharts**: Interactive charting library
- **Responsive Design**: Mobile-first approach with breakpoint optimization

### Machine Learning Model
- **LSTM Layers**: Long Short-Term Memory for sequence modeling
- **CNN Layers**: Convolutional layers for feature extraction
- **Hybrid Architecture**: Combines temporal and spatial learning
- **Sequence Length**: 60-day lookback window for predictions

## 📱 Dashboard Sections

### 1. **Price Charts Tab**
- Main NIFTY 50 price chart with technical indicator overlays
- Interactive tooltips and zoom functionality
- Multiple timeframe support
- Customizable indicator visibility

### 2. **Technical Indicators Tab**
- **RSI Chart**: Momentum analysis with 30/70 threshold lines
- **MACD Chart**: Trend following with histogram and signal line
- **Bollinger Bands**: Volatility and price channel analysis
- **Moving Averages**: Trend identification and support/resistance

### 3. **Predictions Tab**
- Future price predictions with confidence intervals
- Interactive prediction chart
- Detailed prediction table with price changes
- Percentage change calculations

### 4. **Model Info Tab**
- Model architecture and parameters
- Performance metrics and evaluation scores
- Training history and validation results
- Model status and health information

### 5. **Market Links Tab**
- External financial data sources
- Trading platforms and analysis tools
- News and research resources
- Direct links to market information

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd stockFile/niftypred
pip install -r requirements-simple.txt
cd app
python app.py
```

### Frontend Setup
```bash
cd stockFile/nifty-prediction-app
npm install
npm start
```

### Docker Setup (Optional)
```bash
cd stockFile
docker-compose up --build
```

## 📊 Data Sources

- **Primary**: Yahoo Finance (yfinance) - Real-time NIFTY 50 data
- **Fallback**: Local CSV data for offline functionality
- **Technical Indicators**: Calculated on-the-fly from price data
- **Model Training**: Historical data with 80/20 train-test split

## 🔧 Configuration

### Model Parameters
- **Sequence Length**: 60 days (configurable)
- **Training Epochs**: 50 (adjustable)
- **Batch Size**: 32
- **Validation Split**: 20%

### Chart Settings
- **Data Points**: Last 200 historical points
- **Prediction Range**: 1-30 days
- **Indicator Periods**: Configurable moving average windows
- **Chart Height**: Responsive based on screen size

## 📈 Technical Indicators Explained

### Moving Averages
- **SMA (Simple Moving Average)**: Average price over specified period
- **EMA (Exponential Moving Average)**: Weighted average giving more importance to recent prices

### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: Above 70 (potential sell signal)
- **Oversold**: Below 30 (potential buy signal)
- **Neutral**: 30-70 range

### MACD (Moving Average Convergence Divergence)
- **MACD Line**: Difference between 12-day and 26-day EMA
- **Signal Line**: 9-day EMA of MACD line
- **Histogram**: MACD line minus signal line

### Bollinger Bands
- **Upper Band**: 20-day SMA + (2 × standard deviation)
- **Middle Band**: 20-day SMA
- **Lower Band**: 20-day SMA - (2 × standard deviation)

## 🎨 UI/UX Features

### Modern Design
- **Gradient Backgrounds**: Professional color schemes
- **Glass Morphism**: Modern visual effects
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adaptive to all screen sizes

### Interactive Elements
- **Hover Effects**: Enhanced user experience
- **Loading States**: Visual feedback during operations
- **Error Handling**: User-friendly error messages
- **Success Notifications**: Confirmation of completed actions

### Accessibility
- **High Contrast**: Readable text and charts
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and descriptions
- **Color Blind Friendly**: Accessible color schemes

## 🔍 API Endpoints

### Core Endpoints
- `GET /api/health` - System health check
- `GET /api/model-info` - Model status and performance
- `POST /api/train` - Train/retrain the model
- `POST /api/predict` - Generate price predictions
- `GET /api/historical` - Historical data with indicators
- `GET /api/market-links` - External market resources

### Response Format
```json
{
  "status": "success|error",
  "message": "Description",
  "data": {},
  "performance": {}
}
```

## 📱 Mobile Optimization

- **Responsive Grid**: Adaptive layout for mobile devices
- **Touch-Friendly**: Optimized for touch interactions
- **Mobile Navigation**: Simplified navigation for small screens
- **Performance**: Optimized loading for mobile networks

## 🚀 Performance Features

- **Lazy Loading**: Load data on demand
- **Caching**: Store model and data locally
- **Optimized Charts**: Efficient rendering for large datasets
- **Background Processing**: Non-blocking operations

## 🔒 Security Features

- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: Sanitized user inputs
- **Error Handling**: Secure error messages
- **Rate Limiting**: API request throttling

## 📊 Future Enhancements

- **Real-time Updates**: WebSocket integration for live data
- **Portfolio Management**: Track multiple stocks
- **Advanced Analytics**: More technical indicators
- **Machine Learning**: Additional model architectures
- **Backtesting**: Historical strategy testing
- **Alerts**: Price and indicator notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🙏 Acknowledgments

- **TensorFlow/Keras**: Deep learning framework
- **Material-UI**: React component library
- **Recharts**: Charting library
- **yfinance**: Financial data provider
- **Flask**: Web framework
- **React**: Frontend library

---

**Note**: This application is for educational and research purposes. Financial predictions should not be considered as investment advice. Always consult with financial professionals before making investment decisions.
