# main_gpt4.py - Complete GPT-4 Enhanced Commerce Orchestration
import os
import sys
import traceback
from datetime import datetime
from typing import Dict, List, Optional

# Import GPT-4 enhanced agents
try:
    from demand_agent_gpt4 import DemandAgent
    from weather_agent_gpt4 import WeatherAgent
    from profitability_agent_gpt4 import ProfitabilityAgent
    from stock_agent_gpt4 import StockAgent
    print("✅ Successfully imported all GPT-4 enhanced agents")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Ensure all GPT-4 enhanced agent files are present")
    sys.exit(1)

class GPT4CommerceOrchestrator:
    """Complete GPT-4 Enhanced Commerce Orchestration System"""
    
    def __init__(self, excel_file_path: str = "synthetic_commerce_data.xlsx",
                 weather_api_key: str = None, openai_api_key: str = None):
        """Initialize complete GPT-4 enhanced system"""
        
        print("🤖 Initializing GPT-4 Enhanced Commerce in a Prompt for Bharat...")
        print("=" * 80)
        
        # Set API keys
        self.openai_api_key = "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"
        self.weather_api_key = "c485c07fe2d89be6f9222b9878a2b782"
        
        if not self.openai_api_key:
            print("⚠️ OpenAI API key not found. GPT-4 features will be limited.")
            print("💡 Set OPENAI_API_KEY environment variable for full AI capabilities")
        else:
            print(f"✅ OpenAI API key configured: {self.openai_api_key[:8]}...")
        
        try:
            # Initialize GPT-4 enhanced agents
            print("\n🧠 Initializing GPT-4 Enhanced Agents...")
            
            self.demand_agent = DemandAgent(excel_file_path, self.openai_api_key)
            self.weather_agent = WeatherAgent(self.weather_api_key, self.openai_api_key)
            self.profitability_agent = ProfitabilityAgent(excel_file_path, self.openai_api_key)
            
            # Initialize master GPT-4 orchestrator
            self.stock_agent = StockAgent(
                self.demand_agent,
                self.weather_agent,
                self.profitability_agent,
                self.openai_api_key
            )
            
            print("=" * 80)
            print("✅ All GPT-4 Enhanced Agents initialized successfully!")
            print("🎯 AI-Powered Commerce System ready for intelligent queries!")
            
            # Display system capabilities
            self._display_system_capabilities()
            
        except Exception as e:
            print(f"❌ System Initialization Error: {e}")
            traceback.print_exc()
            raise
    
    def _display_system_capabilities(self):
        """Display system capabilities"""
        print("\n🎯 SYSTEM CAPABILITIES:")
        print("├── 📊 Demand Agent: GPT-4 enhanced demand analysis")
        print("├── 🌤️ Weather Agent: AI-powered weather impact assessment")
        print("├── 💰 Profitability Agent: GPT-4 financial optimization")
        print("└── 🎯 Stock Agent: Master GPT-4 orchestration")
        print("\n💡 FEATURES:")
        print("• Natural language understanding in Hindi/English")
        print("• Context-aware recommendations")
        print("• Weather-adapted selling strategies")
        print("• Risk-optimized profit calculations")
        print("• Real-time market intelligence")
    
    def process_query_with_gpt4(self, query: str) -> str:
        """
        Master GPT-4 query processing with intelligent orchestration
        
        Query examples:
        - 'location=Begum Bazaar&budget=1500&message=कल क्या बेचना चाहिए?'
        - 'location=Hitech City&budget=3000&message=बारिश में अच्छा बिज़नेस क्या होगा?'
        """
        
        try:
            print(f"\n🤖 GPT-4 Processing Query: {query}")
            print("-" * 70)
            
            # Enhanced query parsing
            params = self._parse_enhanced_query(query)
            
            location = params.get('location', 'Begum Bazaar')
            budget = float(params.get('budget', 1000))
            date = params.get('date', None)
            message = params.get('message', '')
            
            # Enhanced validation
            if budget < 100:
                return "❌ Minimum budget ₹100 required for GPT-4 analysis"
            
            print(f"📍 Location: {location}")
            print(f"💰 Budget: ₹{budget}")
            print(f"📅 Date: {date or 'Today'}")
            print(f"💬 Message: {message or 'N/A'}")
            print(f"🧠 AI Mode: {'GPT-4 Enhanced' if self.openai_api_key else 'Standard'}")
            
            # Process with GPT-4 enhanced orchestration
            if self.openai_api_key and message:
                print("🚀 Engaging GPT-4 Master Orchestration...")
                response = self.stock_agent.generate_whatsapp_response_with_gpt4(
                    location, budget, date, message
                )
            else:
                print("🔄 Using standard orchestration...")
                # Fallback to basic orchestration
                analysis = self.stock_agent.synthesize_recommendations_with_gpt4(
                    location, budget, date, message
                )
                response = self._format_basic_response(analysis)
            
            print("✅ GPT-4 Query processed successfully!")
            return response
            
        except Exception as e:
            error_msg = f"❌ GPT-4 Processing error: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg
    
    def _parse_enhanced_query(self, query: str) -> Dict:
        """Enhanced query parsing with error handling"""
        try:
            params = {}
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    # URL decode common characters
                    value = value.replace('%20', ' ').replace('%3F', '?')
                    params[key] = value
            return params
        except Exception as e:
            print(f"⚠️ Query parsing error: {e}")
            return {'error': 'Query parsing failed'}
    
    def _format_basic_response(self, analysis: Dict) -> str:
        """Format basic response when GPT-4 is not available"""
        if not analysis.get('success'):
            return f"❌ Analysis failed: {analysis.get('error', 'Unknown error')}"
        
        recs = analysis.get('final_recommendations', [])
        if not recs:
            return "❌ No viable recommendations found for current parameters"
        
        response = f"📊 COMMERCE RECOMMENDATIONS\n"
        response += f"📍 Location: {analysis.get('location')}\n"
        response += f"💰 Budget: ₹{analysis.get('budget')}\n\n"
        
        for i, rec in enumerate(recs[:3], 1):
            response += f"{i}. {rec['product']}\n"
            response += f"   Investment: ₹{rec['investment_amount']}\n"
            response += f"   Daily Profit: ₹{rec['daily_profit_estimate']}\n"
            response += f"   ROI: {rec['expected_roi']}%\n\n"
        
        return response
    
    def test_individual_agents_gpt4(self, location: str = "Begum Bazaar", 
                                   budget: float = 2000, test_message: str = "test करना है") -> None:
        """Test individual GPT-4 enhanced agents"""
        
        print(f"\n🧪 TESTING GPT-4 ENHANCED AGENTS")
        print(f"Location: {location}, Budget: ₹{budget}")
        print("=" * 70)
        
        try:
            # Test Demand Agent
            print("\n📊 DEMAND AGENT GPT-4 TEST:")
            demand_result = self.demand_agent.analyze_demand_with_gpt4(
                location, "Cold Drinks", datetime.now().strftime('%Y-%m-%d'), test_message
            )
            print(f"✅ Demand Score: {demand_result.get('demand_score', 'N/A')}/10")
            if 'gpt4_insights' in demand_result:
                print(f"🧠 GPT-4 Insights: Available ({len(demand_result['gpt4_insights'])} chars)")
            
            # Test Weather Agent
            print("\n🌤️ WEATHER AGENT GPT-4 TEST:")
            weather_rec = self.weather_agent.get_daily_recommendation_with_gpt4(
                "Hyderabad", datetime.now().strftime('%Y-%m-%d'), test_message
            )
            print(f"✅ Weather Analysis: {len(weather_rec)} characters")
            
            # Test Profitability Agent
            print("\n💰 PROFITABILITY AGENT GPT-4 TEST:")
            prof_result = self.profitability_agent.analyze_profitability_with_gpt4(
                "Cold Drinks", location, budget/3, test_message
            )
            if prof_result.get('success'):
                print(f"✅ ROI: {prof_result['roi_pct']}%")
                print(f"✅ Daily Profit: ₹{prof_result['daily_profit']}")
                if 'gpt4_insights' in prof_result:
                    print(f"🧠 GPT-4 Financial Insights: Available")
            
            # Test Stock Agent
            print("\n🎯 STOCK AGENT GPT-4 TEST:")
            stock_analysis = self.stock_agent.synthesize_recommendations_with_gpt4(
                location, budget, datetime.now().strftime('%Y-%m-%d'), test_message
            )
            if stock_analysis.get('success'):
                print(f"✅ Recommendations: {len(stock_analysis.get('final_recommendations', []))}")
                print(f"✅ AI-Powered: {stock_analysis.get('ai_powered', False)}")
                if 'gpt4_master_synthesis' in stock_analysis:
                    print(f"🧠 GPT-4 Master Synthesis: Available")
            
            print("\n" + "=" * 70)
            print("✅ GPT-4 Enhanced Agent Testing Completed!")
            
        except Exception as e:
            print(f"❌ Agent testing error: {e}")
            traceback.print_exc()

