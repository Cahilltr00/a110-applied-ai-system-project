# System Diagram

```mermaid
flowchart TD
    subgraph KB["📚 Knowledge Base"]
        DOCS[knowledge_base.py\n32 Q&A Documents]
        CHROMA[(ChromaDB\nVector Store)]
        DOCS -->|upsert on startup| CHROMA
    end

    subgraph RAG["🔍 RAG Pipeline"]
        RETRIEVER["Retriever\nretrieve_questions()"]
        GRADER["Grader\ngrade_answer()"]
        PROMPT["Augmented Prompt\n─────────────────\nQuestion\nCorrect Answer\nStudent's Answer"]
        CLAUDE["☁️ Claude Haiku\nLLM Generator"]

        CHROMA -->|top N matching questions| RETRIEVER
        GRADER --> PROMPT
        PROMPT --> CLAUDE
        CLAUDE -->|YES or NO\n+ feedback sentence| GRADER
    end

    subgraph UI["🖥️ Streamlit UI  ·  app.py"]
        SELECT["Category Selector"]
        DISPLAY["Question Display"]
        INPUT["Answer Input"]
        FEEDBACK["Feedback + Score"]
    end

    subgraph TESTING["🧪 Testing System"]
        PYTEST["pytest"]
        LOGIC["test_game_logic.py\n────────────────\nscore logic\nretrieval structure\ncategory filtering"]
        EVAL["test_grader_eval.py\n────────────────\nYES / NO parsing\nedge cases\nprompt contents"]
        MOCK["Mock Claude\nunittest.mock\n(no API key needed)"]

        PYTEST --> LOGIC
        PYTEST --> EVAL
        EVAL -->|replaces real Claude| MOCK
        MOCK -->|fake response| GRADER
        LOGIC -->|calls real ChromaDB| CHROMA
    end

    HUMAN["👤 User"]
    DEV["👩‍💻 Developer"]

    HUMAN -->|"① pick category"| SELECT
    SELECT -->|"② query by category"| RETRIEVER
    RETRIEVER -->|"③ return questions"| DISPLAY
    DISPLAY -->|"④ show question"| HUMAN
    HUMAN -->|"⑤ type answer"| INPUT
    INPUT -->|"⑥ question + answer"| GRADER
    GRADER -->|"⑦ verdict + feedback"| FEEDBACK
    FEEDBACK -->|"⑧ show result, update score"| HUMAN

    DEV -->|runs| PYTEST
    PYTEST -->|"✅ pass / ❌ fail report"| DEV
```

## Component Summary

| Component | File | Role |
|---|---|---|
| Knowledge Base | `knowledge_base.py` | 32 static Q&A documents |
| Vector Store | ChromaDB (in-memory) | Stores + retrieves documents by semantic similarity |
| Retriever | `rag_utils.retrieve_questions()` | Queries ChromaDB by category, returns N questions |
| Grader | `rag_utils.grade_answer()` | Builds augmented prompt, parses Claude's response |
| Generator | Claude Haiku (Anthropic API) | Produces YES/NO verdict + kid-friendly feedback |
| UI | `app.py` | Streamlit interface — ties all components together |
| Logic Tests | `tests/test_game_logic.py` | Deterministic tests for scoring and retrieval |
| Eval Tests | `tests/test_grader_eval.py` | Mocked tests for AI grading pipeline |

## Where Humans Are Involved

- **User** — selects category, reads questions, submits answers, sees feedback
- **Developer** — runs `pytest` to verify the system behaves correctly before/after changes
- **Mock layer** — replaces Claude in tests so developers can check the parsing logic without API cost or network dependency
