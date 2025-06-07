from textnode import TextType
from textnode import TextNode

def main():
    test_textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print (test_textnode)

if __name__ == "__main__":
    main()

