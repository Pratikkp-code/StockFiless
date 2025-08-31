# StockFiles :  NIFTY 50 Price Prediction Project

A comprehensive machine learning project that predicts NIFTY 50 stock prices using a hybrid LSTM + CNN neural network model, with a modern React frontend and Flask backend.


https://www.kaggle.com/code/vedanthumbe/mlwing

## 🚀 Features

- **Advanced ML Model**: Hybrid LSTM + CNN architecture for accurate price predictions
- **Real-time Data**: Fetches live NIFTY 50 data using yfinance API
- **Interactive Dashboard**: Beautiful React frontend with Material-UI components
- **Price Charts**: Historical data visualization and prediction plots using Recharts
- **External Links**: Direct access to major stock market websites
- **Docker Support**: Fully containerized application for easy deployment
- **RESTful API**: Flask backend with comprehensive endpoints

<img width="1919" height="888" alt="image" src="https://github.com/user-attachments/assets/727f2809-ce2f-4668-852f-41aaed37b2c4" />




<img width="1902" height="766" alt="image" src="https://github.com/user-attachments/assets/1be78df0-8380-4989-a4e4-626dde939c5f" />




Trained model : 

<img width="1886" height="888" alt="image" src="https://github.com/user-attachments/assets/661a0d20-ddae-4678-9760-783a9872fc28" />


## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Flask Backend  │    │  ML Model      │
│   (Port 80)     │◄──►│  (Port 5000)    │◄──►│  (LSTM + CNN)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
vedisalive/
├── niftypred/                    # Backend ML Application
│   ├── app/
│   │   └── app.py               # Flask API server
│   ├── data/
│   │   └── NIFTY50_all.csv      # Historical NIFTY data
│   ├── saved_model/              # Trained model storage
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile               # Backend container
├── nifty-prediction-app/         # React Frontend
│   ├── src/
│   │   ├── App.js               # Main application component
│   │   └── App.css              # Custom styling
│   ├── Dockerfile               # Frontend container
│   └── nginx.conf               # Nginx configuration
├── docker-compose.yml            # Service orchestration
└── README.md                     # This file
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**
- **Flask**: Web framework
- **TensorFlow/Keras**: Deep learning framework
- **LSTM + CNN**: Hybrid neural network architecture
- **Pandas**: Data manipulation
- **yfinance**: Stock data fetching
- **scikit-learn**: Data preprocessing

### Frontend
- **React 18**: Frontend framework
- **Material-UI**: Component library
- **Recharts**: Charting library
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Service orchestration
- **Nginx**: Web server and reverse proxy

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git for cloning the repository

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd vedisalive
```

### 2. Build and Run with Docker
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📊 API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Model Training
- `POST /api/train` - Train the LSTM + CNN model

### Predictions
- `POST /api/predict` - Get price predictions
  - Body: `{"days": 7}` (1-30 days)

### Data
- `GET /api/historical` - Get historical NIFTY data
- `GET /api/market-links` - Get external market links

## 🎯 Usage Guide

### 1. Training the Model
1. Navigate to the Dashboard tab
2. Click "Train Model" button
3. Wait for training to complete (may take several minutes)
4. Model will be saved automatically

### 2. Making Predictions
1. Go to the Predictions tab
2. Enter the number of days (1-30)
3. Click "Predict Prices"
4. View results in charts and detailed cards

### 3. Viewing Historical Data
- Historical NIFTY 50 prices are displayed on the Dashboard
- Data is automatically fetched from yfinance API
- Falls back to local CSV data if API is unavailable

### 4. External Market Links
- Access major stock market websites directly
- Includes NSE India, Money Control, Yahoo Finance, etc.

## 🔧 Development Setup

### Backend Development
```bash
cd niftypred
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```

### Frontend Development
```bash
cd nifty-prediction-app
npm install
npm start
```

## 🐳 Docker Commands

### Build Services
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Manage Services
```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend
```

### Clean Up
```bash
# Remove containers and networks
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove all images
docker-compose down --rmi all
```

## 📈 Model Architecture

### LSTM + CNN Hybrid
- **CNN Layers**: Feature extraction from time series data
  - Conv1D (64 filters, kernel_size=3)
  - MaxPooling1D (pool_size=2)
  - Conv1D (32 filters, kernel_size=3)
  - MaxPooling1D (pool_size=2)

- **LSTM Layers**: Sequence learning and temporal dependencies
  - LSTM (50 units, return_sequences=True)
  - Dropout (0.2)
  - LSTM (50 units, return_sequences=False)
  - Dropout (0.2)

- **Dense Layers**: Final prediction
  - Dense (25 units)
  - Dense (1 unit) - Output

### Training Parameters
- **Sequence Length**: 60 days
- **Epochs**: 50
- **Batch Size**: 32
- **Optimizer**: Adam
- **Loss Function**: Mean Squared Error

## 🔍 Data Sources

### Primary Source
- **yfinance**: Real-time NIFTY 50 data from Yahoo Finance
- **Symbol**: ^NSEI (NIFTY 50 Index)

### Fallback Source
- **Local CSV**: NIFTY50_all.csv with historical data
- **Columns**: Date, Symbol, Series, Prev Close, Open, High, Low, Last, Close, VWAP, Volume, Turnover, Trades, Deliverable Volume, %Deliverable

## 🚨 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Check if Docker containers are running: `docker-compose ps`
   - Verify backend health: `curl http://localhost:5000/api/health`
   - Check logs: `docker-compose logs backend`

2. **Model Training Fails**
   - Ensure sufficient data is available
   - Check Python dependencies in requirements.txt
   - Verify data format in CSV file

3. **Frontend Not Loading**
   - Check nginx logs: `docker-compose logs frontend`
   - Verify frontend container is running
   - Check browser console for errors

4. **Port Conflicts**
   - Change ports in docker-compose.yml
   - Ensure ports 80 and 5000 are available

### Performance Optimization
- **Model Training**: Reduce epochs for faster training
- **Data Loading**: Use smaller datasets for development
- **Memory**: Adjust Docker memory limits if needed

## 🔒 Security Features

- **CORS**: Configured for development
- **Rate Limiting**: API rate limiting in nginx
- **Security Headers**: XSS protection, content type validation
- **Input Validation**: Server-side validation for predictions

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🔮 Future Enhancements

- [ ] Real-time price updates
- [ ] Multiple stock support
- [ ] Advanced technical indicators
- [ ] Portfolio management features
- [ ] Mobile app development
- [ ] Machine learning model versioning
- [ ] Automated trading signals
- [ ] Performance analytics dashboard

---

**Note**: This is a machine learning project for educational purposes. Stock predictions should not be used as the sole basis for investment decisions. Always consult with financial advisors and conduct thorough research before making investment decisions.
