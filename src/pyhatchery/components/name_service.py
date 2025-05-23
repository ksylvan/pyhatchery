"""Project name validation functions."""

import keyword
import re

_PEP503_VALID_RE = re.compile(
    r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$",
    re.IGNORECASE | re.ASCII,
)
_MAX_LEN = 32


def pep503_normalize(name: str) -> str:
    """Return a PEP 503-compatible normalized slug from the input name.
    Normalization involves:
    1. Converting to lowercase.
    2. Replacing any character not in [a-z0-9._-] with a hyphen.
    3. Replacing all runs of the characters ., _, or - with a single hyphen.
    4. Stripping leading/trailing hyphens.

    This ensures the resulting slug is suitable for use in contexts
    expecting PEP 503 normalized names, even if the input contained
    characters outside the typical set.

    See https://peps.python.org/pep-0503 for the base normalization rules.

    Args:
        name (str): The name to normalize and slugify.
    Returns:
        str: The PEP 503-compatible normalized slug.
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"[-_.]+", "-", name)
    name = name.strip("-")
    return name


def derive_python_package_slug(name: str) -> str:
    """
    Derives a Python package slug from a project name.
    Converts to lowercase, replaces separators with underscores,
    and ensures it's a valid Python identifier.

    Args:
        name: The project name.

    Returns:
        A string suitable for use as a Python package name or throws ValueError
    """
    slug = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    slug = slug.lower()
    slug = re.sub(r"_+", "_", slug)
    slug = slug.strip("_")

    if not slug:
        raise ValueError(
            f"Derived Python package slug from {name} is empty. "
            "Please provide a valid project name."
        )

    if keyword.iskeyword(slug):
        raise ValueError(
            f"Derived Python package slug from {name} is a reserved keyword. "
            "Please provide a valid project name."
        )
    if slug[0].isdigit():
        raise ValueError(
            f"Derived Python package slug from {name} starts with a digit. "
            "Please provide a valid project name."
        )

    return slug


def is_valid_python_package_name(slug: str) -> tuple[bool, str | None]:
    """
    Checks if the given slug is a valid PEP 8 Python package name.
    - Must be a valid Python identifier.
    - Must be all lowercase.
    - Should only contain lowercase letters, numbers (not starting), and underscores.

    Args:
        slug: The Python package slug to validate.

    Returns:
        A tuple (is_valid, message). Message is None if valid.
    """
    if not slug:
        return False, "Python package slug cannot be empty."
    if not slug.isidentifier():
        return (
            False,
            f"Derived Python package slug '{slug}' is not a valid Python identifier "
            "(e.g., cannot start with a digit or contain hyphens/spaces).",
        )
    if not slug.islower():
        return (
            False,
            f"Derived Python package slug '{slug}' should be all lowercase.",
        )
    return True, None


def pep503_name_ok(project_name: str) -> tuple[bool, str | None]:
    """
    Args:
        project_name (str): The name of the project to validate.

    Returns:
        bool: True if the project name is valid, False otherwise.
        str: An error message if the project name is invalid, None otherwise.

    Implemented checks
    ------------------
    1. PEP503 compliance: Must start and end with a letter or digit, and may contain
       letters, digits, periods, underscores, or hyphens in between
    2. ASCII only: Only ASCII characters are allowed
    3. Short: 32 chars max (pragmatic upper bound)
    4. Limited underscores: No more than 2 underscores allowed
    """
    if not _PEP503_VALID_RE.match(project_name):
        return (
            False,
            f"Project name '{project_name}' violates PEP 503 conventions.",
        )
    if len(project_name) > _MAX_LEN:
        return (
            False,
            f"Project name '{project_name}' is too long (max {_MAX_LEN} chars).",
        )
    if (project_name.count("_") + project_name.count("-")) > 2:
        return False, "Project name contains too many underscores or dashes."
    return True, None


def has_invalid_characters(name: str) -> tuple[bool, str]:
    """
    Check if the project name contains characters that are not allowed.
    This is a stricter check than PEP503 normalization, which simply
    replaces invalid chars.

    Some characters like '!' should be rejected outright rather than
    silently normalized.

    Args:
        name: The project name to check for invalid characters

    Returns:
        tuple[bool, str]: (has_invalid, error_message)
            - has_invalid: True if the name contains invalid characters
            - error_message: The invalid characters found, or the empty string if valid
    """
    invalid_chars = "!@#$%^&*+=}{[]|\\/:;\"'<>"

    found_invalid = [char for char in invalid_chars if char in name]

    if found_invalid:
        chars_str = ", ".join([f"'{c}'" for c in found_invalid])
        return True, f"Project name contains invalid characters: {chars_str}"

    return False, ""
