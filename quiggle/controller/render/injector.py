import re

class HTMLInjector:
    """HTML injector system for parsing and injecting content into custom <insert> tags."""
    
    # Regex for parsing <insert> tags
    INSERT_REGEX = re.compile(r"<use\s+(\w+)(?:\s+or=['\"](.*?)['\"])?(?:\s+and=['\"](.*?)['\"])?\s*\/?>")
    
    def __init__(self, variables=None):
        """
        Initialize with a dictionary of variables.
        :param variables: Dict containing variable names and their values.
        """
        self.variables     = variables or {}
        self.instances     = {}
        self.position: int = 0
        self.hold_pos: int = 0
        self.tags          = [
                                'use'
                            ]

    def get_char(self) -> str:
        return self.html['raw'][self.position]

    def get_next_char(self) -> str:
        if len(self.html['raw']) - 1 > self.position:
            return self.html['raw'][self.position + 1]
        return ' '
    
    def increment_positions(self) -> None:
        if len(self.html['raw']) - 1 > self.position:
            self.position += 1
            self.hold_pos = self.position

    def find_open_tag(self):
        if not self.get_char() == '<':
            return self.increment_positions()
        self.find_next_blank()

    def find_next_blank(self):
        self.position += 1
        if self.get_char() == '>':
            return self.increment_positions() 
        if self.get_char() != ' ':
            return self.find_next_blank()
        tag = self.html['raw'][self.hold_pos + 1 : self.position]
        if tag in self.tags:
            # if tag not in self.instances.keys():
                # self.instances[tag] = []
                # pass
            print(tag)
            # self.find_closing_tag(tag)
        self.increment_positions()

    def find_closing_tag(self, tag: str):
        self.position += 1
        if self.get_char() == '/' and self.get_next_char == '>':
            # print(self.html['raw'][self.hold_pos : self.position])
            # self.instances[tag].append(self.html['raw'][self.hold_pos : self.position])
            return
        self.find_closing_tag(tag)

    def find_tags(self) -> None:
        while self.position < len(self.html['raw']):
            self.find_open_tag()

    def inject(self, html: str) -> None:
        """
        Parse and replace all <insert> tags in the provided HTML.
        :param html: The input HTML string.
        :return: The HTML with injected content.
        """


        self.html = html
        self.find_tags()
        print(self.instances)

        '''print(html)
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
        return''' # self.INSERT_REGEX.sub(replace_insert, html)


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