from pathlib import Path
from requests.models import Response
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


Function = Callable
ListDict = List[Dict[Any, Any]]
ListInt = List[int]
ListString = List[str]
ListTupleString = List[Tuple[str, str]]
OptionalDict = Optional[Dict[Any, Any]]
OptionalListAny = Optional[List[Any]]
OptionalListDict = Optional[List[Dict[Any, Any]]]
OptionalListInt = Optional[List[int]]
OptionalListString = Optional[List[str]]
OptionalResponse = Optional[Response]
OptionalString = Optional[str]
RequestsResponse = Response
RequiredDict = Dict[Any, Any]
TupleInt = Tuple[int, int]
TupleAny = Tuple[Any, ...]
UnionIntString = Union[int, str]
UnionStringPath = Union[str, Path]
