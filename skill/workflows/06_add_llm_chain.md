# Workflow: Add a New LangChain or LangGraph Chain
---
description: How to add a new AI generation chain to any feature
---

## Option A: Simple LangChain Chain (short content)

Used for: social posts, ad copy, email, product descriptions, scripts

```python
# In drivers/ai/<feature>_chain.py

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider

class MyFeatureAIService:
    def __init__(self) -> None:
        provider = get_llm_provider()
        from app.infrastructure.ai.llm_factory import OpenAIProvider
        if isinstance(provider, OpenAIProvider):
            self._llm = provider.get_langchain_llm()
    
    async def generate(self, input_text: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert... [system instructions]"),
            ("human", "Generate: {input}"),
        ])
        chain = prompt | self._llm | StrOutputParser()
        return await chain.ainvoke({"input": input_text})
```

## Option B: Multi-step LangGraph Graph (long/complex content)

Used for: article writer, blog generator (when quality matters most)

```python
# In drivers/ai/<feature>_graph.py

from typing import TypedDict
from langgraph.graph import StateGraph, END

class MyState(TypedDict):
    input: str
    step1_result: str
    step2_result: str
    final_output: str

async def step1_node(state: MyState) -> MyState:
    # ... call LLM
    return {**state, "step1_result": result}

async def step2_node(state: MyState) -> MyState:
    # ... call LLM using step1_result
    return {**state, "step2_result": result}

def build_graph():
    graph = StateGraph(MyState)
    graph.add_node("step1", step1_node)
    graph.add_node("step2", step2_node)
    graph.set_entry_point("step1")
    graph.add_edge("step1", "step2")
    graph.add_edge("step2", END)
    return graph.compile()

my_graph = build_graph()
```

## Switching LLM Provider
Change `LLM_PROVIDER=anthropic` in `.env` — no code changes needed.
All chains use `get_llm_provider()` which reads from config.

## Prompt Engineering Tips
1. Always set a clear **system role** 
2. Specify **output format** explicitly (JSON, markdown, bullet list)
3. Use **few-shot examples** for complex outputs
4. Add **length constraints** to system prompt
5. For JSON output: validate with `json.loads()` + regex fallback
