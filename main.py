"""
Main application for Tourism AI System
"""
from tourism_ai_agent import TourismAIAgent


def main():
    """
    Main entry point for the Tourism AI application
    """
    print("=" * 60)
    print("Welcome to Tourism AI System")
    print("=" * 60)
    print("\nEnter a place you want to visit and ask about weather or places to visit.")
    print("Examples:")
    print('  - "I\'m going to go to Bangalore, let\'s plan my trip."')
    print('  - "I\'m going to go to Bangalore, what is the temperature there"')
    print('  - "I\'m going to go to Bangalore, what is the temperature there? And what are the places I can visit?"')
    print("\nType 'exit' or 'quit' to stop.\n")
    
    agent = TourismAIAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using Tourism AI System. Goodbye!")
                break
            
            if not user_input:
                print("Please enter a valid query.")
                continue
            
            # Process the request
            response = agent.process_request(user_input)
            
            print(f"\nTourism AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using Tourism AI System. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    main()

