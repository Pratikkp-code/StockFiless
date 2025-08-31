#!/usr/bin/env python3
"""
Startup Script for NIFTY Prediction Project
Launches both backend and frontend services
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed or not in PATH")
        return False

def check_docker_compose():
    """Check if Docker Compose is available"""
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker Compose is available")
            return True
        else:
            print("❌ Docker Compose is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose is not installed or not in PATH")
        return False

def start_services():
    """Start the Docker services"""
    print("🚀 Starting NIFTY Prediction services...")
    
    try:
        # Build and start services
        subprocess.run(['docker-compose', 'up', '--build', '-d'], check=True)
        print("✅ Services started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start services: {e}")
        return False

def check_service_health():
    """Check if services are healthy"""
    print("🔍 Checking service health...")
    
    import requests
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(30)
    
    # Check backend health
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print("❌ Backend health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check failed: {e}")
        return False
    
    # Check frontend health
    try:
        response = requests.get('http://localhost/health', timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is healthy")
        else:
            print("❌ Frontend health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend health check failed: {e}")
        return False
    
    return True

def open_browser():
    """Open the application in the default browser"""
    print("🌐 Opening application in browser...")
    
    try:
        webbrowser.open('http://localhost')
        print("✅ Browser opened successfully")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print("💡 Please manually open: http://localhost")

def show_status():
    """Show the status of running services"""
    print("\n📊 Service Status:")
    print("-" * 40)
    
    try:
        result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Failed to get service status: {e}")

def show_logs():
    """Show recent logs from services"""
    print("\n📋 Recent Logs:")
    print("-" * 40)
    
    try:
        # Show backend logs
        print("🔧 Backend Logs:")
        result = subprocess.run(['docker-compose', 'logs', '--tail=10', 'backend'], 
                              capture_output=True, text=True)
        print(result.stdout)
        
        print("\n🌐 Frontend Logs:")
        result = subprocess.run(['docker-compose', 'logs', '--tail=10', 'frontend'], 
                              capture_output=True, text=True)
        print(result.stdout)
        
    except Exception as e:
        print(f"❌ Failed to get logs: {e}")

def stop_services():
    """Stop the Docker services"""
    print("🛑 Stopping services...")
    
    try:
        subprocess.run(['docker-compose', 'down'], check=True)
        print("✅ Services stopped successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stop services: {e}")

def main():
    """Main function"""
    print("🎯 NIFTY 50 Price Prediction Project")
    print("=" * 50)
    
    # Check prerequisites
    if not check_docker():
        print("\n💡 Please install Docker Desktop and ensure it's running")
        return
    
    if not check_docker_compose():
        print("\n💡 Please install Docker Compose")
        return
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'start':
            if start_services():
                if check_service_health():
                    open_browser()
                    show_status()
                else:
                    print("⚠️  Services started but health checks failed")
                    show_logs()
        
        elif command == 'stop':
            stop_services()
        
        elif command == 'status':
            show_status()
        
        elif command == 'logs':
            show_logs()
        
        elif command == 'restart':
            print("🔄 Restarting services...")
            stop_services()
            time.sleep(5)
            if start_services():
                if check_service_health():
                    print("✅ Services restarted successfully")
                    show_status()
                else:
                    print("⚠️  Services restarted but health checks failed")
        
        elif command == 'help':
            print_help()
        
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    
    else:
        # Default action: start services
        print("🚀 Starting NIFTY Prediction application...")
        
        if start_services():
            if check_service_health():
                open_browser()
                show_status()
                
                print("\n🎉 Application is ready!")
                print("📱 Frontend: http://localhost")
                print("🔧 Backend API: http://localhost:5000")
                print("\n💡 Use 'python start_app.py help' for more commands")
                
                # Keep running to show logs
                try:
                    print("\n📋 Press Ctrl+C to stop the application")
                    while True:
                        time.sleep(10)
                        show_status()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping application...")
                    stop_services()
                    print("👋 Goodbye!")
            else:
                print("⚠️  Services started but health checks failed")
                show_logs()

def print_help():
    """Print help information"""
    print("\n📖 Available Commands:")
    print("-" * 30)
    print("start    - Start the application")
    print("stop     - Stop the application")
    print("restart  - Restart the application")
    print("status   - Show service status")
    print("logs     - Show recent logs")
    print("help     - Show this help")
    print("\n💡 Usage: python start_app.py [command]")
    print("💡 Default: python start_app.py (starts the app)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        stop_services()
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check the logs and try again")
