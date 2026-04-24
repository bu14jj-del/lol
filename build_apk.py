import sys

# Create a custom input that always returns 'y' when asked about root
original_input = input
def patched_input(prompt=''):
    if 'y/n' in prompt.lower():
        return 'y'
    return original_input(prompt)

# Apply the patch
import builtins
builtins.input = patched_input

# Now import and run buildozer
from buildozer.scripts.client import main
sys.argv = ['buildozer', 'android', 'debug']

main()