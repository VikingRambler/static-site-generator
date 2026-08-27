

class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_attributes = ""
        if self.props:
            for key, value in self.props.items():
                html_attributes = html_attributes + f' {key}="{value}"'
        return html_attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        if self.tag == "a":
            return f'<{self.tag} {self.value[0]}="{self.props[1]}>{self.value}</{self.tag}>'
        if self.tag == "img":
            return f'<{self.tag} {self.props[0]}="{self.props[1]}" {self.props[2]}="{self.props[3]}" />'

    def __repr__(self):
            return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{children_html}"
            f"</{self.tag}>"
        )

    

            