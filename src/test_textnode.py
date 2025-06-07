import unittest

from textnode import TextNode
from textnode import TextType

class TestTextNode(unittest.TestCase):
    def test_init_valid(self):
        """Test successful initialization with valid arguments."""
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

        node_with_url = TextNode("Google", TextType.LINK, "https://google.com")
        self.assertEqual(node_with_url.text, "Google")
        self.assertEqual(node_with_url.text_type, TextType.LINK)
        self.assertEqual(node_with_url.url, "https://google.com")

    def test_init_invalid_text_type(self):
        """Test initialization raises TypeError for invalid text_type."""
        with self.assertRaisesRegex(TypeError, "The 'text_type' property must be an instance of the TextType enum"):
            TextNode("Test", "not_an_enum")
        
        with self.assertRaisesRegex(TypeError, "The 'text_type' property must be an instance of the TextType enum"):
            TextNode("Test", 123) # type: ignore

    def test_eq_equal_nodes(self):
        """Test that two identical TextNode objects are equal."""
        node1 = TextNode("Content", TextType.BOLD)
        node2 = TextNode("Content", TextType.BOLD)
        self.assertEqual(node1, node2)

        node3 = TextNode("Link text", TextType.LINK, "https://example.com")
        node4 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node3, node4)

    def test_eq_different_text(self):
        """Test that TextNodes with different text are not equal."""
        node1 = TextNode("Text A", TextType.TEXT)
        node2 = TextNode("Text B", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text_type(self):
        """Test that TextNodes with different text_type are not equal."""
        node1 = TextNode("Same text", TextType.ITALIC)
        node2 = TextNode("Same text", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        """Test that TextNodes with different URLs are not equal."""
        node1 = TextNode("Link", TextType.LINK, "https://url1.com")
        node2 = TextNode("Link", TextType.LINK, "https://url2.com")
        node3 = TextNode("Link", TextType.LINK, None)
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node3)
        
        # Test one with URL, one without
        node4 = TextNode("Image", TextType.IMAGE, "path/to/image.png")
        node5 = TextNode("Image", TextType.IMAGE) # URL is None by default
        self.assertNotEqual(node4, node5)

    def test_eq_different_types(self):
        """Test that a TextNode is not equal to an object of a different type."""
        node = TextNode("Hello", TextType.TEXT)
        other_object = "Just a string"
        self.assertNotEqual(node, other_object)
        self.assertFalse(node == other_object) # Also checking direct ==
        self.assertTrue(node != other_object)  # Also checking direct !=

    def test_repr_no_url(self):
        """Test the __repr__ method when URL is None."""
        node = TextNode("Code block", TextType.CODE)
        # Expected: TextNode('Code block', 'code', None)
        self.assertEqual(repr(node), "TextNode('Code block', 'code', None)")

    def test_repr_with_url(self):
        """Test the __repr__ method when URL is provided."""
        node = TextNode("Visit Us", TextType.LINK, "https://example.com/page")
        # Expected: TextNode('Visit Us', 'link', 'https://example.com/page')
        self.assertEqual(repr(node), "TextNode('Visit Us', 'link', 'https://example.com/page')")

    def test_repr_image_with_url(self):
        """Test the __repr__ method for an image node."""
        node = TextNode("My Pic", TextType.IMAGE, "/img/logo.png")
        # Expected: TextNode('My Pic', 'image', '/img/logo.png')
        self.assertEqual(repr(node), "TextNode('My Pic', 'image', '/img/logo.png')")

if __name__ == "__main__":
    unittest.main()