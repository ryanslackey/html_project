import unittest
from enum import Enum
from converters import text_node_to_html_node
from converters import split_nodes_delimiter
from htmlnode import LeafNode
from textnode import TextNode
from textnode import TextType

class TestTextNodeToHtmlNode(unittest.TestCase):

    # Test cases for TextNode constructor validation
    def test_text_node_constructor_invalid_type(self):
        class InvalidTextType(Enum): # A type not part of the official TextType
            INVALID = "invalid_custom"
        with self.assertRaisesRegex(TypeError, "The 'text_type' property must be an instance of the TextType enum"):
            TextNode("Invalid type text", InvalidTextType.INVALID)

    def test_text_node_constructor_none_type(self):
        with self.assertRaisesRegex(TypeError, "The 'text_type' property must be an instance of the TextType enum"):
            TextNode("None type text", None)

    # Test cases for text_node_to_html_node conversion
    def test_convert_text_type(self):
        text_node = TextNode("This is a plain text.", TextType.TEXT)
        # Based on traceback, expecting props=None implicitly
        # And assuming tag=None, children=None by default in LeafNode constructor
        expected_leaf_node = LeafNode(tag=None, value="This is a plain text.", props=None)
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_convert_bold_type(self):
        text_node = TextNode("This is bold text.", TextType.BOLD)
        # Expecting props=None implicitly
        expected_leaf_node = LeafNode(tag="b", value="This is bold text.", props=None)
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_convert_italic_type(self):
        text_node = TextNode("This is italic text.", TextType.ITALIC)
        expected_leaf_node = LeafNode(tag="i", value="This is italic text.", props=None)
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_convert_code_type(self):
        text_node = TextNode("This is code.", TextType.CODE)
        expected_leaf_node = LeafNode(tag="code", value="This is code.", props=None)
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_convert_link_type(self):
        text_node = TextNode("Click here", TextType.LINK, url="https://www.example.com")
        expected_leaf_node = LeafNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_convert_image_type(self):
        text_node = TextNode("An example image", TextType.IMAGE, url="https://www.example.com/image.png")
        expected_leaf_node = LeafNode(tag="img", value="", props={"src": "https://www.example.com/image.png", "alt": "An example image"})
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)

    def test_conversion_invalid_text_type_in_function(self):
        # This test assumes TextNode allows creation with a TextType member
        # that text_node_to_html_node does not handle.
        # We need a TextType member that is valid for TextNode but not in the match cases.
        # If all TextType members are handled, this specific exception path is hard to test
        # without modifying TextType or text_node_to_html_node.

        # Create a mock TextNode instance with a 'text_type' that will hit the default case
        # This requires careful crafting if TextNode is strict.
        # For this example, let's assume we could (hypothetically) add a new TextType
        # or use a value that somehow bypasses TextNode's check but is not matched.
        # Given the current structure, TextNode's __init__ is stricter.

        # If you have a specific TextType enum member, e.g., TextType.UNHANDLED
        # that TextNode can be created with:
        # text_node = TextNode("Test", TextType.UNHANDLED)
        # with self.assertRaisesRegex(Exception, "TextNode does not have a valid TextType"):
        #    text_node_to_html_node(text_node)
        pass # See comment above, this test case depends on specifics of TextType and TextNode validation.
        

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_empty_input_list(self):
        """Test with an empty list of old_nodes."""
        self.assertEqual(split_nodes_delimiter([], "*", TextType.BOLD), [])

    def test_nodes_not_text_type(self):
        """Test with nodes that are not of text_type TextType.TEXT."""
        nodes = [TextNode("image data", TextType.IMAGE), TextNode("hyperlink", TextType.LINK)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), nodes)

    def test_text_node_no_delimiter_present(self):
        """Test a TextType.TEXT node where the delimiter is not present."""
        nodes = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), nodes)

    def test_valid_split_even_parts_prefix_content(self):
        """Test a valid split: 'prefix*content' -> 2 parts."""
        nodes = [TextNode("prefix*content", TextType.TEXT)]
        expected = [TextNode("prefix", TextType.TEXT), TextNode("content", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), expected)

    def test_valid_split_even_parts_starts_with_delimiter(self):
        """Test a valid split: '*content' -> 2 parts."""
        nodes = [TextNode("*content", TextType.TEXT)]
        expected = [TextNode("", TextType.TEXT), TextNode("content", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), expected)

    def test_valid_split_even_parts_multiple_delimiters(self):
        """Test a valid split: 'a*b*c*d' -> 4 parts."""
        nodes = [TextNode("a*b*c*d", TextType.TEXT)]
        expected = [
            TextNode("a", TextType.TEXT), TextNode("b", TextType.ITALIC),
            TextNode("c", TextType.TEXT), TextNode("d", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), expected)

    def test_valid_split_node_text_is_delimiter_itself(self):
        """Test valid split when node text is just the delimiter: '*' -> 2 parts ["", ""]."""
        nodes = [TextNode("*", TextType.TEXT)]
        expected = [TextNode("", TextType.TEXT), TextNode("", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.CODE), expected)

    def test_valid_split_node_text_is_multiple_delimiters_only_resulting_in_even_parts(self):
        """Test '***' with delimiter '*' -> ['', '', '', ''] (4 parts) """
        nodes = [TextNode("***", TextType.TEXT)] # -> split: ["", "", "", ""]
        expected = [
            TextNode("", TextType.TEXT), TextNode("", TextType.BOLD),
            TextNode("", TextType.TEXT), TextNode("", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), expected)


    def test_invalid_split_odd_parts_typical_markdown_style(self):
        """Test invalid split (odd parts): '*content*' -> 3 parts. Expects Exception."""
        nodes = [TextNode("*content*", TextType.TEXT)] # -> split: ["", "content", ""]
        with self.assertRaisesRegex(Exception, "Invalid Markdown syntax."):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

    def test_invalid_split_odd_parts_text_delimiter_text(self):
        """Test invalid split (odd parts): 'text*content*suffix' -> 3 parts. Expects Exception."""
        nodes = [TextNode("text*content*suffix", TextType.TEXT)] # -> split: ["text", "content", "suffix"]
        with self.assertRaisesRegex(Exception, "Invalid Markdown syntax."):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

    def test_invalid_split_odd_parts_double_delimiter_char(self):
        """Test invalid split (odd parts): '**' with delimiter '*' -> 3 parts. Expects Exception."""
        nodes = [TextNode("**", TextType.TEXT)] # -> split: ["", "", ""]
        with self.assertRaisesRegex(Exception, "Invalid Markdown syntax."):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

    def test_mixed_nodes_one_causes_invalid_markdown_exception(self):
        """Test multiple nodes where one causes an 'Invalid Markdown syntax' exception."""
        nodes = [
            TextNode("prefix*valid_part", TextType.TEXT), # Valid part
            TextNode("*invalid*markdown", TextType.TEXT), # Invalid part, will raise
            TextNode("suffix*another_valid", TextType.TEXT) # Will not be reached
        ]
        with self.assertRaisesRegex(Exception, "Invalid Markdown syntax."):
            split_nodes_delimiter(nodes, "*", TextType.HIGHLIGHT)

    def test_mixed_nodes_all_valid_or_not_applicable(self):
        """Test multiple nodes, all valid or not applicable for splitting."""
        nodes = [
            TextNode("some image", TextType.IMAGE),
            TextNode("prefix*content", TextType.TEXT),
            TextNode("no delimiter here", TextType.TEXT),
            TextNode("*another_content*yet_another*final_content", TextType.TEXT) # 4 parts: "", "another_content", "yet_another", "final_content"
        ]
        expected = [
            TextNode("some image", TextType.IMAGE),
            TextNode("prefix", TextType.TEXT), TextNode("content", TextType.CUSTOM_TYPE),
            TextNode("no delimiter here", TextType.TEXT), # This node should remain TextType.TEXT
            TextNode("", TextType.TEXT), TextNode("another_content", TextType.CUSTOM_TYPE),
            TextNode("yet_another", TextType.TEXT), TextNode("final_content", TextType.CUSTOM_TYPE),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.CUSTOM_TYPE), expected)

    def test_empty_string_node_text(self):
        """Test a TextType.TEXT node with empty string text."""
        nodes = [TextNode("", TextType.TEXT)]
        # "*" in "" is False.
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), [TextNode("", TextType.TEXT)])

    def test_empty_string_delimiter_raises_valueerror(self):
        """Test behavior with an empty string delimiter (causes str.split error)."""
        nodes = [TextNode("abc", TextType.TEXT)]
        # `"" in "abc"` is True. ` "abc".split("") ` raises ValueError.
        with self.assertRaises(ValueError): # Specifically ValueError from split
            split_nodes_delimiter(nodes, "", TextType.BOLD)

    def test_text_node_with_only_non_target_delimiters(self):
        """Test a TextType.TEXT node with different delimiters, not the target one."""
        nodes = [TextNode("hello`code`world", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), nodes)

    def test_complex_delimiters(self):
        """Test with a multi-character delimiter."""
        # Test case for invalid split (5 parts)
        nodes_invalid = [TextNode("text```code```more text```another code```suffix", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown syntax."):
            split_nodes_delimiter(nodes_invalid, "```", TextType.CODE_BLOCK)

        # Test case for valid split (4 parts)
        nodes_valid = [TextNode("text```code```more text```another code", TextType.TEXT)]
        expected_valid = [
            TextNode("text", TextType.TEXT), TextNode("code", TextType.CODE_BLOCK),
            TextNode("more text", TextType.TEXT), TextNode("another code", TextType.CODE_BLOCK)
        ]
        self.assertEqual(split_nodes_delimiter(nodes_valid, "```", TextType.CODE_BLOCK), expected_valid)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)   