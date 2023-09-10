import re

from typing import Optional


def urljoin(*paths, base_url: str, sep: Optional[str] = "/"):
    """Custom urljoin function because urllib.parse.urljoin is a bit dumb about multiple positional args.
    :param *paths: elements that form path locations
    :param base_url: the base url that paths are joined to, this should include the scheme; for example:
                       'https://example.org'
    :param sep: path seperator character; default is '/'"""
    fslash_reg = re.compile(fr"{sep}{2,}")  # pattern to make sure paths only have single '/'
    scheme_reg = re.compile(r":/{3,}")  # pattern to make sure scheme only has '://'
    paths = fslash_reg.sub(sep, f"{sep}".join(str(p) for p in paths if p))
    url = scheme_reg.sub("://", f"{base_url}{'/' if not base_url.endswith('/') else ''}{paths}")

    return url
