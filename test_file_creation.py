#!/usr/bin/env python3
"""
Test script to verify AutoGen can write files to disk with Ollama.
"""

import os
import sys
from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

def main():
    print("🚀 Testing AutoGen file creation with Ollama...")
    
    # Load LLM inference endpoints from the config file
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    print(f"📋 Loaded config: {config_list}")
    
    # Create the agent that uses the LLM
    assistant = ConversableAgent(
        "assistant", 
        llm_config={"config_list": config_list},
        system_message="""You are a helpful coding assistant. When asked to write code, you must:
1. Write the code to a file using Python's file operations
2. Use proper file handling with 'with open()' statements
3. Always save files to the current working directory
4. Include proper error handling
5. After writing the file, verify it was created successfully"""
    )
    
    # Create the user proxy agent with code execution enabled
    user_proxy = UserProxyAgent(
        "user", 
        code_execution_config={
            "work_dir": ".",
            "use_docker": False,
            "timeout": 60
        },
        human_input_mode="NEVER"
    )
    
    # Test message asking for code generation and file writing
    message = """
    Write a Python function to calculate the factorial of a number and save it to a file called 'factorial.py'. 
    
    IMPORTANT: You must actually write the code to a file using Python file operations, not just show the code.
    
    The function should be named 'factorial' and should handle edge cases like 0 and negative numbers.
    Also include a main section that demonstrates the function with some examples.
    
    After writing the file, verify it was created and show its contents.
    """
    
    print("💬 Starting conversation...")
    print(f"📝 Request: {message}")
    
    # Start the conversation
    try:
        result = user_proxy.initiate_chat(
            assistant, 
            message=message,
            max_turns=5
        )
        print("✅ Conversation completed successfully!")
        
        # Check if the file was created
        if os.path.exists("factorial.py"):
            print("✅ File 'factorial.py' was created!")
            with open("factorial.py", "r") as f:
                content = f.read()
                print("📄 File contents:")
                print("-" * 50)
                print(content)
                print("-" * 50)
        else:
            print("❌ File 'factorial.py' was not created!")
            
    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()