import re

class Markup:
    def __init__(self, extension: str):
        self.extension = extension
        self._MARKUP_EXTENSIONS = {
            ".org": self._strip_org_frontmatter
        }

    def strip_frontmatter(self, text: str) -> str:
            if self.extension in self._MARKUP_EXTENSIONS.keys():
                return self._MARKUP_EXTENSIONS[self.extension](text)
            else:
                return text

    def _strip_org_frontmatter(self, content: str) -> str:
        """
        Remove front matter from a string representing an Org-mode file.

        This function removes all lines from `:PROPERTIES:` to `:END:` 
        and any lines starting with `#+` from the given content string.

        Args:
            content (str): The content of an Org-mode file as a string.

        Returns:
            str: The content with the front matter removed.

        Example:
            >>> content = '''
            ... :PROPERTIES:
            ... :ID: 123
            ... :END:
            ... #+TITLE: Example
            ... This is some text.
            ... ** A heading
            ... Some more text.
            ... '''
            >>> cleaned_content = remove_front_matter(content)
            >>> print(cleaned_content)
            This is some text.
            ** A heading
            Some more text.
        """
        # Remove :PROPERTIES: to :END: block
        content = re.sub(r':PROPERTIES:(.|\n)*?:END:', '', content)
        
        # Remove lines starting with #+
        pattern = r'^\s*#\+[a-zA-Z0-9_]+.*?$'
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        return content.strip()