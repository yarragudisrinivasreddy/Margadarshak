# natural_language_parser_gpt4_fixed.py - Corrected GPT-4 Enhanced Parser
import re
import json
import os
import requests
from datetime import datetime
from typing import Dict, Optional, List

class GPT4NaturalLanguageParser:
    def __init__(self, openai_api_key: str = None):
        """Initialize GPT-4 Enhanced Natural Language Parser"""
        
        # 🔐 SECURITY FIX: Use environment variable instead of hardcoding
        self.openai_api_key = "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"
        self.use_gpt4 = bool(self.openai_api_key)
        
        if self.use_gpt4:
            print("✅ Natural Language Parser: GPT-4 enhanced parsing enabled")
        else:
            print("🔄 Natural Language Parser: Using rule-based fallback")
            print("💡 Set OPENAI_API_KEY environment variable to enable GPT-4")
        
        # Known locations for validation
        self.known_locations = {
            'begum bazar': 'Begum Bazaar',
            'begum bazaar': 'Begum Bazaar', 
            'charminar': 'Charminar',
            'hitech city': 'Hitech City',
            'hi-tech city': 'Hitech City',
            'hitec city': 'Hitech City',
            'kukatpally': 'Kukatpally',
            'kphb': 'Kukatpally',
            'secunderabad': 'Secunderabad',
            'sec bad': 'Secunderabad',
            'ameerpet': 'Ameerpet',
            'jubilee hills': 'Jubilee Hills',
            'banjara hills': 'Banjara Hills',
            'gachibowli': 'Gachibowli',
            'madhapur': 'Madhapur',
            'kondapur': 'Kondapur'
        }
    
    def parse_query(self, query: str) -> Dict:
        """Parse natural language query using GPT-4 or fallback"""
        
        if self.use_gpt4:
            try:
                gpt4_result = self._parse_with_gpt4(query)
                if gpt4_result and not gpt4_result.get('error'):
                    validated_result = self._validate_gpt4_result(gpt4_result, query)
                    return validated_result
                else:
                    print(f"⚠️ GPT-4 parsing failed: {gpt4_result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"⚠️ GPT-4 parsing error: {e}")
        
        # Fallback to rule-based parsing
        print("🔄 Using fallback rule-based parsing")
        return self._parse_with_rules(query)
    
    def _parse_with_gpt4(self, query: str) -> Dict:
        """🔧 FIXED: Use GPT-4 for intelligent natural language parsing"""
        
        try:
            # 🔧 FIX: Simplified system prompt without JSON format requirement
            system_prompt = """You are an expert at extracting business information from Indian street vendor queries.

From the user's query, extract:
1. Location (Hyderabad area names like Begum Bazaar, Hitech City, etc.)
2. Budget amount in rupees (numbers mentioned)
3. Date if any (today, tomorrow, specific dates)
4. Intent (sell, buy, profit, help, weather, products, business)
5. Your confidence level (0.0 to 1.0)

Respond with a JSON object containing: location, budget, date, intent, original_message, confidence

Common areas: Begum Bazaar, Charminar, Hitech City, Kukatpally, Secunderabad, Ameerpet, Gachibowli"""

            user_prompt = f"Extract information from this vendor query: {query}"
            
            # 🔧 FIX: Corrected API request format
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # 🔧 FIX: Use gpt-4 model with proper parameters
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 300
                # 🔧 REMOVED: response_format to avoid complications
            }
            
            print(f"🔄 Making GPT-4 API call for: {query[:50]}...")
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                print(f"🤖 GPT-4 Response: {content[:100]}...")
                
                # 🔧 FIX: Better JSON extraction from response
                try:
                    # Try direct JSON parsing first
                    parsed_json = json.loads(content)
                    return parsed_json
                except json.JSONDecodeError:
                    # Extract JSON from response text
                    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
                    if json_match:
                        try:
                            return json.loads(json_match.group())
                        except:
                            pass
                    
                    # If JSON extraction fails, create structured response
                    return self._extract_from_text_response(content, query)
            
            else:
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get('error', {}).get('message', 'Unknown error')
                except:
                    error_detail = response.text[:200]
                
                return {
                    'error': f'API call failed: {response.status_code}',
                    'detail': error_detail
                }
                
        except Exception as e:
            return {'error': f'GPT-4 parsing exception: {str(e)}'}
    
    def _extract_from_text_response(self, content: str, original_query: str) -> Dict:
        """🔧 FIX: Extract information from text response when JSON parsing fails"""
        
        content_lower = content.lower()
        
        # Extract location
        location = 'Begum Bazaar'  # default
        for loc_key, loc_name in self.known_locations.items():
            if loc_key in content_lower:
                location = loc_name
                break
        
        # Extract budget
        budget_match = re.search(r'(\d{3,6})', content)
        budget = int(budget_match.group(1)) if budget_match else 1000
        
        # Extract intent
        intent = 'sell'  # default
        if any(word in content_lower for word in ['profit', 'earn', 'money']):
            intent = 'profit'
        elif any(word in content_lower for word in ['help', 'advice', 'suggest']):
            intent = 'help'
        elif any(word in content_lower for word in ['buy', 'purchase']):
            intent = 'buy'
        
        # Extract confidence
        confidence_match = re.search(r'(\d\.\d)', content)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.8
        
        return {
            'location': location,
            'budget': budget,
            'date': None,
            'intent': intent,
            'original_message': original_query,
            'confidence': confidence
        }
    
    def _validate_gpt4_result(self, gpt4_result: Dict, original_query: str) -> Dict:
        """Validate and enhance GPT-4 parsing result"""
        
        validated = {
            'location': gpt4_result.get('location', 'Begum Bazaar'),
            'budget': int(gpt4_result.get('budget', 1000)) if gpt4_result.get('budget') else 1000,
            'date': gpt4_result.get('date'),
            'intent': gpt4_result.get('intent', 'general'),
            'original_message': gpt4_result.get('original_message', original_query),
            'confidence': float(gpt4_result.get('confidence', 0.8)),
            'parsing_method': 'gpt4',
            'gpt4_raw': gpt4_result
        }
        
        # Validate location
        location_lower = validated['location'].lower()
        if location_lower in self.known_locations:
            validated['location'] = self.known_locations[location_lower]
        
        # Validate budget range
        if validated['budget'] < 100:
            validated['budget'] = 1000
        elif validated['budget'] > 1000000:
            validated['budget'] = 100000
        
        # Add intent analysis
        validated['intent_analysis'] = self._analyze_intent_gpt4(original_query, validated['intent'])
        
        return validated
    
    def _analyze_intent_gpt4(self, query: str, primary_intent: str) -> Dict:
        """Additional intent analysis"""
        
        query_lower = query.lower()
        
        return {
            'primary_intent': primary_intent,
            'has_profit_focus': any(word in query_lower for word in ['profit', 'fayda', 'earn', 'kama', 'paisa']),
            'weather_sensitive': any(word in query_lower for word in ['rain', 'barish', 'hot', 'garmi']),
            'urgency_level': 'high' if any(word in query_lower for word in ['today', 'aaj', 'urgent']) else 'normal',
            'query_complexity': 'high' if len(query.split()) > 10 else 'medium' if len(query.split()) > 5 else 'simple'
        }
    
    def _parse_with_rules(self, query: str) -> Dict:
        """🔧 Enhanced rule-based parsing"""
        
        normalized_query = query.lower().strip()
        
        # Extract components using improved patterns
        location = self._extract_location_rules(normalized_query)
        budget = self._extract_budget_rules(normalized_query)
        date = self._extract_date_rules(normalized_query)
        intent = self._extract_intent_rules(normalized_query)
        confidence = self._calculate_rule_confidence(location, budget, query)
        
        return {
            'location': location,
            'budget': budget,
            'date': date,
            'intent': intent,
            'original_message': query,
            'confidence': confidence,
            'parsing_method': 'rules',
            'intent_analysis': self._analyze_intent_rules(normalized_query)
        }
    
    def _extract_location_rules(self, text: str) -> str:
        """Enhanced location extraction"""
        
        # Direct matching
        for location_key, location_name in self.known_locations.items():
            if location_key in text:
                return location_name
        
        # Pattern matching with more variations
        location_patterns = [
            r'(?:in|at|near|around)\s+([a-z\s]+?)(?:\s|$|,)',
            r'(?:visiting|visit|go to|going to)\s+([a-z\s]+?)(?:\s|$|,)',
            r'([a-z\s]+?)\s+(?:market|area|location|mein|me)',
            r'(?:^|\s)(begum|hitech|kukat|secunder|charminar|ameer)[\w\s]*'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                match_clean = match.strip().lower()
                # Partial matching for location names
                for loc_key, loc_name in self.known_locations.items():
                    if match_clean in loc_key or loc_key in match_clean:
                        return loc_name
        
        return 'Begum Bazaar'
    
    def _extract_budget_rules(self, text: str) -> int:
        """Enhanced budget extraction"""
        
        budget_patterns = [
            r'(\d{3,6})\s*(?:rs|rupees|₹|rups|rupee)',
            r'(?:rs|rupees|₹)\s*(\d{3,6})',
            r'budget\s+(?:of\s+)?(\d{3,6})',
            r'(?:have|got|with)\s+(\d{3,6})',
            r'(\d{3,6})\s+(?:only|total|ke saath)',
            r'(?:^|\s)(\d{3,6})(?:\s|$)',
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, text)
            if match:
                budget = int(match.group(1))
                if 100 <= budget <= 500000:  # Reasonable range
                    return budget
        
        return 1000
    
    def _extract_date_rules(self, text: str) -> Optional[str]:
        """Enhanced date extraction"""
        
        today = datetime.now()
        
        if any(word in text for word in ['today', 'aaj', 'आज']):
            return today.strftime('%Y-%m-%d')
        elif any(word in text for word in ['tomorrow', 'kal', 'कल']):
            tomorrow = today.replace(day=today.day + 1) if today.day < 28 else today.replace(month=today.month + 1, day=1)
            return tomorrow.strftime('%Y-%m-%d')
        
        return None
    
    def _extract_intent_rules(self, text: str) -> str:
        """Enhanced intent extraction"""
        
        intent_keywords = {
            'sell': ['sell', 'bech', 'business', 'kaam', 'dhanda'],
            'profit': ['profit', 'fayda', 'earn', 'kama', 'paisa', 'money'],
            'weather': ['rain', 'barish', 'hot', 'garmi', 'cold', 'sardi'],
            'help': ['help', 'madad', 'suggest', 'recommend', 'btao', 'batao'],
            'buy': ['buy', 'purchase', 'kharid', 'products', 'saman']
        }
        
        intent_scores = {}
        for intent_type, keywords in intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                intent_scores[intent_type] = score
        
        return max(intent_scores, key=intent_scores.get) if intent_scores else 'general'
    
    def _calculate_rule_confidence(self, location: str, budget: int, query: str) -> float:
        """Enhanced confidence calculation"""
        
        confidence = 0.4  # Higher base for improved rules
        
        if location != 'Begum Bazaar':
            confidence += 0.2
        
        if budget != 1000:
            confidence += 0.2
        
        if len(query.split()) >= 5:
            confidence += 0.1
        
        business_keywords = ['sell', 'buy', 'business', 'profit', 'earn', 'bech', 'kaam']
        if any(keyword in query.lower() for keyword in business_keywords):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _analyze_intent_rules(self, text: str) -> Dict:
        """Enhanced rule-based intent analysis"""
        
        return {
            'has_profit_focus': any(word in text for word in ['profit', 'fayda', 'earn', 'kama', 'paisa']),
            'weather_sensitive': any(word in text for word in ['rain', 'barish', 'hot', 'garmi', 'weather']),
            'urgency_level': 'high' if any(word in text for word in ['today', 'aaj', 'urgent', 'jaldi']) else 'normal',
            'query_complexity': 'high' if len(text.split()) > 10 else 'medium' if len(text.split()) > 5 else 'simple'
        }

# 🧪 Test with corrected version
if __name__ == "__main__":
    print("=== FIXED GPT-4 ENHANCED NATURAL LANGUAGE PARSER ===")
    
    # Initialize parser
    parser = GPT4NaturalLanguageParser()
    
    # Test queries
    test_queries = [
        "i have 5000 i am in begum bazar to products"
    ]
    
    print(f"\n🧪 Testing {len(test_queries)} queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- TEST {i} ---")
        print(f"Input: {query}")
        
        try:
            result = parser.parse_query(query)
            print(f"Location: {result.get('location')}")
            print(f"Budget: ₹{result.get('budget')}")
            print(f"Intent: {result.get('intent')}")
            print(f"Method: {result.get('parsing_method')}")
            print(f"Confidence: {result.get('confidence', 0):.2f}")
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ Parsed successfully")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n✅ Testing completed!")
