import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization_defaults(self):
        """Test HTMLNode initialization with all default (None) values."""
        node = HTMLNode()
        self.assertIsNone(node.tag, "Default tag should be None")
        self.assertIsNone(node.value, "Default value should be None")
        self.assertIsNone(node.children, "Default children should be None")
        self.assertIsNone(node.props, "Default props should be None")

    def test_initialization_with_tag_and_value(self):
        """Test HTMLNode initialization with specified tag and value."""
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_all_arguments(self):
        """Test HTMLNode initialization with all arguments provided."""
        child_node = HTMLNode(tag="span", value="Child text")
        node = HTMLNode(
            tag="div",
            value="Parent value", # A div with children might not typically have a direct value
            children=[child_node],
            props={"id": "main", "class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Parent value")
        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], HTMLNode)
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.props, {"id": "main", "class": "container"})

    def test_props_to_html_props_is_none(self):
        """Test props_to_html when props is None."""
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_props_is_empty_dict(self):
        """Test props_to_html when props is an empty dictionary."""
        node = HTMLNode(tag="p", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_property(self):
        """Test props_to_html with a single property."""
        node = HTMLNode(tag="a", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')

    def test_props_to_html_with_multiple_properties(self):
        """Test props_to_html with multiple properties."""
        # In Python 3.7+ dicts preserve insertion order, which props_to_html relies on.
        # For older Pythons, the order of attributes in the string might vary.
        props_dict = {"src": "image.jpg", "alt": "An image"}
        node = HTMLNode(tag="img", props=props_dict)
        expected_html_attrs = ' src="image.jpg" alt="An image"'
        
        # A more robust test if order is not strictly guaranteed (though it should be for 3.7+)
        # self.assertIn(' src="image.jpg"', node.props_to_html())
        # self.assertIn(' alt="An image"', node.props_to_html())
        # self.assertTrue(node.props_to_html().startswith(" "))
        
        self.assertEqual(node.props_to_html(), expected_html_attrs)

    def test_repr_method_defaults(self):
        """Test the __repr__ method with default values."""
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")

    def test_repr_method_with_values(self):
        """Test the __repr__ method with specific values and nested children."""
        child_node = HTMLNode(tag="strong", value="text")
        node = HTMLNode(
            tag="p",
            value="Some paragraph.",
            children=[child_node],
            props={"class": "text-class"}
        )
        expected_repr = "HTMLNode('p', 'Some paragraph.', [HTMLNode('strong', 'text', None, None)], {'class': 'text-class'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_raises_not_implemented_error(self):
        """Test that the base to_html method raises NotImplementedError."""
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        """🧪 Test that to_html returns only the value when tag is None."""
        node = LeafNode(value="Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")

    def test_to_html_with_tag_no_props(self):
        """🧪 Test to_html with a tag and value but no props."""
        node = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_to_html_with_tag_and_props(self):
        """🧪 Test to_html with tag, value, and props."""
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_to_html_no_value_raises_error(self):
        """🧪 Test that to_html raises a ValueError if value is None."""
        node = LeafNode(tag="p")
        with self.assertRaisesRegex(ValueError, "A LeafNode must have a value."):
            node.to_html()

    def test_props_to_html_no_props(self):
        """🧪 Test props_to_html when props is None (inherited functionality)."""
        node = LeafNode(tag="p", value="Test")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        """🧪 Test props_to_html with props (inherited functionality)."""
        node = LeafNode(tag="img", value="", props={"src": "image.png", "alt": "My Image"})
        # The order of attributes can vary in dictionaries before Python 3.7,
        # but string join order should be consistent with item insertion for modern Pythons.
        # For robustness, could check for inclusion of each prop string.
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="My Image"') # Note leading space

    def test_repr_output(self):
        """🧪 Test the __repr__ method for accurate representation."""
        node = LeafNode(tag="span", value="Content", props={"class": "bold"})
        expected_repr = "LeafNode('span', 'Content', None, {'class': 'bold'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_empty_value_allowed(self):
        """🧪 Test that an empty string value is allowed."""
        node = LeafNode(tag="p", value="")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_value_with_special_chars(self):
        """🧪 Test to_html with a value containing special HTML characters (no escaping is done by this class)."""
        node = LeafNode(tag="p", value="<Hello & World>")
        self.assertEqual(node.to_html(), "<p><Hello & World></p>")

    def test_to_html_props_with_special_chars_in_value(self):
        """🧪 Test to_html with props whose values contain special characters."""
        node = LeafNode(tag="a", value="Link", props={"href": "https://example.com?param1=a&param2=b"})
        self.assertEqual(node.to_html(), '<a href="https://example.com?param1=a&param2=b">Link</a>')

class TestParentNode(unittest.TestCase):

    def test_basic_rendering(self):
        """Test ParentNode with simple LeafNode children."""
        # For LeafNode to pass, value must not be None
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, " and normal text."),
                LeafNode("i", " Italic text."),
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b> and normal text.<i> Italic text.</i></p>")

    def test_rendering_with_props(self):
        """Test ParentNode with HTML properties."""
        node = ParentNode(
            "a",
            [LeafNode(None, "Click me!")],
            {"href": "https://www.example.com", "target": "_blank"}
        )
        actual_html = node.to_html()
        # Order of props can vary, check for essential parts
        self.assertTrue(actual_html.startswith("<a"))
        self.assertIn(' href="https://www.example.com"', actual_html)
        self.assertIn(' target="_blank"', actual_html)
        self.assertTrue(actual_html.endswith(">Click me!</a>"))


    def test_nested_parent_nodes(self):
        """Test ParentNode containing another ParentNode."""
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Header"),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a paragraph with "),
                        LeafNode("strong", "bold text"),
                        LeafNode(None, " inside."),
                    ],
                    {"class": "inner-paragraph"}
                )
            ],
            {"id": "outer-div", "style": "color: blue;"}
        )
        
        actual_html = node.to_html()
        # Check for parts due to potential prop order variation
        self.assertTrue(actual_html.startswith("<div"))
        self.assertIn(' id="outer-div"', actual_html)
        self.assertIn(' style="color: blue;"', actual_html)
        self.assertIn('<h1>Header</h1>', actual_html)
        self.assertIn('<p class="inner-paragraph">This is a paragraph with <strong>bold text</strong> inside.</p>', actual_html)
        self.assertTrue(actual_html.endswith("</div>"))

    # Corrected: Tests for errors raised by to_html when init args are None,
    # as per your original class definitions.
    def test_to_html_raises_error_if_tag_is_none_from_constructor(self):
        """Test to_html raises ValueError if tag was None from constructor."""
        # Your constructor allows tag=None
        node = ParentNode(None, [LeafNode(None, "Child")])
        with self.assertRaisesRegex(ValueError, "ParentNode object must have tag\\."):
            node.to_html() # Error is raised here

    def test_to_html_raises_error_if_children_is_none_from_constructor(self):
        """Test to_html raises ValueError if children was None from constructor."""
        # Your constructor allows children=None
        node = ParentNode("div", None) # type: ignore
        with self.assertRaisesRegex(ValueError, "ParentNode object must have children nodes\\."):
            node.to_html() # Error is raised here

    def test_to_html_children_set_to_none_post_init(self):
        """Test ValueError from to_html if children is set to None after instantiation."""
        node = ParentNode("p", [LeafNode(None, "Initial child")])
        node.children = None # Manually set children to None
        # Regex matches the error message from your ParentNode.to_html
        with self.assertRaisesRegex(ValueError, "ParentNode object must have children nodes\\."):
            node.to_html()
            
    def test_to_html_tag_set_to_none_post_init(self):
        """Test ValueError from to_html if tag is set to None after instantiation."""
        node = ParentNode("p", [LeafNode(None, "Child")])
        node.tag = None # Manually set tag to None
        # Regex matches the error message from your ParentNode.to_html
        with self.assertRaisesRegex(ValueError, "ParentNode object must have tag\\."):
            node.to_html()

    def test_empty_children_list(self):
        """Test ParentNode with an empty list of children."""
        node = ParentNode("div", [], {"class": "empty-container"})
        self.assertEqual(node.to_html(), '<div class="empty-container"></div>')

    def test_parent_node_with_no_props(self):
        """Test ParentNode renders correctly without any props."""
        node = ParentNode("section", [LeafNode("h2", "A Section")])
        self.assertEqual(node.to_html(), "<section><h2>A Section</h2></section>")
        
    def test_repr_method(self):
        """Test the __repr__ method for ParentNode."""
        # LeafNode default for children and props is None
        # HTMLNode __init__ sets value to None if not provided for ParentNode
        leaf = LeafNode("b", "Bold") # props will be None
        node = ParentNode("p", [leaf], {"class": "text"})
        # Corrected expected_repr based on HTMLNode.__repr__
        # ParentNode: tag='p', value=None, children=[leaf], props={...}
        # LeafNode: tag='b', value='Bold', children=None, props=None
        expected_repr = "ParentNode('p', None, [LeafNode('b', 'Bold', None, None)], {'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

    def test_leafnode_requires_value_in_to_html(self):
        """Test LeafNode.to_html raises ValueError if value is None."""
        # Your LeafNode constructor allows value=None
        node = LeafNode(tag="span", value=None) 
        # The error is raised by to_html, as per your LeafNode definition
        with self.assertRaisesRegex(ValueError, "A LeafNode must have a value."):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()