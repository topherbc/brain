from brain import CognitiveCrew

def main():
    # Initialize the cognitive crew
    crew = CognitiveCrew()
    
    # Example input
    input_data = "Your test input here"
    
    # Process the input
    result = crew.process_input(input_data)
    
    print(f"Decision: {result}")

if __name__ == "__main__":
    main()