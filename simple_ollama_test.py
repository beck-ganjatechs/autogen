#!/usr/bin/env python3
"""
Simple test to verify Ollama can generate code and write it to disk.
"""

import requests
import json
import os

def test_ollama_direct():
    """Test Ollama directly via LiteLLM proxy."""
    print("Testing Ollama directly...")
    print("=" * 50)
    
    # Test 1: Simple code generation
    print("\nTest 1: Generating Python code...")
    
    url = "http://localhost:4000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": "ollama/llama3.2:latest",
        "messages": [
            {
                "role": "user", 
                "content": "Write a complete Python script that creates a file called 'hello_world.py' and writes 'Hello from Ollama!' to it. Include the file.write() call and proper file handling."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print("Generated code:")
        print("-" * 30)
        print(content)
        print("-" * 30)
        
        # Extract Python code from the response
        if "```python" in content:
            code_start = content.find("```python") + 9
            code_end = content.find("```", code_start)
            python_code = content[code_start:code_end].strip()
        elif "```" in content:
            code_start = content.find("```") + 3
            code_end = content.find("```", code_start)
            python_code = content[code_start:code_end].strip()
        else:
            # Look for print statements or file operations
            lines = content.split('\n')
            python_code = '\n'.join([line for line in lines if line.strip() and not line.startswith('#')])
        
        print("\nExtracted Python code:")
        print("-" * 30)
        print(python_code)
        print("-" * 30)
        
        # Write the code to a file
        with open("generated_code.py", "w") as f:
            f.write(python_code)
        
        print("\nCode written to 'generated_code.py'")
        
        # Execute the generated code
        print("\nExecuting generated code...")
        exec(python_code)
        
        # Check if hello_world.py was created
        if os.path.exists("hello_world.py"):
            print("✅ SUCCESS: hello_world.py was created!")
            with open("hello_world.py", "r") as f:
                content = f.read()
            print(f"File content: '{content}'")
        else:
            print("❌ FAILED: hello_world.py was not created")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def test_ollama_code_generation():
    """Test different code generation scenarios."""
    print("\n" + "=" * 50)
    print("Test 2: Different code generation scenarios...")
    
    scenarios = [
        "Create a Python function that writes 'Hello World' to a file called 'test.txt'",
        "Write a Python script that creates a JSON file with some sample data",
        "Create a Python program that generates a simple HTML file"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario}")
        print("-" * 40)
        
        url = "http://localhost:4000/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "model": "ollama/llama3.2:latest",
            "messages": [{"role": "user", "content": scenario}],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("Generated response:")
            print(content[:200] + "..." if len(content) > 200 else content)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    success = test_ollama_direct()
    if success:
        test_ollama_code_generation()
    else:
        print("Basic test failed, skipping additional tests.")