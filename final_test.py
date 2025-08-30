# Example usage with your working system
from complete_commerce_orchestrator import CompleteCommerceOrchestrator

# Initialize complete system
orchestrator = CompleteCommerceOrchestrator(
    excel_file_path="synthetic_commerce_data.xlsx",
    openai_api_key="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",
    weather_api_key="c485c07fe2d89be6f9222b9878a2b782"
)

# Test natural language queries
queries = [
    "i have 5000 i am in begum bazar to products"
]

for query in queries:
    print(f"\nQuery: {query}")
    response = orchestrator.process_user_query(query)
    print("=" * 50)
    print(response)
    print("=" * 50)
