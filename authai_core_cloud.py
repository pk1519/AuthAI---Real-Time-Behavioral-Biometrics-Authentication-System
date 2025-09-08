"""
Cloud-Compatible AuthAI Core Module

This version simulates behavioral monitoring for cloud deployment
since pynput and pyautogui don't work in cloud environments.
"""

import time
import random
import threading
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import numpy as np
import os
import csv

class CloudRealTimeMonitor:
    """Simulated real-time monitor for cloud environments"""
    
    def __init__(self, model_name: str, model, scaler=None, ae_meta=None, 
                 window_seconds=30.0, detection_interval=2.0):
        self.model_name = model_name
        self.model = model
        self.scaler = scaler
        self.ae_meta = ae_meta
        self.window_seconds = window_seconds
        self.detection_interval = detection_interval
        self.is_running = False
        self.detection_thread = None
        self.log_file = "detections_log.csv"
        
        # Initialize CSV log file
        self._init_log_file()
        
        # Simulation parameters
        self.base_features = {
            'avg_mouse_speed': 150.0,
            'avg_typing_speed': 200.0,
            'tab_switch_rate': 0.5,
            'mouse_click_rate': 2.0,
            'keyboard_error_rate': 0.05,
            'active_window_duration': 10.0
        }
        
        # Add some randomness to simulate real behavior
        self.feature_variance = {
            'avg_mouse_speed': 50.0,
            'avg_typing_speed': 80.0,
            'tab_switch_rate': 0.2,
            'mouse_click_rate': 1.0,
            'keyboard_error_rate': 0.03,
            'active_window_duration': 5.0
        }
    
    def _init_log_file(self):
        """Initialize the CSV log file with headers"""
        if not os.path.exists(self.log_file):
            headers = [
                'timestamp', 'user_id', 'model', 'score', 'is_improper',
                'avg_mouse_speed', 'avg_typing_speed', 'tab_switch_rate',
                'mouse_click_rate', 'keyboard_error_rate', 'active_window_duration'
            ]
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def _generate_simulated_features(self) -> Dict[str, float]:
        """Generate realistic behavioral features for simulation"""
        features = {}
        for feature, base_value in self.base_features.items():
            variance = self.feature_variance[feature]
            # Add random variation around base value
            features[feature] = max(0, base_value + random.gauss(0, variance))
        
        return features
    
    def _predict_with_model(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Make prediction using the loaded model"""
        try:
            # Convert features to array format expected by model
            feature_array = np.array([[
                features['avg_mouse_speed'],
                features['avg_typing_speed'],
                features['tab_switch_rate'],
                features['mouse_click_rate'],
                features['keyboard_error_rate'],
                features['active_window_duration']
            ]])
            
            # Apply scaling if scaler is available
            if self.scaler:
                feature_array = self.scaler.transform(feature_array)
            
            # Make prediction
            if hasattr(self.model, 'predict_proba'):
                # For models with probability predictions
                pred_proba = self.model.predict_proba(feature_array)[0]
                if len(pred_proba) > 1:
                    score = float(pred_proba[1])  # Probability of bot class
                else:
                    score = float(pred_proba[0])
            else:
                # For models without probability (like Isolation Forest)
                pred = self.model.predict(feature_array)[0]
                # Convert to probability-like score
                score = 0.8 if pred == -1 else 0.2
            
            # Determine if it's considered improper (bot-like)
            is_improper = 1 if score > 0.5 else 0
            
            return {
                'score': score,
                'is_improper': is_improper,
                'prediction': 'Robot' if is_improper else 'Person'
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Return default values on error
            return {
                'score': 0.1,
                'is_improper': 0,
                'prediction': 'Person'
            }
    
    def run_detection_once(self) -> Optional[Dict[str, Any]]:
        """Run a single detection cycle"""
        try:
            # Generate simulated features
            features = self._generate_simulated_features()
            
            # Make prediction
            prediction_result = self._predict_with_model(features)
            
            # Create detection event
            detection = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'user_id': 'cloud_user',
                'model': self.model_name,
                'score': prediction_result['score'],
                'is_improper': prediction_result['is_improper'],
                **features
            }
            
            # Log to CSV
            self._log_detection(detection)
            
            return detection
            
        except Exception as e:
            print(f"Detection error: {e}")
            return None
    
    def _log_detection(self, detection: Dict[str, Any]):
        """Log detection to CSV file"""
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    detection['timestamp'],
                    detection['user_id'],
                    detection['model'],
                    detection['score'],
                    detection['is_improper'],
                    detection['avg_mouse_speed'],
                    detection['avg_typing_speed'],
                    detection['tab_switch_rate'],
                    detection['mouse_click_rate'],
                    detection['keyboard_error_rate'],
                    detection['active_window_duration']
                ])
        except Exception as e:
            print(f"Logging error: {e}")
    
    def start(self):
        """Start the monitoring (simulation mode)"""
        self.is_running = True
        print(f"Started cloud simulation monitor with model: {self.model_name}")
    
    def stop(self):
        """Stop the monitoring"""
        self.is_running = False
        print("Stopped cloud simulation monitor")


class CloudBotSimulator:
    """Bot behavior simulator for cloud environments"""
    
    def __init__(self, duration_sec=15, step_interval=0.5):
        self.duration_sec = duration_sec
        self.step_interval = step_interval
        self.is_running = False
    
    def run(self):
        """Run bot simulation by modifying global state"""
        self.is_running = True
        start_time = time.time()
        
        print(f"🤖 Starting bot simulation for {self.duration_sec} seconds...")
        
        # Simulate bot behavior for the specified duration
        while time.time() - start_time < self.duration_sec and self.is_running:
            time.sleep(self.step_interval)
        
        self.is_running = False
        print("🤖 Bot simulation completed")


def load_best_model_and_meta():
    """
    Load the best available model for cloud deployment
    Returns a simple demo model if no trained models are available
    """
    try:
        import joblib
        
        # Try to load models from models directory
        model_files = {
            'RandomForest': 'models/rf_model.joblib',
            'XGBoost': 'models/xgb_model.joblib',
            'IsolationForest': 'models/iso_model.joblib'
        }
        
        # Try to load any available model
        for model_name, model_path in model_files.items():
            if os.path.exists(model_path):
                try:
                    model = joblib.load(model_path)
                    print(f"✅ Loaded {model_name} model from {model_path}")
                    
                    # Try to load scaler
                    scaler_path = model_path.replace('_model.joblib', '_scaler.joblib')
                    scaler = None
                    if os.path.exists(scaler_path):
                        scaler = joblib.load(scaler_path)
                        print(f"✅ Loaded scaler from {scaler_path}")
                    
                    return model_name, model, scaler, None
                    
                except Exception as e:
                    print(f"Failed to load {model_name}: {e}")
                    continue
        
        # If no models found, create a simple demo classifier
        print("ℹ️ No trained models found, creating demo classifier...")
        from sklearn.ensemble import RandomForestClassifier
        
        # Create and train a simple demo model with random data
        demo_model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        # Generate some dummy training data
        X_demo = np.random.rand(100, 6)  # 6 features
        y_demo = np.random.randint(0, 2, 100)  # Binary labels
        
        demo_model.fit(X_demo, y_demo)
        
        print("✅ Created demo RandomForest model")
        return "Demo_RandomForest", demo_model, None, None
        
    except ImportError:
        print("❌ Required libraries not available")
        raise Exception("Failed to load or create model")


# Alias for backwards compatibility
RealTimeMonitor = CloudRealTimeMonitor
BotSimulator = CloudBotSimulator

if __name__ == "__main__":
    print("🔒 AuthAI Cloud Core Module Test")
    
    # Test model loading
    try:
        model_name, model, scaler, ae_meta = load_best_model_and_meta()
        print(f"✅ Successfully loaded model: {model_name}")
        
        # Test monitor
        monitor = CloudRealTimeMonitor(model_name, model, scaler, ae_meta)
        monitor.start()
        
        # Run a few detections
        for i in range(3):
            detection = monitor.run_detection_once()
            if detection:
                print(f"Detection {i+1}: {detection['prediction']} (score: {detection['score']:.3f})")
            time.sleep(1)
        
        monitor.stop()
        print("✅ Cloud core module test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
