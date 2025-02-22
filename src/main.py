from textnode import TextNode, TextType


def main() -> None:
    text_node: TextNode = TextNode("This is bold text node", TextType.BOLD,
                                   "https://www.boot.dev")
    print(repr(text_node))


if __name__ == "__main__":
    main()
