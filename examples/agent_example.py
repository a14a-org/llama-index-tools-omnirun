"""Example: Using OmniRun sandbox tools with LlamaIndex.

Requires: OMNIRUN_API_KEY environment variable.

Usage:
    python examples/agent_example.py
"""

from llama_index_tools_omnirun import OmniRunToolSpec

spec = OmniRunToolSpec()
tools = spec.to_tool_list()

# Show available tools
print("Available tools:")
for t in tools:
    print(f"  - {t.metadata.name}: {t.metadata.description}")

# Execute code in sandbox
print("\nExecuting code in sandbox...")
result = tools[0]("print('Hello from Firecracker!')")
print(f"Result: {result}")

# Write and read a file
print("\nWriting a file...")
tools[2]("/tmp/data.txt", "sample data")

print("Reading the file back...")
content = tools[3]("/tmp/data.txt")
print(f"Content: {content}")

# Run a shell command
print("\nRunning shell command...")
result = tools[1]("uname -a")
print(f"System info: {result}")

spec.cleanup()
print("\nDone.")
