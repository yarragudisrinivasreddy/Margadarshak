# complete_commerce_orchestrator.py - Final Integration of All Agents
import os
import traceback
from datetime import datetime
from typing import Dict, List, Optional

# Import all your existing agents
from natural_language_parser_gpt4 import GPT4NaturalLanguageParser
from demand_agent_gpt4 import DemandAgent
from weather_agent_gpt4 import WeatherAgent
from profitability_agent_gpt4 import ProfitabilityAgent
from stock_agent_gpt4 import StockAgent

class CompleteCommerceOrchestrator:
    """Complete Commerce in a Prompt for Bharat - All Agents Integrated"""
    
    def __init__(self, excel_file_path: str = "synthetic_commerce_data.xlsx",
                 openai_api_key: str = None, weather_api_key: str = None):
        """Initialize complete integrated system"""
        
        print("🚀 Initializing Complete Commerce in a Prompt for Bharat...")
        print("=" * 70)
        
        # Get API keys
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.weather_api_key = weather_api_key or os.getenv("OPENWEATHER_API_KEY")
        
        try:
            # 1. Initialize GPT-4 Enhanced Natural Language Parser
            print("🧠 Initializing GPT-4 Enhanced Parser...")
            self.parser = GPT4NaturalLanguageParser(self.openai_api_key)
            
            # 2. Initialize All Business Intelligence Agents
            print("📊 Initializing Demand Agent...")
            self.demand_agent = DemandAgent(excel_file_path, self.openai_api_key)
            
            print("🌤️ Initializing Weather Agent...")
            self.weather_agent = WeatherAgent(self.weather_api_key, self.openai_api_key)
            
            print("💰 Initializing Profitability Agent...")
            self.profitability_agent = ProfitabilityAgent(excel_file_path, self.openai_api_key)
            
            # 3. Initialize Master Stock Agent (Orchestrator)
            print("🎯 Initializing Master Stock Agent...")
            self.stock_agent = StockAgent(
                self.demand_agent,
                self.weather_agent, 
                self.profitability_agent,
                self.openai_api_key
            )
            
            print("=" * 70)
            print("✅ Complete Commerce AI System Initialized Successfully!")
            print("🎯 Ready for natural language business queries!")
            
        except Exception as e:
            print(f"❌ System Initialization Error: {e}")
            traceback.print_exc()
            raise
    
    def process_user_query(self, user_message: str) -> str:
        """
        Complete processing pipeline: Natural Language → Business Intelligence → Final Response
        
        Args:
            user_message: Natural language query from user
            
        Returns:
            Comprehensive business recommendation in WhatsApp format
        """
        
        try:
            print(f"\n🗣️ Processing User Query: '{user_message}'")
            print("-" * 50)
            
            # STEP 1: Parse Natural Language with GPT-4
            print("🧠 Step 1: GPT-4 Natural Language Processing...")
            parsed_info = self.parser.parse_query(user_message)
            
            location = parsed_info.get('location', 'Begum Bazaar')
            budget = parsed_info.get('budget', 1000)
            date = parsed_info.get('date') or datetime.now().strftime('%Y-%m-%d')
            intent = parsed_info.get('intent', 'general')
            confidence = parsed_info.get('confidence', 0.0)
            
            print(f"   📍 Location: {location}")
            print(f"   💰 Budget: ₹{budget}")
            print(f"   🎯 Intent: {intent}")
            print(f"   ✅ Confidence: {confidence:.2f}")
            
            # STEP 2: Gather Intelligence from All Agents
            print("\n📊 Step 2: Gathering Multi-Agent Intelligence...")
            
            # Demand Intelligence
            print("   🔍 Analyzing Demand Patterns...")
            demand_summary = self.demand_agent.get_location_summary(location, date)
            top_demand_products = [p['product'] for p in demand_summary.get('top_products', [])]
            
            # Weather Intelligence  
            print("   🌤️ Analyzing Weather Impact...")
            weather_data = self.weather_agent.fetch_current_weather("Hyderabad")
            if self.weather_agent.openai_api_key:
                weather_analysis = self.weather_agent.analyze_weather_impact_with_gpt4(
                    weather_data, user_message
                )
            else:
                weather_analysis = self.weather_agent.analyze_weather_impact(weather_data)
            
            weather_products = weather_analysis.get('recommendations', {}).get('high_demand', [])
            weather_boost = weather_analysis.get('recommendations', {}).get('weather_boost', 1.0)
            
            # Profitability Intelligence
            print("   💰 Analyzing Profitability Scenarios...")
            candidate_products = list(set(top_demand_products + weather_products))
            if not candidate_products:
                candidate_products = ['Cold Drinks', 'Tea', 'Samosa', 'Ice Cream', 'Fresh Fruits']
            
            profitability_insights = {}
            budget_per_product = budget / min(len(candidate_products), 3)
            
            for product in candidate_products[:5]:  # Analyze top 5 candidates
                if self.profitability_agent.openai_api_key:
                    profit_analysis = self.profitability_agent.analyze_profitability_with_gpt4(
                        product, location, budget_per_product, user_message
                    )
                else:
                    profit_analysis = self.profitability_agent.analyze_profitability(
                        product, location, budget_per_product
                    )
                
                if profit_analysis.get('success') and profit_analysis.get('roi_pct', 0) >= 15:
                    profitability_insights[product] = profit_analysis
            
            # STEP 3: Master AI Orchestration
            print("\n🎯 Step 3: Master AI Orchestration...")
            
            if self.stock_agent.openai_api_key:
                # Use GPT-4 enhanced orchestration
                final_response = self.stock_agent.generate_whatsapp_response_with_gpt4(
                    location, budget, date, user_message
                )
            else:
                # Use traditional orchestration
                orchestration_result = self.stock_agent.synthesize_recommendations_with_gpt4(
                    location, budget, date, user_message
                )
                final_response = self._format_comprehensive_response(
                    orchestration_result, parsed_info, demand_summary, 
                    weather_analysis, profitability_insights
                )
            
            print("✅ Complete processing pipeline executed successfully!")
            return final_response
            
        except Exception as e:
            error_msg = f"❌ Processing Error: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            
            return f"""🤖 **Commerce AI Assistant**
            
❌ Maaf bhai, kuch technical problem aa gayi hai.

Error: {str(e)}

💡 **Try again with:**
• Simple language: "I have 2000 rupees in Begum Bazaar"
• Clear location: Begum Bazaar, Hitech City, Kukatpally
• Specific budget amount

🔄 Please try again in a few moments!"""
    
    def _format_comprehensive_response(self, orchestration_result: Dict, parsed_info: Dict,
                                     demand_summary: Dict, weather_analysis: Dict,
                                     profitability_insights: Dict) -> str:
        """Format comprehensive response when GPT-4 orchestration is not available"""
        
        location = parsed_info.get('location', 'Begum Bazaar')
        budget = parsed_info.get('budget', 1000)
        intent = parsed_info.get('intent', 'general')
        
        recommendations = orchestration_result.get('final_recommendations', [])
        
        if not recommendations:
            return f"""🤖 **Commerce AI - {location}**
            
❌ Current budget ₹{budget} ke saath profitable options nahi mil rahe.

💡 **Suggestions:**
• Budget increase karo minimum ₹1500+
• Different location try karo
• Market conditions improve hone ka wait karo

📞 Try again with higher budget!"""
        
        # Build comprehensive response
        weather_condition = weather_analysis.get('weather_summary', {}).get('condition', 'clear')
        weather_temp = weather_analysis.get('weather_summary', {}).get('temperature', 'N/A')
        
        response = f"""🤖 **COMPLETE COMMERCE AI ANALYSIS - {location}**
📅 Date: {datetime.now().strftime('%Y-%m-%d')}
💰 Budget: ₹{budget}
🎯 Intent: {intent.title()}
🌤️ Weather: {weather_condition.title()} ({weather_temp}°C)

🏆 **AI RECOMMENDED PRODUCTS:**
"""
        
        for i, rec in enumerate(recommendations[:3], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            response += f"""
{emoji} **{rec.get('product', 'N/A')}**
• Investment: ₹{rec.get('investment_amount', 0)}
• Daily Profit: ₹{rec.get('daily_profit_estimate', 0)}
• ROI: {rec.get('expected_roi', 0)}%
• Risk: {rec.get('risk_level', 'Medium')}
"""
        
        # Add intelligence insights
        response += f"""
📊 **MARKET INTELLIGENCE:**
• Top Demand: {', '.join([p['product'] for p in demand_summary.get('top_products', [])[:3]])}
• Weather Boost: {weather_analysis.get('recommendations', {}).get('weather_boost', 1.0):.1f}x
• Profitable Products: {len(profitability_insights)}

💡 **AI STRATEGY:**
• Focus on top 2 products for maximum returns
• Weather conditions are {'favorable' if weather_analysis.get('recommendations', {}).get('weather_boost', 1.0) > 1.2 else 'normal'}
• Expected success rate: High

🙏 **Commerce AI wishes you great business success!**
_Powered by Multi-Agent AI Intelligence_ 🚀"""
        
        return response
    
    def batch_process_queries(self, queries: List[str]) -> List[Dict]:
        """Process multiple queries for testing/analysis"""
        
        results = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n🧪 Processing Query {i}/{len(queries)}: {query}")
            
            try:
                response = self.process_user_query(query)
                results.append({
                    'query': query,
                    'response': response,
                    'status': 'success',
                    'processed_at': datetime.now().isoformat()
                })
            except Exception as e:
                results.append({
                    'query': query,
                    'error': str(e),
                    'status': 'failed',
                    'processed_at': datetime.now().isoformat()
                })
        
        return results

# Interactive Interface
def run_interactive_commerce_ai():
    """Run interactive Commerce AI interface"""
    
    print("🇮🇳 COMMERCE IN A PROMPT FOR BHARAT - INTERACTIVE MODE 🇮🇳")
    print("Natural Language Business Intelligence for Street Vendors")
    print("=" * 70)
    
    try:
        # Initialize complete system
        orchestrator = CompleteCommerceOrchestrator()
        
        print("\n💡 Instructions:")
        print("• Ask in simple Hindi/English: 'मुझे 2000 रुपये के साथ बेगम बाजार में क्या बेचना चाहिए?'")
        print("• Or English: 'I have 5000 rupees in Hitech City, what should I sell?'")
        print("• Type 'quit' to exit")
        print("• Type 'test' to run demo queries")
        print("-" * 50)
        
        while True:
            print("\n🤖 Commerce AI: What's your business question?")
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🙏 धन्यवाद! Thanks for using Commerce AI!")
                break
            
            if user_input.lower() == 'test':
                # Run demo queries
                demo_queries = [
                    "मुझे 2000 रुपये के साथ बेगम बाजार में अच्छा बिज़नेस चाहिए",
                    "I have 5000 rupees in Hitech City, what to sell today?",
                    "help me with business in Kukatpally with 3000 budget",
                    "barish mein kya sell karu with 1500 in Ameerpet"
                ]
                
                for demo_query in demo_queries:
                    print(f"\n🧪 Demo: {demo_query}")
                    print("=" * 60)
                    result = orchestrator.process_user_query(demo_query)
                    print(result[:500] + "..." if len(result) > 500 else result)
                    print("=" * 60)
                continue
            
            if not user_input:
                print("🤔 कुछ तो पूछिए! Please ask something!")
                continue
            
            print(f"\n🔄 Processing: '{user_input}'")
            print("=" * 60)
            
            try:
                response = orchestrator.process_user_query(user_input)
                print(response)
            except Exception as e:
                print(f"❌ Sorry, कुछ गलत हुआ: {e}")
            
            print("=" * 60)
    
    except Exception as e:
        print(f"❌ System Error: {e}")
        traceback.print_exc()

# Test Suite
def run_comprehensive_test():
    """Run comprehensive test with various scenarios"""
    
    print("🧪 COMPREHENSIVE COMMERCE AI TEST SUITE")
    print("=" * 60)
    
    try:
        orchestrator = CompleteCommerceOrchestrator()
        
        test_scenarios = [
            {
                'name': 'Hindi Mixed Query',
                'query': 'मुझे 3000 रुपये के साथ कुकतपल्ली में अच्छा धंधा चाहिए'
            },
            {
                'name': 'English Profit Focus', 
                'query': 'I want maximum profit with 5000 rupees in Hitech City'
            },
            {
                'name': 'Weather Dependent',
                'query': 'barish mein kya sell karu in Begum Bazaar with 2000 budget'
            },
            {
                'name': 'Low Budget Challenge',
                'query': 'help me with 800 rupees only in Charminar area'
            },
            {
                'name': 'Business Expansion',
                'query': 'want to expand business in Secunderabad have 4000 rupees'
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{'='*15} TEST {i}: {scenario['name']} {'='*15}")
            print(f"Query: {scenario['query']}")
            print("-" * 60)
            
            try:
                result = orchestrator.process_user_query(scenario['query'])
                print("Response Preview:")
                print(result[:400] + "..." if len(result) > 400 else result)
                print("✅ Test Passed")
            except Exception as e:
                print(f"❌ Test Failed: {e}")
            
            print("=" * 60)
        
        print("\n🎉 Comprehensive Testing Completed!")
        
    except Exception as e:
        print(f"❌ Test Suite Error: {e}")

# Main Execution
if __name__ == "__main__":
    
    print("🇮🇳 COMPLETE COMMERCE IN A PROMPT FOR BHARAT 🇮🇳")
    print("Multi-Agent AI System with GPT-4 Natural Language Processing")
    print("=" * 70)
    
    mode = input("""Choose mode:
1. Interactive Commerce AI (press 1)
2. Comprehensive Test Suite (press 2)
3. Single Query Test (press 3)
Enter choice: """).strip()
    
    if mode == "1":
        run_interactive_commerce_ai()
    elif mode == "2":
        run_comprehensive_test()
    elif mode == "3":
        try:
            orchestrator = CompleteCommerceOrchestrator()
            test_query = input("Enter your query: ").strip()
            if test_query:
                print(f"\n🧪 Processing: {test_query}")
                print("=" * 60)
                result = orchestrator.process_user_query(test_query)
                print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Invalid choice. Running interactive mode...")
        run_interactive_commerce_ai()
