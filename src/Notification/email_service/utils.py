import re


def extract_variables(template_content: str) -> set:
    """Extract variables from a template string using regex."""
    # Match {{ variable }} pattern
    pattern = r"{{\s*([a-zA-Z0-9_]+)\s*}}"
    return set(re.findall(pattern, template_content))
