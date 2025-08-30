# profitability_agent_gpt4.py - Enhanced with Direct OpenAI GPT-4
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import requests
from typing import Dict, List, Optional

class ProfitabilityAgent:
    def __init__(self, excel_file_path: str, openai_api_key: str = None):
        """Initialize GPT-4 Enhanced Profitability Agent"""
        self.excel_file_path = excel_file_path
        self.openai_api_key = "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"
        self._load_data()
        self._initialize_cost_database()
        
        if self.openai_api_key:
            print("✅ Profitability Agent: GPT-4 integration enabled")
        else:
            print("🔄 Profitability Agent: Using traditional analysis")
    
    def _load_data(self):
        """Load demographics data"""
        try:
            self.demographics = pd.read_excel(self.excel_file_path, sheet_name='Demographics')
            print("✅ Profitability Agent: Demographics loaded successfully")
        except Exception as e:
            print(f"❌ Profitability Agent: Error loading data - {e}")
            self.demographics = pd.DataFrame([
                {'Location': 'Begum Bazaar', 'Population': 200000, 'Median_Income': 15000},
                {'Location': 'Charminar', 'Population': 120000, 'Median_Income': 12000},
                {'Location': 'Hitech City', 'Population': 250000, 'Median_Income': 40000},
                {'Location': 'Kukatpally', 'Population': 220000, 'Median_Income': 18000},
                {'Location': 'Secunderabad', 'Population': 180000, 'Median_Income': 22000}
            ])
            print("🔄 Using fallback demographics data")
    
    def _initialize_cost_database(self):
        """Initialize comprehensive product database"""
        self.product_costs = {
            'Cold Drinks': {'cost': 15, 'selling_price': 25, 'margin': 40, 'competition_level': 'High', 'demand_stability': 'High'},
            'Tea': {'cost': 5, 'selling_price': 10, 'margin': 50, 'competition_level': 'Medium', 'demand_stability': 'Very High'},
            'Samosa': {'cost': 8, 'selling_price': 15, 'margin': 47, 'competition_level': 'Medium', 'demand_stability': 'High'},
            'Ice Cream': {'cost': 20, 'selling_price': 35, 'margin': 43, 'competition_level': 'Medium', 'demand_stability': 'Medium'},
            'Fresh Fruits': {'cost': 25, 'selling_price': 40, 'margin': 38, 'competition_level': 'High', 'demand_stability': 'Medium'},
            'Hot Snacks': {'cost': 12, 'selling_price': 20, 'margin': 40, 'competition_level': 'Medium', 'demand_stability': 'High'},
            'Umbrellas': {'cost': 150, 'selling_price': 250, 'margin': 40, 'competition_level': 'Low', 'demand_stability': 'Low'},
            'Raincoats': {'cost': 100, 'selling_price': 180, 'margin': 44, 'competition_level': 'Low', 'demand_stability': 'Low'}
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
                "temperature": 0.1,
                "max_tokens": 1200
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
    
    def analyze_profitability_with_gpt4(self, product: str, location: str, budget: float,
                                       user_context: str = "", expected_sales: int = None) -> Dict:
        """Enhanced profitability analysis with GPT-4"""
        
        # Get traditional analysis first
        traditional_analysis = self.analyze_profitability(product, location, budget, expected_sales)
        
        # Enhance with GPT-4 if available
        if self.openai_api_key and user_context and traditional_analysis.get('success'):
            try:
                system_prompt = """You are a financial advisor for Indian street vendors.
                Analyze profitability data and provide practical financial advice in Hindi-English mix.
                Focus on actionable strategies for maximizing profits, minimizing risks, and growing the business."""
                
                user_prompt = f"""Financial Analysis for Street Vendor:
                
                Business Details:
                - Product: {product}
                - Location: {location}
                - Budget: ₹{budget}
                
                Analysis Results:
                - ROI: {traditional_analysis.get('roi_pct', 0)}%
                - Daily Profit: ₹{traditional_analysis.get('daily_profit', 0)}
                - Units Affordable: {traditional_analysis.get('units_affordable', 0)}
                - Risk Level: {traditional_analysis.get('risk_level', 'Unknown')}
                
                Market Context:
                - Competition: {self.product_costs.get(product, {}).get('competition_level', 'Unknown')}
                - Demand Stability: {self.product_costs.get(product, {}).get('demand_stability', 'Unknown')}
                
                Vendor Context: {user_context}
                
                Provide specific advice on:
                1. Investment viability and expected returns
                2. Profit optimization strategies
                3. Risk management tips
                4. Business growth recommendations"""
                
                gpt4_insights = self._call_openai_gpt4(system_prompt, user_prompt)
                
                # Enhance analysis with GPT-4 insights
                traditional_analysis['gpt4_insights'] = gpt4_insights
                traditional_analysis['investment_advice'] = self._extract_investment_advice(gpt4_insights)
                traditional_analysis['optimization_tips'] = self._extract_optimization_tips(gpt4_insights)
                traditional_analysis['risk_management'] = self._extract_risk_management(gpt4_insights)
                
            except Exception as e:
                print(f"⚠️ GPT-4 profitability analysis failed: {e}")
        
        return traditional_analysis
    
    def analyze_profitability(self, product: str, location: str, budget: float,
                            expected_sales: int = None) -> Dict:
        """Traditional profitability analysis"""
        try:
            if product not in self.product_costs:
                return {'error': f"No cost data available for product: {product}"}
            
            # Get demographics
            demo_data = self.demographics[self.demographics['Location'] == location]
            if demo_data.empty:
                return {'error': f"No demographics data for location: {location}"}
            
            population = int(demo_data.iloc[0]['Population'])
            median_income = float(demo_data.iloc[0]['Median_Income'])
            
            # Get product data
            product_data = self.product_costs[product]
            cost_per_unit = float(product_data['cost'])
            selling_price = float(product_data['selling_price'])
            
            # Calculate metrics
            units_affordable = int(budget / cost_per_unit)
            market_factor = self._calculate_market_factor(population, median_income, product)
            adjusted_selling_price = self._adjust_price_for_market(
                selling_price, median_income, product_data['competition_level']
            )
            
            # Financial calculations
            total_cost = float(units_affordable * cost_per_unit)
            total_revenue = float(units_affordable * adjusted_selling_price)
            gross_profit = float(total_revenue - total_cost)
            profit_per_unit = float(adjusted_selling_price - cost_per_unit)
            profit_margin_pct = float((profit_per_unit / adjusted_selling_price) * 100)
            roi_pct = float((gross_profit / budget) * 100 if budget > 0 else 0)
            
            # Daily projections
            daily_sales_estimate = expected_sales or self._estimate_daily_sales(product, location, units_affordable)
            daily_revenue = float(daily_sales_estimate * adjusted_selling_price)
            daily_profit = float(daily_sales_estimate * profit_per_unit)
            days_to_sell = float(units_affordable / daily_sales_estimate if daily_sales_estimate > 0 else 0)
            
            # Risk assessment
            risk_score = self._calculate_risk_score(product_data, market_factor, days_to_sell)
            
            return self._convert_to_json_serializable({
                'product': product,
                'location': location,
                'budget': budget,
                'analysis_date': datetime.now().strftime('%Y-%m-%d'),
                'units_affordable': units_affordable,
                'cost_per_unit': round(cost_per_unit, 2),
                'selling_price': round(adjusted_selling_price, 2),
                'profit_per_unit': round(profit_per_unit, 2),
                'total_cost': round(total_cost, 2),
                'total_revenue': round(total_revenue, 2),
                'gross_profit': round(gross_profit, 2),
                'profit_margin_pct': round(profit_margin_pct, 1),
                'roi_pct': round(roi_pct, 1),
                'daily_sales_estimate': daily_sales_estimate,
                'daily_revenue': round(daily_revenue, 2),
                'daily_profit': round(daily_profit, 2),
                'days_to_sell_inventory': round(days_to_sell, 1),
                'market_factor': round(market_factor, 2),
                'population': population,
                'median_income': median_income,
                'competition_level': product_data['competition_level'],
                'demand_stability': product_data['demand_stability'],
                'risk_score': round(risk_score, 1),
                'risk_level': self._get_risk_level(risk_score),
                'recommendation': self._generate_recommendation(roi_pct, market_factor, risk_score),
                'success': True
            })
            
        except Exception as e:
            return {'error': f"Profitability analysis error: {str(e)}", 'success': False}
    
    def _convert_to_json_serializable(self, obj):
        """Convert numpy types to JSON serializable"""
        if isinstance(obj, dict):
            return {k: self._convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_serializable(i) for i in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif pd.isna(obj):
            return None
        else:
            return obj
    
    def _calculate_market_factor(self, population: int, median_income: float, product: str) -> float:
        """Calculate market attractiveness factor"""
        income_factor = median_income / 15000
        population_factor = population / 100000
        
        # Product-specific adjustments
        if product in ['Ice Cream', 'Mobile Accessories']:
            product_adjustment = income_factor * 1.2
        elif product in ['Tea', 'Samosa', 'Hot Snacks']:
            product_adjustment = (population_factor * 1.3 + income_factor * 0.7) / 2
        else:
            product_adjustment = 1.0
        
        base_factor = (income_factor + population_factor) / 2
        final_factor = (base_factor + product_adjustment) / 2
        
        return min(1.6, max(0.7, final_factor))
    
    def _adjust_price_for_market(self, base_price: float, median_income: float, competition: str) -> float:
        """Adjust selling price based on market conditions"""
        income_multiplier = 1.1 if median_income > 25000 else 0.95 if median_income < 12000 else 1.0
        competition_multiplier = 0.95 if competition == 'High' else 1.05 if competition == 'Low' else 1.0
        
        adjusted_price = base_price * income_multiplier * competition_multiplier
        return round(adjusted_price, 2)
    
    def _estimate_daily_sales(self, product: str, location: str, inventory: int) -> int:
        """Estimate daily sales"""
        base_sales = {
            'Cold Drinks': 45, 'Tea': 60, 'Samosa': 35, 'Ice Cream': 25,
            'Fresh Fruits': 40, 'Hot Snacks': 50, 'Umbrellas': 5, 'Raincoats': 3
        }
        
        base = base_sales.get(product, 30)
        location_multipliers = {
            'Hitech City': 1.2, 'Secunderabad': 1.1, 'Kukatpally': 1.0,
            'Begum Bazaar': 1.3, 'Charminar': 0.9
        }
        
        multiplier = location_multipliers.get(location, 1.0)
        estimated_daily = int(base * multiplier)
        max_daily = max(1, int(inventory * 0.2))
        
        return min(estimated_daily, max_daily)
    
    def _calculate_risk_score(self, product_data: Dict, market_factor: float, days_to_sell: float) -> float:
        """Calculate risk score (0-10)"""
        risk_score = 5.0
        
        if market_factor < 0.9:
            risk_score += 2.0
        elif market_factor > 1.3:
            risk_score -= 1.5
        
        if days_to_sell > 30:
            risk_score += 3.0
        elif days_to_sell > 14:
            risk_score += 1.5
        elif days_to_sell < 7:
            risk_score -= 1.0
        
        if product_data['competition_level'] == 'High':
            risk_score += 1.0
        elif product_data['competition_level'] == 'Low':
            risk_score -= 0.5
        
        return min(10.0, max(0.0, risk_score))
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level"""
        if risk_score <= 3.0:
            return "Low Risk"
        elif risk_score <= 6.0:
            return "Medium Risk"
        else:
            return "High Risk"
    
    def _generate_recommendation(self, roi: float, market_factor: float, risk_score: float) -> str:
        """Generate recommendation"""
        if roi > 40 and risk_score < 4 and market_factor > 1.2:
            return "🔥 Excellent Investment - High ROI with low risk"
        elif roi > 30 and risk_score < 6:
            return "✅ Highly Recommended - Strong profitability"
        elif roi > 20:
            return "👍 Good Investment - Solid returns"
        elif roi > 10:
            return "⚠️ Moderate Investment - Consider carefully"
        else:
            return "❌ Not Recommended - Poor profitability"
    
    def _extract_investment_advice(self, gpt4_response: str) -> str:
        """Extract investment advice from GPT-4 response"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'investment' in line.lower() or 'invest' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 investment advice available"
    
    def _extract_optimization_tips(self, gpt4_response: str) -> List[str]:
        """Extract optimization tips"""
        tips = []
        lines = gpt4_response.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['optimize', 'increase', 'maximize', 'improve']):
                if len(line.strip()) > 20 and len(line.strip()) < 150:
                    tips.append(line.strip())
        return tips[:3]
    
    def _extract_risk_management(self, gpt4_response: str) -> str:
        """Extract risk management advice"""
        lines = gpt4_response.split('\n')
        for line in lines:
            if 'risk' in line.lower() or 'safe' in line.lower():
                if len(line.strip()) > 20 and len(line.strip()) < 200:
                    return line.strip()
        return "GPT-4 risk management advice available"
