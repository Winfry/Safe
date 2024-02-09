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
