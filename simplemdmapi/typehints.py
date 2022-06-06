from pathlib import Path
from requests.models import Response
from typing import Any, Dict, List, Optional, Tuple, Union


ListDict = List[Dict[Any, Any]]
ListInt = List[int]
ListString = List[str]
ListTupleString = List[Tuple[str, str]]
OptionalDict = Optional[Dict[Any, Any]]
OptionalListDict = Optional[List[Dict[Any, Any]]]
OptionalListInt = Optional[List[int]]
OptionalListString = Optional[List[str]]
OptionalResponse = Optional[Response]
OptionalString = Optional[str]
RequestsResponse = Response
RequiredDict = Dict[Any, Any]
TupleInt = Tuple[int, int]
UnionIntString = Union[int, str]
UnionStringPath = Union[str, Path]
