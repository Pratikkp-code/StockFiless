import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  TextField,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Link,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Switch,
  FormControlLabel
} from '@mui/material';
import {
  ShowChart,
  Link as LinkIcon,
  Refresh,
  PlayArrow,
  Analytics,
  ModelTraining,
  Timeline,
  Info,
  Warning,
  CheckCircle
} from '@mui/icons-material';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  AreaChart, Area, ComposedChart, Bar
} from 'recharts';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [historicalData, setHistoricalData] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [currentPrice, setCurrentPrice] = useState(null);
  const [predictionDays, setPredictionDays] = useState(7);
  const [marketLinks, setMarketLinks] = useState([]);
  const [modelStatus, setModelStatus] = useState('unknown');
  const [modelInfo, setModelInfo] = useState(null);
  const [showTechnicalIndicators, setShowTechnicalIndicators] = useState(true);
  const [selectedIndicators, setSelectedIndicators] = useState(['SMA_20', 'EMA_12', 'RSI']);

  const API_BASE_URL = 'http://localhost:5000/api';

  useEffect(() => {
    checkHealth();
    fetchHistoricalData();
    fetchMarketLinks();
    fetchModelInfo();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (response.ok) {
        setModelStatus('healthy');
      } else {
        setModelStatus('unhealthy');
      }
    } catch (error) {
      setModelStatus('unhealthy');
    }
  };

  const fetchHistoricalData = async () => {
    try {
      console.log('Fetching historical data...');
      const response = await fetch(`${API_BASE_URL}/historical`);
      const data = await response.json();
      console.log('Historical data response:', data);
      if (data.status === 'success') {
        console.log('Setting historical data:', data.data);
        setHistoricalData(data.data);
        if (data.data.length > 0) {
          setCurrentPrice(data.data[data.data.length - 1].price);
          console.log('Current price set to:', data.data[data.data.length - 1].price);
        }
      } else {
        console.error('Historical data fetch failed:', data.message);
      }
    } catch (error) {
      console.error('Error fetching historical data:', error);
    }
  };

  const fetchMarketLinks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/market-links`);
      const data = await response.json();
      if (data.status === 'success') {
        setMarketLinks(data.links);
      }
    } catch (error) {
      console.error('Error fetching market links:', error);
    }
  };

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/model-info`);
      const data = await response.json();
      if (data.status === 'success') {
        setModelInfo(data);
      }
    } catch (error) {
      console.error('Error fetching model info:', error);
    }
  };

  const trainModel = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    
    try {
      const response = await fetch(`${API_BASE_URL}/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setMessage({ type: 'success', text: data.message });
        fetchModelInfo(); // Refresh model info
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to train model' });
    } finally {
      setLoading(false);
    }
  };

  const makePrediction = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ days: predictionDays }),
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setPredictions(data.predictions);
        setMessage({ type: 'success', text: 'Predictions generated successfully' });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to generate predictions' });
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(price);
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-IN');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'unhealthy': return 'error';
      default: return 'warning';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return <CheckCircle />;
      case 'unhealthy': return <Warning />;
      default: return <Info />;
    }
  };

  const renderPriceChart = () => {
    console.log('Rendering price chart with data:', historicalData);
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            NIFTY 50 Price Chart
          </Typography>
          {historicalData && historicalData.length > 0 ? (
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={formatDate}
                  interval="preserveStartEnd"
                />
                <YAxis 
                  domain={['dataMin - 100', 'dataMax + 100']}
                  tickFormatter={formatPrice}
                />
                <RechartsTooltip 
                  labelFormatter={formatDate}
                  formatter={(value) => [formatPrice(value), 'Price']}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#2196F3" 
                  strokeWidth={2}
                  dot={false}
                  name="NIFTY 50"
                />
                {showTechnicalIndicators && selectedIndicators.includes('SMA_20') && (
                  <Line 
                    type="monotone" 
                    dataKey="SMA_20" 
                    stroke="#FF9800" 
                    strokeWidth={1}
                    dot={false}
                    name="SMA 20"
                  />
                )}
                {showTechnicalIndicators && selectedIndicators.includes('SMA_50') && (
                  <Line 
                    type="monotone" 
                    dataKey="SMA_50" 
                    stroke="#9C27B0" 
                    strokeWidth={1}
                    dot={false}
                    name="SMA 50"
                  />
                )}
                {showTechnicalIndicators && selectedIndicators.includes('EMA_12') && (
                  <Line 
                    type="monotone" 
                    dataKey="EMA_12" 
                    stroke="#4CAF50" 
                    strokeWidth={1}
                    dot={false}
                    name="EMA 12"
                  />
                )}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <Box textAlign="center" py={4}>
              <Typography variant="body1" color="textSecondary">
                No data available. Please wait for data to load or check the backend.
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderTechnicalIndicators = () => {
    console.log('Rendering technical indicators with data:', historicalData);
    return (
      <Grid container spacing={2}>
        {/* Moving Averages Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Moving Averages
              </Typography>
              {historicalData && historicalData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={formatDate} />
                    <YAxis tickFormatter={formatPrice} />
                    <RechartsTooltip labelFormatter={formatDate} formatter={(value) => [formatPrice(value), 'Price']} />
                    <Legend />
                    <Line type="monotone" dataKey="price" stroke="#000" strokeWidth={2} name="NIFTY 50" />
                    <Line type="monotone" dataKey="MA_10_days" stroke="#FF6B6B" strokeWidth={1} name="MA 10 Days" />
                    <Line type="monotone" dataKey="MA_50_days" stroke="#4ECDC4" strokeWidth={1} name="MA 50 Days" />
                    <Line type="monotone" dataKey="MA_100_days" stroke="#45B7D1" strokeWidth={1} name="MA 100 Days" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body1" color="textSecondary" textAlign="center">
                  No data available for technical indicators.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* RSI Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                RSI (Relative Strength Index)
              </Typography>
              {historicalData && historicalData.length > 0 ? (
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={formatDate} />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip labelFormatter={formatDate} />
                    <Line type="monotone" dataKey="RSI" stroke="#E91E63" strokeWidth={2} />
                    <Line y={70} stroke="#FF5722" strokeDasharray="5 5" />
                    <Line y={30} stroke="#FF5722" strokeDasharray="5 5" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body1" color="textSecondary" textAlign="center">
                  No RSI data available.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        {/* MACD Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                MACD
              </Typography>
              {historicalData && historicalData.length > 0 ? (
                <ResponsiveContainer width="100%" height={200}>
                  <ComposedChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={formatDate} />
                    <YAxis />
                    <RechartsTooltip labelFormatter={formatDate} />
                    <Bar dataKey="MACD_Histogram" fill="#2196F3" opacity={0.6} name="MACD Histogram" />
                    <Line type="monotone" dataKey="MACD" stroke="#FF9800" strokeWidth={2} name="MACD Line" />
                    <Line type="monotone" dataKey="MACD_Signal" stroke="#4CAF50" strokeWidth={2} name="Signal Line" />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body1" color="textSecondary" textAlign="center">
                  No MACD data available.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        {/* Bollinger Bands Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Bollinger Bands
              </Typography>
              {historicalData && historicalData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={formatDate} />
                    <YAxis tickFormatter={formatPrice} />
                    <RechartsTooltip labelFormatter={formatDate} formatter={(value) => [formatPrice(value), 'Price']} />
                    <Area type="monotone" dataKey="BB_Upper" stackId="1" stroke="#4CAF50" fill="#4CAF50" fillOpacity={0.1} name="Upper Band" />
                    <Area type="monotone" dataKey="BB_Lower" stackId="1" stroke="#F44336" fill="#F44336" fillOpacity={0.1} name="Lower Band" />
                    <Line type="monotone" dataKey="BB_Middle" stroke="#2196F3" strokeWidth={2} name="Middle Band" />
                    <Line type="monotone" dataKey="price" stroke="#000" strokeWidth={2} name="NIFTY 50" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body1" color="textSecondary" textAlign="center">
                  No Bollinger Bands data available.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderPredictions = () => (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Price Predictions
            </Typography>
            {predictions.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={predictions}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tickFormatter={formatDate} />
                  <YAxis tickFormatter={formatPrice} />
                  <RechartsTooltip labelFormatter={formatDate} formatter={(value) => [formatPrice(value), 'Predicted Price']} />
                  <Legend />
                  <Line type="monotone" dataKey="predicted_price" stroke="#E91E63" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <Box textAlign="center" py={4}>
                <Typography variant="body1" color="textSecondary">
                  No predictions available. Generate predictions to see the chart.
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      </Grid>
      
      {predictions.length > 0 && (
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Prediction Details
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Day</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Predicted Price</TableCell>
                      <TableCell>Change from Current</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {predictions.map((pred, index) => {
                      const change = currentPrice ? pred.predicted_price - currentPrice : 0;
                      const changePercent = currentPrice ? (change / currentPrice) * 100 : 0;
                      return (
                        <TableRow key={index}>
                          <TableCell>{pred.day}</TableCell>
                          <TableCell>{formatDate(pred.date)}</TableCell>
                          <TableCell>{formatPrice(pred.predicted_price)}</TableCell>
                          <TableCell>
                            <Typography 
                              variant="body2" 
                              color={change >= 0 ? 'success.main' : 'error.main'}
                            >
                              {change >= 0 ? '+' : ''}{formatPrice(change)} ({changePercent >= 0 ? '+' : ''}{changePercent.toFixed(2)}%)
                            </Typography>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      )}
    </Grid>
  );

  const renderModelInfo = () => (
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Status
            </Typography>
            <Box display="flex" alignItems="center" mb={2}>
              <Chip
                icon={getStatusIcon(modelStatus)}
                label={modelStatus.toUpperCase()}
                color={getStatusColor(modelStatus)}
                variant="outlined"
              />
            </Box>
            <Typography variant="body2" color="textSecondary">
              Model Loaded: {modelInfo?.model_loaded ? 'Yes' : 'No'}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Sequence Length: {modelInfo?.sequence_length || 'N/A'}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Architecture: Advanced CNN-LSTM (Notebook Style)
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      
      {modelInfo?.performance && (
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Model Performance Metrics
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">MSE</Typography>
                  <Typography variant="h6">{modelInfo.performance.mse.toFixed(4)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">MAE</Typography>
                  <Typography variant="h6">{modelInfo.performance.mae.toFixed(4)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">R² Score</Typography>
                  <Typography variant="h6">{modelInfo.performance.r2.toFixed(4)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">RMSE</Typography>
                  <Typography variant="h6">{modelInfo.performance.rmse.toFixed(4)}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      )}
      
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Advanced CNN-LSTM Architecture
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              This model uses the advanced architecture from the notebook with:
            </Typography>
            <Box component="ul" sx={{ pl: 2, mb: 2 }}>
              <li>TimeDistributed CNN layers (64→128→64 filters)</li>
              <li>Bidirectional LSTM layers (100 units each)</li>
              <li>Advanced data preprocessing with 100-day sequences</li>
              <li>Comprehensive technical indicators</li>
            </Box>
            <Box bgcolor="grey.100" p={2} borderRadius={1} maxHeight={200} overflow="auto">
              <pre style={{ margin: 0, fontSize: '12px' }}>
                {modelInfo?.model_summary?.join('\n') || 'No model summary available'}
              </pre>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderMarketLinks = () => (
    <Grid container spacing={2}>
      {marketLinks.map((link, index) => (
        <Grid item xs={12} md={6} lg={4} key={index}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {link.name}
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                {link.description}
              </Typography>
              <Link href={link.url} target="_blank" rel="noopener noreferrer">
                Visit Site
              </Link>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box textAlign="center" mb={4}>
        <Typography variant="h3" component="h1" gutterBottom color="primary">
          NIFTY 50 Prediction Dashboard
        </Typography>
        <Typography variant="h6" color="textSecondary">
          Advanced AI-powered stock market analysis and prediction
        </Typography>
      </Box>

      {message.text && (
        <Alert severity={message.type} sx={{ mb: 3 }}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent textAlign="center">
              <Typography variant="h4" color="primary">
                {currentPrice ? formatPrice(currentPrice) : 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Current NIFTY 50 Price
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent textAlign="center">
              <Typography variant="h4" color="success.main">
                {predictions.length > 0 ? formatPrice(predictions[predictions.length - 1]?.predicted_price) : 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {predictionDays}-Day Prediction
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent textAlign="center">
              <Typography variant="h4" color="info.main">
                {modelInfo?.performance?.r2 ? (modelInfo.performance.r2 * 100).toFixed(1) + '%' : 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Model Accuracy (R²)
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent textAlign="center">
              <Typography variant="h4" color="warning.main">
                {historicalData.length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Data Points
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box mb={3}>
        <Paper sx={{ width: '100%' }}>
          <Tabs value={activeTab} onChange={handleTabChange} centered>
            <Tab icon={<ShowChart />} label="Price Charts" />
            <Tab icon={<Analytics />} label="Technical Indicators" />
            <Tab icon={<Timeline />} label="Predictions" />
            <Tab icon={<ModelTraining />} label="Model Info" />
            <Tab icon={<LinkIcon />} label="Market Links" />
          </Tabs>
        </Paper>
      </Box>

      <Box mb={3}>
        <Paper sx={{ p: 2 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
              <Typography variant="h6">Controls</Typography>
            </Grid>
            <Grid item>
              <TextField
                label="Prediction Days"
                type="number"
                value={predictionDays}
                onChange={(e) => setPredictionDays(parseInt(e.target.value))}
                inputProps={{ min: 1, max: 30 }}
                size="small"
              />
            </Grid>
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                onClick={makePrediction}
                disabled={loading}
                startIcon={<PlayArrow />}
              >
                Generate Predictions
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                color="secondary"
                onClick={trainModel}
                disabled={loading}
                startIcon={<ModelTraining />}
              >
                Train Model
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                onClick={fetchHistoricalData}
                startIcon={<Refresh />}
              >
                Refresh Data
              </Button>
            </Grid>
            <Grid item>
              <FormControlLabel
                control={
                  <Switch
                    checked={showTechnicalIndicators}
                    onChange={(e) => setShowTechnicalIndicators(e.target.checked)}
                  />
                }
                label="Show Technical Indicators"
              />
            </Grid>
          </Grid>
        </Paper>
      </Box>

      {loading && (
        <Box textAlign="center" py={4}>
          <CircularProgress size={60} />
          <Typography variant="h6" mt={2}>
            Processing...
          </Typography>
        </Box>
      )}

      {!loading && (
        <Box>
          {activeTab === 0 && renderPriceChart()}
          {activeTab === 1 && renderTechnicalIndicators()}
          {activeTab === 2 && renderPredictions()}
          {activeTab === 3 && renderModelInfo()}
          {activeTab === 4 && renderMarketLinks()}
        </Box>
      )}
    </Container>
  );
}

export default App;
