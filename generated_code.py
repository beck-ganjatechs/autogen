# Create a new file called 'hello_world.py'
def create_file(filename):
    try:
        # Open the file in write mode ('w' is used for writing)
        with open(filename, 'w') as file:
            # Write the desired string to the file
            file.write('Hello from Ollama!')
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function and specify the filename
create_file('hello_world.py')