## local imports
from quiggle.tools.printer import colors

## global imports
import random
import string

def generate_code(length: int, mode: str = 'all') -> str:
    '''
    Generate a random code of specified length based on the given mode.

    Args:
        length (int): The length of the code to generate.
        mode (str): The mode determining the character pool:
            - 'all': Digits, uppercase, and lowercase letters (default).
            - 'alpha': Uppercase and lowercase letters.
            - 'number': Only digits.
            - 'lower': Digits and lowercase letters.
            - 'upper': Digits and uppercase letters.

    Returns:
        str: A randomly generated code.
    
    Raises:
        ValueError: If the length is less than 1 or an invalid mode is specified.
    '''
    if length < 1:
        raise ValueError("Length must be at least 1.")

    # Define character pools for each mode
    pools = {
        'all': string.ascii_letters + string.digits,
        'alpha': string.ascii_letters,
        'number': string.digits,
        'lower': string.ascii_lowercase + string.digits,
        'upper': string.ascii_uppercase + string.digits
    }

    # Get the character pool based on mode
    if mode not in pools:
        raise ValueError(f"Invalid mode '{mode}'. Available modes: {', '.join(pools.keys())}")

    char_pool = pools[mode]

    # Generate and return the random code
    return ''.join(random.choices(char_pool, k=length))