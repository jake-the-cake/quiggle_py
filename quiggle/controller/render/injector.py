import re

class HTMLInjector:
    """HTML injector system for parsing and injecting content into custom <insert> tags."""
    
    # Regex for parsing <insert> tags
    INSERT_REGEX = re.compile(r"<insert\s+(\w+)(?:\s+or=['\"](.*?)['\"])?(?:\s+and=['\"](.*?)['\"])?\s*\/?>")
    
    def __init__(self, variables=None):
        """
        Initialize with a dictionary of variables.
        :param variables: Dict containing variable names and their values.
        """
        self.variables = variables or {}
        print(self.variables)
    
    def inject(self, html: str) -> str:
        """
        Parse and replace all <insert> tags in the provided HTML.
        :param html: The input HTML string.
        :return: The HTML with injected content.
        """
        def replace_insert(match):
            # Extract attributes from the regex match
            variable_name = match.group(1)  # e.g., status_code
            default_value = match.group(2)  # e.g., '999'
            append_variable = match.group(3)  # e.g., status_message
            
            # Retrieve the variable's value or use the default
            injection = self.variables.get(variable_name, default_value)
            
            # Optionally append another variable's value
            if append_variable:
                appended_value = self.variables.get(append_variable, "")
                injection = f"{injection} {appended_value}".strip()
            
            return injection
        
        # Replace all matches in the HTML
        return self.INSERT_REGEX.sub(replace_insert, html)



# Example Usage
# variables = {
#     "status_code": "404",
#     "status_message": "Not Found"
# }

# html_content = """
# <html>
#     <body>
#         <h1>Error Page</h1>
#         <p>Status: <insert status_code or='999' and=status_message /></p>
#         <p>Default: <insert missing_variable or="default_value" /></p>
#     </body>
# </html>
# """

# injector = QuiggleHTMLInjector(variables)
# result = injector.inject(html_content)
# print(result)