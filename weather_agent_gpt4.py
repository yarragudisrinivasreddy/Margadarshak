# weather_agent_gpt4.py - Enhanced with Direct OpenAI GPT-4
import requests
import json
from datetime import datetime
import random
import os
from typing import Dict, List, Optional

class WeatherAgent:
    def __init__(self, weather_api_key: str = None, openai_api_key: str = None):
        """Initialize GPT-4 Enhanced Weather Agent"""
        self.weather_api_key = "c485c07fe2d89be6f9222b9878a2b782"
        self.openai_api_key = "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"
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.use_weather_fallback = "c485c07fe2d89be6f9222b9878a2b782"
        
        if self.openai_api_key:
            print("✅ Weather Agent: GPT-4 integration enabled")
        else:
            print("🔄 Weather Agent: Using traditional analysis")
        
        if self.use_weather_fallback:
            print("🔄 Weather Agent: Using fallback weather data")
        else:
            print("✅ Weather Agent: Using OpenWeather API")
        
        # Weather-product correlation matrix
        self.weather_products = {
            'hot': {
                'boost': ['Cold Drinks', 'Ice Cream', 'Fresh Fruits'],
                'reduce': ['Tea', 'Hot Snacks'],
                'multiplier': 1.6
            },
            'cold': {
                'boost': ['Tea', 'Hot Snacks', 'Samosa'],
                'reduce': ['Cold Drinks', 'Ice Cream'],
                'multiplier': 1.4
            },
            'rainy': {
                'boost': ['Umbrellas', 'Raincoats', 'Tea', 'Hot Snacks'],
                'reduce': ['Ice Cream', 'Fresh Fruits'],
                'multiplier': 1.8
            },
            'humid': {
                'boost': ['Cold Drinks', 'Fresh Fruits'],
                'reduce': ['Hot Snacks'],
                'multiplier': 1.3
            }
        }
    
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
                "temperature": 0.2,
                "max_tokens": 800
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
                return "GPT-4 analysis unavailable"
                
        except Exception as e:
            return "GPT-4 analysis unavailable"
    
    def fetch_current_weather(self, city: str = "Hyderabad") -> Dict:
        """Fetch weather data with fallback"""
        if self.use_weather_fallback:
            return self._generate_fallback_weather(city)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},IN",
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'weather_main': data['weather'][0]['main'].lower(),
                    'weather_description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'city': data['name'],
                    'source': 'OpenWeather API'
                }
            else:
                return self._generate_fallback_weather(city)
                
        except Exception as e:
            return self._generate_fallback_weather(city)
    
    def _generate_fallback_weather(self, city: str = "Hyderabad") -> Dict:
        """Generate realistic weather data for Hyderabad"""
        current_month = datetime.now().month
        current_hour = datetime.now().hour
        
        # Seasonal patterns for Hyderabad
        if 3 <= current_month <= 6:  # Summer
            base_temp = random.uniform(32, 42)
            humidity = random.uniform(40, 70)
            conditions = ['clear sky', 'few clouds', 'haze']
        elif 7 <= current_month <= 9:  # Monsoon
            base_temp = random.uniform(25, 32)
            humidity = random.uniform(70, 90)
            conditions = ['moderate rain', 'light rain', 'overcast clouds']
        else:  # Winter/Post-monsoon
            base_temp = random.uniform(20, 30)
            humidity = random.uniform(50, 75)
            conditions = ['clear sky', 'few clouds', 'mist']
        
        # Daily variation
        if 6 <= current_hour <= 18:
            temperature = base_temp + random.uniform(-2, 3)
        else:
            temperature = base_temp - random.uniform(3, 8)
        
        weather_desc = random.choice(conditions)
        weather_main = 'rain' if 'rain' in weather_desc else 'clear'
        
        return {
            'success': True,
            'temperature': round(temperature, 1),
            'feels_like': round(temperature + random.uniform(-2, 4), 1),
            'humidity': int(humidity),
            'weather_main': weather_main,
            'weather_description': weather_desc,
            'wind_speed': round(random.uniform(2, 12), 1),
            'city': city,
            'source': 'Fallback (Simulated)'
        }
    
    def analyze_weather_impact_with_gpt4(self, weather_data: Dict, user_context: str = "") -> Dict:
        """Enhanced weather analysis with GPT-4"""
        
        # Get traditional analysis first
        traditional_analysis = self.analyze_weather_impact(weather_data)
        
        # Enhance with GPT-4 if available
        if self.openai_api_key and user_context and traditional_analysis.get('success') != False:
            try:
                weather_summary = traditional_analysis.get('weather_summary', {})
                recommendations = traditional_analysis.get('recommendations', {})
                
                system_prompt = """You are a weather-business expert for Indian street vendors. 
                Analyze weather conditions and provide practical business advice in Hindi-English mix.
                Consider Indian climate patterns, local customer behavior, and street vending dynamics."""
                
                user_prompt = f"""Weather Business Analysis for Street Vendor:
                
                Current Conditions:
                - Temperature: {weather_summary.get('temperature', 'N/A')}°C
                - Humidity: {weather_summary.get('humidity', 'N/A')}%
                - Weather: {weather_summary.get('condition', 'N/A')}
                
                Traditional Analysis:
                - High Demand Products: {recommendations.get('high_demand', [])}
                - Weather Boost Factor: {recommendations.get('weather_boost', 1.0)}x
                
                Vendor Context: {user_context}
                
                Provide specific advice on:
                1. Best products to sell in these conditions
                2. Selling locations and timing strategies
                3. Customer behavior insights
                4. Risk mitigation for weather changes"""
                
                gpt4_insights = self._call_openai_gpt4(system_prompt, user_prompt)
                
                # Enhance traditional analysis
                traditional_analysis['gpt4_insights'] = gpt4_insights
                traditional_analysis['ai_selling_strategy'] = self._extract_selling_strategy(gpt4_insights)
                traditional_analysis['customer_insights'] = self._extract_customer_insights(gpt4_insights)
                traditional_analysis['location_advice'] = self._extract_location_advice(gpt4_insights)
                
            except Exception as e:
                print(f"⚠️ GPT-4 weather analysis failed: {e}")
        
        return traditional_analysis
    
    def analyze_weather_impact(self, weather_data: Dict, target_products: List[str] = None) -> Dict:
        """Traditional weather impact analysis"""
        if not weather_data.get('success'):
            return {'error': weather_data.get('error', 'Weather data unavailable')}
        
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        weather_main = weather_data['weather_main']
        weather_desc = weather_data['weather_description']
        
        # Determine conditions
        conditions = []
        if temp > 35:
            conditions.append('hot')
        elif temp < 20:
            conditions.append('cold')
        
        if humidity > 70:
            conditions.append('humid')
        
        if 'rain' in weather_main or 'rain' in weather_desc:
            conditions.append('rainy')
        
        # Calculate product impacts
        all_products = ['Cold Drinks', 'Tea', 'Samosa', 'Ice Cream', 'Fresh Fruits', 'Hot Snacks', 'Umbrellas', 'Raincoats']
        product_impacts = {}
        
        for product in (target_products or all_products):
            impact = 1.0
            reasons = []
            
            for condition in conditions:
                if condition in self.weather_products:
                    rules = self.weather_products[condition]
                    if product in rules['boost']:
                        impact *= rules['multiplier']
                        reasons.append(f"+{int((rules['multiplier']-1)*100)}% due to {condition}")
                    elif product in rules['reduce']:
                        impact *= (2 - rules['multiplier'])
                        reasons.append(f"-{int((rules['multiplier']-1)*100)}% due to {condition}")
            
            product_impacts[product] = {
                'multiplier': round(impact, 2),
                'impact': 'High' if impact > 1.4 else 'Medium' if impact > 1.1 else 'Low',
                'reasons': reasons
            }
        
        # Generate recommendations
        high_demand = [p for p, data in product_impacts.items() if data['multiplier'] > 1.3]
        low_demand = [p for p, data in product_impacts.items() if data['multiplier'] < 0.8]
        
        return {
            'weather_summary': {
                'temperature': temp,
                'humidity': humidity,
                'condition': weather_desc,
                'weather_types': conditions,
                'source': weather_data.get('source', 'Unknown')
            },
            'product_impacts': product_impacts,
            'recommendations': {
                'high_demand': high_demand[:3],
                'low_demand': low_demand[:2],
                'weather_boost': max([data['multiplier'] for data in product_impacts.values()]),
                'optimal_conditions': len([p for p in product_impacts.values() if p['multiplier'] > 1.2]) > 3
            }
        }
    
    def _extract_selling_strategy(self, gpt4_response: str) -> str:
        """Extract selling strategy from GPT-4 response"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'strategy' in line.lower() or 'sell' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 selling strategy available"
    
    def _extract_customer_insights(self, gpt4_response: str) -> str:
        """Extract customer behavior insights"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'customer' in line.lower() or 'behavior' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 customer insights available"
    
    def _extract_location_advice(self, gpt4_response: str) -> str:
        """Extract location advice from GPT-4 response"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'location' in line.lower() or 'where' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 location advice available"
    
    def get_daily_recommendation_with_gpt4(self, city: str = "Hyderabad", 
                                         target_date: str = None, user_context: str = "") -> str:
        """Get GPT-4 enhanced daily recommendation"""
        weather_data = self.fetch_current_weather(city)
        
        if not weather_data.get('success'):
            return f"❌ Weather Agent Error: {weather_data.get('error')}"
        
        if self.openai_api_key and user_context:
            analysis = self.analyze_weather_impact_with_gpt4(weather_data, user_context)
        else:
            analysis = self.analyze_weather_impact(weather_data)
        
        if 'error' in analysis:
            return f"❌ Weather Analysis Error: {analysis['error']}"
        
        weather = analysis['weather_summary']
        recs = analysis['recommendations']
        
        # Build response
        recommendation = f"""🌤️ GPT-4 ENHANCED WEATHER ANALYSIS - {weather_data['city']}
📅 Date: {target_date or datetime.now().strftime('%Y-%m-%d')}
📡 Source: {weather['source']}

🌡️ CONDITIONS:
• Temperature: {weather['temperature']}°C
• Humidity: {weather['humidity']}%
• Weather: {weather['condition'].title()}
• Impact Level: {'🔥 High' if recs['optimal_conditions'] else '⚡ Medium'}

📈 HIGH DEMAND PRODUCTS:
{chr(10).join([f'• {product} ({analysis["product_impacts"][product]["multiplier"]}x boost)' for product in recs['high_demand']]) if recs['high_demand'] else '• Standard demand for all products'}

🎯 AI STRATEGY:
• Weather Boost: {recs['weather_boost']:.1f}x demand increase
• Market Impact: {int((recs['weather_boost']-1)*100):+d}%
• Conditions: {'🔥 Excellent for sales' if recs['optimal_conditions'] else '✅ Good opportunities'}"""
        
        # Add GPT-4 insights if available
        if 'gpt4_insights' in analysis and analysis['gpt4_insights'] != "GPT-4 not available":
            recommendation += f"\n\n🤖 GPT-4 INSIGHTS:\n{analysis.get('ai_selling_strategy', 'AI-powered recommendations available')}"
        
        return recommendation
