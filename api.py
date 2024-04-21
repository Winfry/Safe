import os


# Set the environment variable
os.environ["OPENAI_API_KEY"] = "your_api_key"


import os
openai_api_key = ("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")

# Ensure openai_api_key is a string
if isinstance(openai_api_key, str):
    # Set the environment variable
    openai_api_key = ("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")

else:
    print("Error: OPENAI_API_KEY must be a string.")

openai_api_key = os.getenv("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")

# Check if the environment variable is set
if "OPENAI_API_KEY" in os.environ:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    
    # Ensure openai_api_key is a string
    if isinstance(openai_api_key, str):
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = "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"
    else:
        print("Error: OPENAI_API_KEY must be a string.")
else:
    print("Error: OPENAI_API_KEY environment variable is not set.")


import os

# Set the environment variable
os.environ["OPENAI_API_KEY"] = "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"