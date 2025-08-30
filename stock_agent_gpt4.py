# stock_agent_gpt4.py - Enhanced Master Orchestrator with GPT-4
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import requests
from typing import Dict, List, Optional

class StockAgent:
    def __init__(self, demand_agent, weather_agent, profitability_agent, openai_api_key: str = None):
        """Initialize GPT-4 Enhanced Stock Agent"""
        self.demand_agent = demand_agent
        self.weather_agent = weather_agent
        self.profitability_agent = profitability_agent
        self.openai_api_key = "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"
        
        # Business constraints
        self.max_products_per_recommendation = 3
        self.min_roi_threshold = 15.0
        self.max_risk_threshold = 8.0
        
        if self.openai_api_key:
            print("✅ Stock Agent: GPT-4 Master Orchestrator initialized")
        else:
            print("🔄 Stock Agent: Using traditional orchestration")
    
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
                "temperature": 0.4,
                "max_tokens": 1500
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
    
    def synthesize_recommendations_with_gpt4(self, location: str, budget: float,
                                           date: str = None, user_message: str = "") -> Dict:
        """GPT-4 enhanced recommendation synthesis"""
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            print(f"🤖 GPT-4 Stock Agent: Orchestrating for {location} (₹{budget})")
            
            # Step 1: Gather insights from all agents
            print("📊 Consulting Demand Agent...")
            demand_summary = self.demand_agent.get_location_summary(location, date)
            top_demand_products = [p['product'] for p in demand_summary['top_products']]
            
            print("🌤️ Consulting Weather Agent...")
            weather_data = self.weather_agent.fetch_current_weather("Hyderabad")
            if self.weather_agent.openai_api_key and user_message:
                weather_analysis = self.weather_agent.analyze_weather_impact_with_gpt4(weather_data, user_message)
            else:
                weather_analysis = self.weather_agent.analyze_weather_impact(weather_data)
            
            weather_boost = weather_analysis.get('recommendations', {}).get('weather_boost', 1.0)
            weather_products = weather_analysis.get('recommendations', {}).get('high_demand', [])
            
            # Step 2: Analyze profitability for candidate products
            print("💰 Consulting Profitability Agent...")
            candidate_products = list(set(top_demand_products + weather_products))
            if not candidate_products:
                candidate_products = ['Cold Drinks', 'Tea', 'Samosa', 'Ice Cream', 'Fresh Fruits']
            
            profitability_analyses = {}
            budget_per_product = budget / min(len(candidate_products), self.max_products_per_recommendation)
            
            for product in candidate_products[:5]:
                if self.profitability_agent.openai_api_key and user_message:
                    prof_analysis = self.profitability_agent.analyze_profitability_with_gpt4(
                        product, location, budget_per_product, user_message
                    )
                else:
                    prof_analysis = self.profitability_agent.analyze_profitability(
                        product, location, budget_per_product
                    )
                
                if prof_analysis.get('success') and prof_analysis['roi_pct'] >= self.min_roi_threshold:
                    profitability_analyses[product] = prof_analysis
            
            # Step 3: GPT-4 intelligent synthesis
            if self.openai_api_key and user_message:
                print("🧠 GPT-4 Master Synthesis...")
                ai_recommendations = self._gpt4_master_synthesis(
                    location, budget, date, user_message,
                    demand_summary, weather_analysis, profitability_analyses
                )
            else:
                ai_recommendations = self._traditional_synthesis(
                    location, budget, date, demand_summary, weather_analysis, profitability_analyses
                )
            
            return ai_recommendations
            
        except Exception as e:
            print(f"❌ Stock Agent Synthesis Error: {e}")
            return {'error': f"Synthesis error: {str(e)}", 'success': False}
    
    def _gpt4_master_synthesis(self, location: str, budget: float, date: str,
                              user_message: str, demand_data: Dict, 
                              weather_data: Dict, profitability_data: Dict) -> Dict:
        """Use GPT-4 for intelligent master synthesis"""
        
        try:
            system_prompt = """You are the Master AI Business Advisor for "Commerce in a Prompt for Bharat" - 
            the most advanced AI system for Indian street vendors.
            
            You have deep expertise in:
            - Indian street vending business dynamics
            - Local market conditions and customer behavior
            - Weather impact on sales patterns
            - Financial optimization for small businesses
            - Cultural and seasonal factors
            
            Your role is to synthesize insights from demand analysis, weather conditions, and profitability calculations
            to provide the most intelligent, practical, and profitable recommendations.
            
            Provide specific, actionable recommendations that street vendors can implement immediately for maximum success."""
            
            # Prepare comprehensive context
            user_context = f"""MASTER BUSINESS SYNTHESIS REQUEST:
            
Vendor Details:
- Location: {location}
- Budget: ₹{budget}
- Date: {date}
- Vendor Message: "{user_message}"

DEMAND INTELLIGENCE:
Top products by demand: {[f"{p['product']} ({p['demand_score']}/10)" for p in demand_data.get('top_products', [])]}

WEATHER INTELLIGENCE:
Current conditions: {weather_data.get('weather_summary', {}).get('condition', 'Unknown')} at {weather_data.get('weather_summary', {}).get('temperature', 'N/A')}°C
Weather-boosted products: {weather_data.get('recommendations', {}).get('high_demand', [])}
Weather boost factor: {weather_data.get('recommendations', {}).get('weather_boost', 1.0)}x

PROFITABILITY INTELLIGENCE:
{self._format_profitability_for_gpt4(profitability_data)}

SYNTHESIS REQUIREMENTS:
Based on the vendor's message "{user_message}", provide:
1. Top 3 product recommendations with specific rationale
2. Optimal budget allocation strategy
3. Weather-adapted selling strategy
4. Risk assessment and mitigation
5. Expected daily profit projections
6. Implementation timeline and tips

Focus on practical, immediately actionable advice in Hindi-English mix that the vendor can understand and implement."""
            
            gpt4_response = self._call_openai_gpt4(system_prompt, user_context)
            
            # Process GPT-4 recommendations into structured format
            recommendations = self._process_gpt4_master_recommendations(
                gpt4_response, profitability_data, weather_data, budget
            )
            
            return {
                'location': location,
                'date': date,
                'budget': budget,
                'gpt4_master_synthesis': gpt4_response,
                'final_recommendations': recommendations['products'],
                'business_strategy': recommendations['strategy'],
                'implementation_plan': recommendations['implementation'],
                'weather_conditions': weather_data.get('weather_summary', {}),
                'market_analysis': {
                    'demand_products': [p['product'] for p in demand_data.get('top_products', [])],
                    'weather_products': weather_data.get('recommendations', {}).get('high_demand', []),
                    'weather_boost': weather_data.get('recommendations', {}).get('weather_boost', 1.0)
                },
                'success': True,
                'ai_powered': True,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ GPT-4 master synthesis failed: {e}")
            return self._traditional_synthesis(location, budget, date, demand_data, weather_data, profitability_data)
    
    def _format_profitability_for_gpt4(self, prof_data: Dict) -> str:
        """Format profitability data for GPT-4"""
        formatted = []
        for product, analysis in prof_data.items():
            formatted.append(f"- {product}: ROI {analysis.get('roi_pct', 0):.1f}%, Daily Profit ₹{analysis.get('daily_profit', 0):.0f}, Risk {analysis.get('risk_level', 'Unknown')}")
        return '\n'.join(formatted)
    
    def _process_gpt4_master_recommendations(self, gpt4_content: str, prof_data: Dict, 
                                           weather_data: Dict, budget: float) -> Dict:
        """Process GPT-4 master response into structured recommendations"""
        
        # Extract product recommendations
        products_mentioned = []
        for product in prof_data.keys():
            if product.lower() in gpt4_content.lower():
                products_mentioned.append(product)
        
        # Select and structure final products
        final_products = []
        remaining_budget = budget
        
        for product in products_mentioned[:3]:
            if product in prof_data and remaining_budget >= prof_data[product]['cost_per_unit'] * 10:
                analysis = prof_data[product]
                affordable_units = min(
                    int(remaining_budget / analysis['cost_per_unit']),
                    analysis['units_affordable']
                )
                
                investment = affordable_units * analysis['cost_per_unit']
                weather_boost = weather_data.get('recommendations', {}).get('weather_boost', 1.0)
                
                final_products.append({
                    'product': product,
                    'rank': len(final_products) + 1,
                    'units_to_buy': affordable_units,
                    'investment_amount': investment,
                    'expected_roi': analysis['roi_pct'],
                    'daily_profit_estimate': round(analysis['daily_profit'] * weather_boost, 2),
                    'selling_price': analysis['selling_price'],
                    'risk_level': analysis['risk_level'],
                    'weather_boost': weather_boost,
                    'gpt4_rationale': self._extract_product_rationale(gpt4_content, product)
                })
                
                remaining_budget -= investment
        
        # Generate strategy and implementation
        total_investment = sum(p['investment_amount'] for p in final_products)
        total_daily_profit = sum(p['daily_profit_estimate'] for p in final_products)
        
        strategy = {
            'total_investment': round(total_investment, 2),
            'expected_daily_profit': round(total_daily_profit, 2),
            'monthly_roi': round((total_daily_profit * 30 / total_investment) * 100, 1) if total_investment > 0 else 0,
            'success_probability': 'High' if total_daily_profit > 400 else 'Medium',
            'gpt4_strategy': self._extract_strategy_summary(gpt4_content)
        }
        
        implementation = {
            'timeline': self._extract_timeline(gpt4_content),
            'selling_tips': self._extract_selling_tips(gpt4_content),
            'risk_mitigation': self._extract_risk_mitigation(gpt4_content)
        }
        
        return {
            'products': final_products,
            'strategy': strategy,
            'implementation': implementation
        }
    
    def _extract_product_rationale(self, gpt4_content: str, product: str) -> str:
        """Extract GPT-4 rationale for specific product"""
        sentences = gpt4_content.split('.')
        for sentence in sentences:
            if product.lower() in sentence.lower() and len(sentence.strip()) < 200 and len(sentence.strip()) > 20:
                return sentence.strip()
        return f"GPT-4 recommends {product} based on comprehensive analysis"
    
    def _extract_strategy_summary(self, gpt4_content: str) -> str:
        """Extract strategy summary"""
        lines = gpt4_content.split('\n')
        for line in lines:
            if 'strategy' in line.lower() or 'approach' in line.lower():
                if len(line.strip()) < 300 and len(line.strip()) > 20:
                    return line.strip()
        return "GPT-4 comprehensive strategy available"
    
    def _extract_timeline(self, gpt4_content: str) -> str:
        """Extract implementation timeline"""
        lines = gpt4_content.split('\n')
        for line in lines:
            if 'timeline' in line.lower() or 'time' in line.lower():
                if len(line.strip()) < 200 and len(line.strip()) > 20:
                    return line.strip()
        return "GPT-4 implementation timeline available"
    
    def _extract_selling_tips(self, gpt4_content: str) -> List[str]:
        """Extract selling tips"""
        tips = []
        lines = gpt4_content.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['tip', 'sell', 'customer', 'location']):
                if len(line.strip()) < 150 and len(line.strip()) > 20:
                    tips.append(line.strip())
        return tips[:3]
    
    def _extract_risk_mitigation(self, gpt4_content: str) -> str:
        """Extract risk mitigation advice"""
        lines = gpt4_content.split('\n')
        for line in lines:
            if 'risk' in line.lower() or 'safe' in line.lower():
                if len(line.strip()) < 200 and len(line.strip()) > 20:
                    return line.strip()
        return "GPT-4 risk management advice available"
    
    def _traditional_synthesis(self, location: str, budget: float, date: str,
                             demand_data: Dict, weather_data: Dict, prof_data: Dict) -> Dict:
        """Traditional synthesis fallback"""
        
        # Score and select products
        product_scores = {}
        for product, analysis in prof_data.items():
            demand_score = 0
            for p in demand_data.get('top_products', []):
                if p['product'] == product:
                    demand_score = p['demand_score']
                    break
            
            weather_boost = 1.0
            if product in weather_data.get('recommendations', {}).get('high_demand', []):
                weather_boost = weather_data.get('recommendations', {}).get('weather_boost', 1.0)
            
            composite_score = (analysis['roi_pct'] * 0.4) + (demand_score * 10 * 0.3) + ((weather_boost - 1) * 100 * 0.3)
            product_scores[product] = {
                'score': composite_score,
                'analysis': analysis,
                'weather_boost': weather_boost
            }
        
        # Select top products
        sorted_products = sorted(product_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        final_products = []
        remaining_budget = budget
        
        for product, data in sorted_products[:3]:
            analysis = data['analysis']
            if remaining_budget >= analysis['cost_per_unit'] * 10:
                affordable_units = min(
                    int(remaining_budget / analysis['cost_per_unit']),
                    analysis['units_affordable']
                )
                
                investment = affordable_units * analysis['cost_per_unit']
                
                final_products.append({
                    'product': product,
                    'rank': len(final_products) + 1,
                    'units_to_buy': affordable_units,
                    'investment_amount': investment,
                    'expected_roi': analysis['roi_pct'],
                    'daily_profit_estimate': round(analysis['daily_profit'] * data['weather_boost'], 2),
                    'selling_price': analysis['selling_price'],
                    'risk_level': analysis['risk_level'],
                    'weather_boost': data['weather_boost']
                })
                
                remaining_budget -= investment
        
        total_investment = sum(p['investment_amount'] for p in final_products)
        total_daily_profit = sum(p['daily_profit_estimate'] for p in final_products)
        
        return {
            'location': location,
            'date': date,
            'budget': budget,
            'final_recommendations': final_products,
            'business_strategy': {
                'total_investment': round(total_investment, 2),
                'expected_daily_profit': round(total_daily_profit, 2),
                'monthly_roi': round((total_daily_profit * 30 / total_investment) * 100, 1) if total_investment > 0 else 0
            },
            'success': True,
            'ai_powered': False
        }
    
    def generate_whatsapp_response_with_gpt4(self, location: str, budget: float,
                                           date: str = None, user_message: str = "") -> str:
        """Generate GPT-4 enhanced WhatsApp response"""
        
        analysis = self.synthesize_recommendations_with_gpt4(location, budget, date, user_message)
        
        if not analysis.get('success'):
            return f"🤖 Sorry bhai, technical issue: {analysis.get('error', 'Unknown error')}"
        
        recs = analysis.get('final_recommendations', [])
        strategy = analysis.get('business_strategy', {})
        weather = analysis.get('weather_conditions', {})
        
        if not recs:
            return f"""🤖 **GPT-4 Commerce Assistant - {location}**
            
❌ Current market conditions mein profitable options nahi mil rahe with ₹{budget} budget.

💡 **GPT-4 Suggestions:**
• Budget increase karo minimum ₹1500+
• Different location try karo
• Weather conditions better hone ka wait karo

📞 Try again with updated parameters!"""
        
        # Build GPT-4 enhanced response
        response = f"""🤖 **Margadarshak AI - {location}**
📅 Date: {date or datetime.now().strftime('%Y-%m-%d')}
💰 Budget: ₹{budget}
🌤️ Weather: {weather.get('condition', 'Clear').title()} ({weather.get('temperature', 'N/A')}°C)


🏆 **Margadarshak AI Suggests:**
"""
        
        for rec in recs:
            emoji = "🥇" if rec['rank'] == 1 else "🥈" if rec['rank'] == 2 else "🥉"
            response += f"""
{emoji} **{rec['product']}**
• Quantity: {rec['units_to_buy']} units
• Investment: ₹{rec['investment_amount']}
• Daily Profit: ₹{rec['daily_profit_estimate']} ({rec['weather_boost']:.1f}x weather boost)
• ROI: {rec['expected_roi']}%
• Risk: {rec['risk_level']}
• Margadarshak AI Logic: {rec.get('gpt4_rationale', 'AI-optimized selection')[:100]}...
"""
        
        response += f"""
📊 **Margadarshak AI Business Strategy:**
• Total Investment: ₹{strategy.get('total_investment', 0)}
• Expected Daily Profit: ₹{strategy.get('expected_daily_profit', 0)}
• Monthly ROI: {strategy.get('monthly_roi', 0)}%
• Success Probability: {strategy.get('success_probability', 'Medium')}

🧠 **Margadarshak AI Master Insights:**
{analysis.get('gpt4_master_synthesis', 'Advanced AI analysis completed')[:250]}...

⏰ **Optimal Hours:** 10:00 AM - 7:00 PM
🎯 **Best Locations:** High footfall areas, office complexes
📱 **Implementation:** {analysis.get('implementation_plan', {}).get('timeline', 'Start immediately')}

💡 **Margadarshak AI Pro Tips:**
• Focus 70% effort on top 2 products
• Monitor weather changes for demand optimization
• Track daily performance for continuous improvement"""
        
        return response
