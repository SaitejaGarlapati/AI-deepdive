from typing import TypedDict, Optional, List

class GraphState(TypedDict, total=False):
    question: str
    context: Optional[str]
    answer: Optional[str]
    traces: List[str]
