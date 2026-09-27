from html.parser import HTMLParser

class TelegraphHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.current_node = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ['h3', 'h4', 'p', 'ul', 'li', 'strong', 'em', 'br', 'hr']:
            node = {'tag': tag, 'children': []}
            if self.stack:
                self.stack[-1]['children'].append(node)
            else:
                self.nodes.append(node)
            self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1]['tag'] == tag:
            self.stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if text and self.stack:
            self.stack[-1]['children'].append(text)
        elif text and not self.stack:
            self.nodes.append({'tag': 'p', 'children': [text]})

def html_to_telegraph_nodes(html_str):
    parser = TelegraphHTMLParser()
    parser.feed(html_str)
    return parser.nodes
