def urljoin(*args) -> str:
    """Join a series of string objects together into a url."""
    return "/".join(str(s).removesuffix("/") for s in args)
