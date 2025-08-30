# demand_agent_gpt4.py - Enhanced with Direct OpenAI GPT-4
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import requests
from typing import Dict, List, Optional

class DemandAgent:
    def __init__(self, excel_file_path: str, openai_api_key: str = None):
        """Initialize GPT-4 Enhanced Demand Agent"""
        self.excel_file_path = excel_file_path
        self.openai_api_key = "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"
        self._load_data()
        
        if self.openai_api_key:
            print("✅ Demand Agent: GPT-4 integration enabled")
        else:
            print("🔄 Demand Agent: Using traditional analysis (no GPT-4)")
    
    def _load_data(self):
        """Load historical sales and seasonal data"""
        try:
            self.historical_sales = pd.read_excel(self.excel_file_path, sheet_name='Historical_Sales')
            self.seasonal_demand = pd.read_excel(self.excel_file_path, sheet_name='Seasonal_Demand')
            self.historical_sales['Date'] = pd.to_datetime(self.historical_sales['Date'])
            print("✅ Demand Agent: Data loaded successfully")
        except Exception as e:
            print(f"❌ Demand Agent: Error loading data - {e}")
            self.historical_sales = pd.DataFrame()
            self.seasonal_demand = pd.DataFrame()
    
    def _call_openai_gpt4(self, system_message: str, user_message: str) -> str:
        """Direct OpenAI GPT-4 API call"""
        if not self.openai_api_key:
            return "GPT-4 not available"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"⚠️ OpenAI API Error: {response.status_code}")
                return "GPT-4 analysis unavailable"
                
        except Exception as e:
            print(f"⚠️ GPT-4 call failed: {e}")
            return "GPT-4 analysis unavailable"
    
    def analyze_demand_with_gpt4(self, location: str, product: str, 
                                target_date: str = None, user_context: str = "") -> Dict:
        """Enhanced demand analysis with GPT-4"""
        
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get traditional analysis first
        traditional_analysis = self.analyze_demand(location, product, target_date)
        
        # Enhance with GPT-4 if available
        if self.openai_api_key and user_context:
            try:
                system_prompt = """You are an expert demand analyst for Indian street vendors. 
                Analyze demand data and provide practical insights in Hindi-English mix that vendors understand.
                Focus on actionable advice considering local market conditions, seasonal patterns, and customer behavior."""
                
                user_prompt = f"""Analyze demand for {product} in {location} on {target_date}.
                
                Data Analysis:
                - Demand Score: {traditional_analysis.get('demand_score', 5)}/10
                - Predicted Sales: {traditional_analysis.get('predicted_sales', 30)} units
                - Seasonal Factor: {traditional_analysis.get('seasonal_factor', 1.0)}x
                - Trend: {traditional_analysis.get('trend', 'Stable')}
                
                Vendor Context: {user_context}
                
                Provide specific recommendations for selling strategy and market opportunities."""
                
                gpt4_insights = self._call_openai_gpt4(system_prompt, user_prompt)
                
                # Enhance analysis with GPT-4 insights
                traditional_analysis['gpt4_insights'] = gpt4_insights
                traditional_analysis['ai_recommendation'] = self._extract_key_recommendation(gpt4_insights)
                traditional_analysis['selling_strategy'] = self._extract_selling_strategy(gpt4_insights)
                
            except Exception as e:
                print(f"⚠️ GPT-4 enhancement failed: {e}")
        
        return traditional_analysis
    
    def analyze_demand(self, location: str, product: str, target_date: str = None) -> Dict:
        """Traditional demand analysis"""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Filter historical data
            filtered_data = self.historical_sales[
                (self.historical_sales['Location'] == location) & 
                (self.historical_sales['Product'] == product)
            ].copy()
            
            if filtered_data.empty:
                return self._generate_fallback_analysis(location, product, target_date)
            
            # Calculate metrics
            avg_daily_sales = filtered_data['Units_Sold'].mean()
            recent_data = filtered_data.tail(30)
            recent_avg = recent_data['Units_Sold'].mean()
            seasonal_factor = self._get_seasonal_factor(product, target_date)
            
            # Demand prediction
            final_prediction = max(0, int(avg_daily_sales * seasonal_factor))
            demand_score = min(10, max(1, int((final_prediction / max(avg_daily_sales, 1)) * 5)))
            
            trend = "📈 Rising" if recent_avg > avg_daily_sales else "📉 Declining" if recent_avg < avg_daily_sales else "➡️ Stable"
            
            return {
                'location': location,
                'product': product,
                'target_date': target_date,
                'demand_score': demand_score,
                'predicted_sales': final_prediction,
                'historical_average': int(avg_daily_sales),
                'recent_average': int(recent_avg),
                'seasonal_factor': round(seasonal_factor, 2),
                'trend': trend,
                'confidence': 'High',
                'recommendation': self._generate_recommendation(demand_score, trend)
            }
            
        except Exception as e:
            return {'error': f"Demand analysis error: {str(e)}"}
    
    def _get_seasonal_factor(self, product: str, target_date: str) -> float:
        """Calculate seasonal adjustment factor"""
        try:
            month = datetime.strptime(target_date, '%Y-%m-%d').month
            seasonal_data = self.seasonal_demand[
                (self.seasonal_demand['Product'] == product) & 
                (self.seasonal_demand['Month'] == month)
            ]
            
            if not seasonal_data.empty:
                return float(seasonal_data['Demand_Index'].iloc[0])
            else:
                # Fallback seasonal logic
                if product in ['Cold Drinks', 'Ice Cream', 'Fresh Fruits']:
                    return 1.5 if 4 <= month <= 8 else 0.8
                elif product in ['Tea', 'Hot Snacks']:
                    return 1.4 if month in [11, 12, 1, 2] else 0.9
                else:
                    return 1.0
        except:
            return 1.0
    
    def _generate_fallback_analysis(self, location: str, product: str, target_date: str) -> Dict:
        """Generate fallback analysis"""
        fallback_sales = {
            'Cold Drinks': 45, 'Tea': 60, 'Samosa': 35,
            'Ice Cream': 25, 'Fresh Fruits': 40, 'Snacks': 50
        }
        
        base_sales = fallback_sales.get(product, 30)
        seasonal_factor = self._get_seasonal_factor(product, target_date)
        predicted_sales = int(base_sales * seasonal_factor)
        
        return {
            'location': location,
            'product': product,
            'target_date': target_date,
            'demand_score': 6,
            'predicted_sales': predicted_sales,
            'historical_average': base_sales,
            'recent_average': base_sales,
            'seasonal_factor': seasonal_factor,
            'trend': "➡️ Stable",
            'confidence': "Low",
            'recommendation': "Medium Priority",
            'note': "Prediction based on market averages"
        }
    
    def _generate_recommendation(self, demand_score: int, trend: str) -> str:
        """Generate business recommendation"""
        if demand_score >= 8:
            return "🔥 High Priority - Strong demand expected!"
        elif demand_score >= 6:
            return "✅ Medium Priority - Good opportunity"
        elif demand_score >= 4:
            return "⚠️ Low Priority - Consider alternatives"
        else:
            return "❌ Avoid - Very low demand predicted"
    
    def _extract_key_recommendation(self, gpt4_response: str) -> str:
        """Extract key recommendation from GPT-4 response"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'recommend' in line.lower() or 'suggest' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 enhanced recommendation available"
    
    def _extract_selling_strategy(self, gpt4_response: str) -> str:
        """Extract selling strategy from GPT-4 response"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['strategy', 'sell', 'timing', 'location']):
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 selling strategy available"
    
    def get_location_summary(self, location: str, target_date: str = None) -> Dict:
        """Get comprehensive location summary"""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        products = ['Cold Drinks', 'Tea', 'Samosa', 'Ice Cream', 'Fresh Fruits', 'Snacks']
        summaries = []
        
        for product in products:
            analysis = self.analyze_demand(location, product, target_date)
            if 'error' not in analysis:
                summaries.append({
                    'product': product,
                    'demand_score': analysis['demand_score'],
                    'predicted_sales': analysis['predicted_sales'],
                    'recommendation': analysis['recommendation']
                })
        
        summaries.sort(key=lambda x: x['demand_score'], reverse=True)
        
        return {
            'location': location,
            'date': target_date,
            'top_products': summaries[:3],
            'all_products': summaries
        }
