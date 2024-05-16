from typing import Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence["HTMLNode"] | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"'
        return result

    def __repr__(self) -> str:
        return (
            f"HTMLNode('{self.tag}', '{self.value}', '{self.children}', '{self.props}')"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value is required")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode('{self.tag}', '{self.value}', '{self.props})'"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str | None, children: Sequence[HTMLNode], props: dict | None = None
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Must provide a tag")
        if not self.children:
            raise ValueError("Parent has no children")

        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += f"{child.to_html()}"

        result += f"</{self.tag}>"

        return result

    def __repr__(self):
        return f"ParentNode('{self.tag}', '{self.children}', '{self.props})'"