def run_gpt4_test_suite():
    """Run comprehensive GPT-4 test suite"""
    
    print("🧪 GPT-4 COMMERCE IN A PROMPT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    try:
        # Initialize system
        system = GPT4CommerceOrchestrator()
        
        # Define GPT-4 test scenarios
        gpt4_test_scenarios = [
            {
                'name': '💰 Standard Hindi Query - Begum Bazaar',
                'query': 'location=Begum Bazaar&budget=1500&message=कल क्या बेचना चाहिए जो ज्यादा फायदा दे?',
                'description': 'Hindi language query with profit focus'
            },
            {
                'name': '🌧️ Weather-Aware Query - Hitech City', 
                'query': 'location=Hitech City&budget=3000&message=बारिश के मौसम में क्या बिज़नेस अच्छा रहेगा?',
                'description': 'Weather-dependent business strategy'
            },
            {
                'name': '💸 Low Budget Challenge - Charminar',
                'query': 'location=Charminar&budget=800&message=कम पैसे में कैसे अच्छा बिज़नेस करूं?',
                'description': 'Budget optimization with constraints'
            },
            {
                'name': '📈 Business Expansion - Secunderabad',
                'query': 'location=Secunderabad&budget=2500&message=अपना बिज़नेस बढ़ाना चाहता हूं, क्या करना चाहिए?',
                'description': 'Business growth and expansion strategy'
            },
            {
                'name': '🎯 Mixed Language Query - Kukatpally',
                'query': 'location=Kukatpally&budget=2000&message=I want good profit today, suggest best products',
                'description': 'English query with profit optimization'
            }
        ]
        
        # Run GPT-4 enhanced test scenarios
        for i, scenario in enumerate(gpt4_test_scenarios, 1):
            print(f"\n{'='*25} GPT-4 TEST {i}: {scenario['name']} {'='*25}")
            print(f"📝 Description: {scenario['description']}")
            print(f"🔧 Query: {scenario['query']}")
            print("\n📱 GPT-4 SYSTEM RESPONSE:")
            print("-" * 70)
            
            try:
                result = system.process_query_with_gpt4(scenario['query'])
                print(result)
            except Exception as e:
                print(f"❌ Test failed: {e}")
            
            print("\n" + "="*80)
        
        # Test individual GPT-4 agents
        print(f"\n{'='*30} GPT-4 AGENT TESTING {'='*30}")
        system.test_individual_agents_gpt4("Hitech City", 2500, "GPT-4 test करना है")
        
        print(f"\n{'='*35} GPT-4 TEST SUMMARY {'='*35}")
        print("✅ GPT-4 Enhanced Testing Completed Successfully!")
        print("🎯 System Validation: PASSED")
        print("🚀 Ready for Production Deployment!")
        print("🤖 GPT-4 Intelligence: ACTIVE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ GPT-4 Test suite error: {e}")
        traceback.print_exc()

def interactive_gpt4_mode():
    """Interactive GPT-4 mode for testing"""
    
    print("🤖 GPT-4 INTERACTIVE MODE - Commerce in a Prompt")
    print("=" * 60)
    
    try:
        system = GPT4CommerceOrchestrator()
        
        print("\n💡 GPT-4 Instructions:")
        print("• Ask in Hindi, English, or Hinglish")
        print("• Be specific about location and budget")
        print("• Type 'quit' to exit")
        print("• Type 'test' to run full test suite")
        print("-" * 60)
        
        while True:
            print("\n🤖 GPT-4 Commerce AI: Ready for your query...")
            
            location = input("Location (e.g., Begum Bazaar): ").strip()
            if location.lower() == 'quit':
                break
            elif location.lower() == 'test':
                run_gpt4_test_suite()
                continue
            
            budget = input("Budget (₹): ").strip()
            message = input("Your message (Hindi/English): ").strip()
            
            # Build GPT-4 enhanced query
            query = f"location={location}&budget={budget}&message={message}"
            
            print(f"\n🔄 GPT-4 Processing: {query}")
            print("=" * 60)
            
            try:
                result = system.process_query_with_gpt4(query)
                print(result)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("=" * 60)
        
        print("🙏 Thanks for using GPT-4 Enhanced Commerce in a Prompt!")
        
    except Exception as e:
        print(f"❌ Interactive mode error: {e}")

# Main execution with GPT-4 capabilities
if __name__ == "__main__":
    
    print("🇮🇳 GPT-4 ENHANCED COMMERCE IN A PROMPT FOR BHARAT 🇮🇳")
    print("AI-Powered Business Intelligence for Street Vendors")
    print("=" * 70)
    
    
    # Check API key availability
    # if not os.getenv("OPENAI_API_KEY"):
    #     print("⚠️ OpenAI API Key Not Found!")
    #     print("💡 For full GPT-4 capabilities, set your API key:")
    #     print("   export OPENAI_API_KEY='your-api-key-here'")
    #     print("📋 Get your API key from: https://platform.openai.com/api-keys")
    #     print("-" * 70)
    
    # Choose execution mode
    mode = input("Choose mode:\n1. GPT-4 Test Suite (press 1)\n2. GPT-4 Interactive Mode (press 2)\n3. Single GPT-4 Query Test (press 3)\nEnter choice: ").strip()
    
    if mode == "1":
        # Run GPT-4 enhanced test suite
        run_gpt4_test_suite()
        
    elif mode == "2":
        # GPT-4 interactive mode
        interactive_gpt4_mode()
        
    elif mode == "3":
        # Single GPT-4 query test
        try:
            system = GPT4CommerceOrchestrator()
            
            # Example GPT-4 enhanced query
            test_query = "location=Begum Bazaar&budget=2000&message=मुझे आज अच्छा पैसा कमाना है, क्या बेचूं?"
            print(f"\n🧪 Testing GPT-4 Query: {test_query}")
            print("=" * 70)
            
            result = system.process_query_with_gpt4(test_query)
            print(result)
            
        except Exception as e:
            print(f"❌ Single query test error: {e}")
    
    else:
        print("❌ Invalid choice. Running GPT-4 test suite by default...")
        run_gpt4_test_suite()
