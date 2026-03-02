from typing import Any, Dict, Union
import json

class Token:
    """Base token class for polymorphic processing."""

    def __init__(self, content: Any) -> None:
        self.content = content

    def clean(self, config: Dict[str, Any]) -> Any:
        # This will be imported or injected to avoid circularity with registry
        from config.registry import apply_filters
        return apply_filters(self.content, config)

    def serialize(self, cleaned: Any) -> str:
        """Serialize the cleaned content to string."""
        return str(cleaned)

    def process(self, config: Dict[str, Any]) -> str:
        """Clean and serialize the token."""
        return self.serialize(self.clean(config))


class Line(Token):
    """Token representing a line of text."""

    def serialize(self, cleaned: str) -> str:
        return cleaned + "\n"


class StructuralToken(Token):
    """Token for JSON structural characters (braces, brackets, commas)."""

    def clean(self, config: Dict[str, Any]) -> str:
        return str(self.content)

    def serialize(self, cleaned: str) -> str:
        return cleaned


class StringValueToken(Token):
    """Token for JSON string values."""

    def serialize(self, cleaned: str) -> str:
        return json.dumps(cleaned, ensure_ascii=False)


class KeyToken(Token):
    """Token for JSON object keys."""

    def serialize(self, cleaned: str) -> str:
        return json.dumps(cleaned, ensure_ascii=False) + ":"


class NumberToken(Token):
    """Token for JSON number values."""

    def clean(self, config: Dict[str, Any]) -> Any:
        return self.content

    def serialize(self, cleaned: Any) -> str:
        return json.dumps(cleaned)


class BoolNullToken(Token):
    """Token for JSON boolean and null values."""

    def clean(self, config: Dict[str, Any]) -> Any:
        return self.content

    def serialize(self, cleaned: Any) -> str:
        return json.dumps(cleaned)


class NewlineToken(Token):
    """Token representing a newline character."""

    def __init__(self) -> None:
        super().__init__("\n")

    def clean(self, config: Dict[str, Any]) -> str:
        return str(self.content)

    def serialize(self, cleaned: str) -> str:
        return cleaned

class HashToken(Token):
    """Token to represent the before_hash."""
    def __init__(self, content: str) -> None:
        super().__init__(content)

    def clean(self, config: Dict[str, Any]) -> str:
        return self.content
    
    def serialize(self, cleaned: str) -> str:
        return cleaned

class RuleToken(Token):
    """Token representing a schema coercion rule that was applied."""
    def __init__(self, content: Dict[str, Any]) -> None:
        super().__init__(content)

    def clean(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self.content
    
    def serialize(self, cleaned: Dict[str, Any]) -> str:
        return ""
