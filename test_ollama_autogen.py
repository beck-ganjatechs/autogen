#!/usr/bin/env python3
"""
Test script to verify Ollama + AutoGen integration for code generation and file writing.
"""

import os
import sys
from pathlib import Path
from typing import Annotated

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen import ConversableAgent, GroupChat, GroupChatManager, UserProxyAgent

# Configuration for Ollama via LiteLLM
config_list = [
    {
        "model": "ollama/llama3.2:latest",
        "base_url": "http://localhost:4000/v1",
        "api_key": "dummy-key",  # LiteLLM doesn't require real API key for Ollama
    }
]

# Set up the working directory
default_path = "./"
os.makedirs(default_path, exist_ok=True)

# Create a simple file writing function
def create_file_with_code(
    filename: Annotated[str, "Name and path of file to create."], 
    code: Annotated[str, "Code to write in the file."]
):
    """Create a new file with the given code content."""
    try:
        file_path = os.path.join(default_path, filename)
        with open(file_path, "w") as file:
            file.write(code)
        return 0, f"File '{filename}' created successfully"
    except Exception as e:
        return 1, f"Error creating file '{filename}': {str(e)}"

def read_file_content(
    filename: Annotated[str, "Name and path of file to read."]
):
    """Read the content of a file."""
    try:
        file_path = os.path.join(default_path, filename)
        with open(file_path, "r") as file:
            content = file.read()
        return 0, content
    except Exception as e:
        return 1, f"Error reading file '{filename}': {str(e)}"

def list_directory(
    directory: Annotated[str, "Directory to list."] = "."
):
    """List files in a directory."""
    try:
        dir_path = os.path.join(default_path, directory)
        files = os.listdir(dir_path)
        return 0, f"Files in {directory}: {', '.join(files)}"
    except Exception as e:
        return 1, f"Error listing directory '{directory}': {str(e)}"

# Create agents
engineer = ConversableAgent(
    name="Engineer",
    system_message="""You are a software engineer. You can create, read, and modify code files.
    When asked to create code, always write it to a file using the create_file_with_code function.
    Always provide complete, working code that can be executed immediately.""",
    llm_config={"config_list": config_list},
)

# Register functions with the engineer
engineer.register_for_llm(description="Create a new file with code.")(create_file_with_code)
engineer.register_for_llm(description="Read the content of a file.")(read_file_content)
engineer.register_for_llm(description="List files in a directory.")(list_directory)

# Register functions for execution
engineer.register_for_execution()(create_file_with_code)
engineer.register_for_execution()(read_file_content)
engineer.register_for_execution()(list_directory)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

# Test the setup
def test_ollama_autogen():
    """Test Ollama + AutoGen integration."""
    print("Testing Ollama + AutoGen integration...")
    print("=" * 50)
    
    # Test 1: Simple file creation
    print("\nTest 1: Creating a simple Python script...")
    result = user_proxy.initiate_chat(
        engineer,
        message="""Create a Python script called 'hello_world.py' that prints 'Hello from Ollama + AutoGen!' and saves it to a file.""",
    )
    
    # Test 2: Check if file was created
    print("\nTest 2: Verifying file creation...")
    result = user_proxy.initiate_chat(
        engineer,
        message="List the files in the current directory to see if hello_world.py was created.",
    )
    
    # Test 3: Read the created file
    print("\nTest 3: Reading the created file...")
    result = user_proxy.initiate_chat(
        engineer,
        message="Read the content of hello_world.py to verify it was created correctly.",
    )
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_ollama_autogen()