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

    def is_position_lt_len(self) -> bool:
        return len(self.html['raw']) - 1 > self.position

    def get_char(self) -> str:
        return self.html['raw'][self.position]

    def get_next_char(self) -> str:
        if self.is_position_lt_len():
            return self.html['raw'][self.position + 1]
        return self.get_char()
    
    def increment_positions(self) -> None:
        if self.is_position_lt_len():
            self.position += 1
            self.hold_pos = self.position

    def find_tags(self) -> None:
        while self.position < len(self.html['raw']) - 1:
            self.find_open_tag()

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
            if tag not in self.instances.keys():
                self.instances[tag] = []
            return self.find_closing_tag(tag)
        return self.increment_positions()

    def find_closing_tag(self, tag: str):
        self.position += 1
        if self.get_char() == '/' and self.get_next_char() == '>':
            self.instances[tag].append(self.html['raw'][self.hold_pos : self.position + 2])
            return self.increment_positions()
        return self.find_closing_tag(tag)

    def inject(self, html: str) -> None:
        """
        Parse and replace all <insert> tags in the provided HTML.
        :param html: The input HTML string.
        :return: The HTML with injected content.
        """


        self.html = html
        self.find_tags()
        for tag in self.instances.keys():
            for instance in self.instances[tag]:
                content       = ''
                default_value = ''
                split_string  = instance[1:-2].split(' ')
                variable      = split_string[1]
                attributes    = [item for item in ' '.join(split_string[2:]).replace('=', ' ').split(' ') if item != '']
                if attributes[0] == 'or':
                    default_value = attributes[1]
                if variable in self.variables: content += self.variables[variable]
                else: content += default_value

                self.html['final'] = self.html['final'].replace(instance, content)