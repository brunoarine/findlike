from findlike.markup import Markup
from textwrap import dedent

class TestMarkup:
    def test_remove_org_front_matter(self):
        content = """
        :PROPERTIES:
        :ID: 123
        :END:
        #+TITLE: Example
        This is some text.
        ** A heading
        Some more text.
        """
        extension = ".org"
        markup = Markup(extension=extension)
        expected = "This is some text.\n** A heading\nSome more text."
        assert markup.strip_frontmatter(dedent(content)) == expected

    def test_remove_org_front_matter_empty_input(self):
        extension = ".org"
        markup = Markup(extension=extension)
        content = ""
        expected = ""
        assert markup.strip_frontmatter(content) == expected

    def test_remove_org_front_matter_no_front_matter(self):
        extension = ".org"
        markup = Markup(extension=extension)
        content = "This is some text.\n** A heading\nSome more text."
        expected = "This is some text.\n** A heading\nSome more text."
        assert markup.strip_frontmatter(content) == expected
