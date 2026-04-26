import os
import chromadb
import anthropic
from knowledge_base import DOCS


def get_collection():
    """Create an in-memory ChromaDB collection and ingest all knowledge base docs."""
    client = chromadb.Client()
    collection = client.get_or_create_collection("trivia")
    _ingest_docs(collection)
    return collection


def _ingest_docs(collection):
    """Upsert all knowledge base documents into the collection."""
    collection.upsert(
        ids=[doc["id"] for doc in DOCS],
        documents=[doc["question"] for doc in DOCS],
        metadatas=[
            {"answer": doc["answer"], "category": doc["category"]}
            for doc in DOCS
        ],
    )


def retrieve_questions(collection, category: str, n: int = 5) -> list[dict]:
    """
    Retrieve n questions matching the given category.
    Uses semantic search on the category string, then filters by metadata.
    """
    results = collection.query(
        query_texts=[category],
        n_results=min(n, len(DOCS)),
        where={"category": category},
    )
    questions = []
    for i, doc_id in enumerate(results["ids"][0]):
        questions.append({
            "id": doc_id,
            "question": results["documents"][0][i],
            "answer": results["metadatas"][0][i]["answer"],
            "category": results["metadatas"][0][i]["category"],
        })
    return questions[:n]


def grade_answer(question: str, correct_answer: str, user_answer: str) -> tuple[bool, str]:
    """
    Use Claude to grade a free-text answer.
    Returns (is_correct, feedback_message).
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    prompt = (
        f"Question: {question}\n"
        f"Correct answer: {correct_answer}\n"
        f"Student's answer: {user_answer}\n\n"
        "Is the student's answer correct? Reply with exactly two lines:\n"
        "Line 1: YES or NO\n"
        "Line 2: One short, friendly sentence of feedback for a kindergartener."
    )
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    response = message.content[0].text.strip()
    lines = response.splitlines()
    is_correct = lines[0].strip().upper().startswith("YES")
    feedback = lines[1].strip() if len(lines) > 1 else ("Great job!" if is_correct else f"The answer was {correct_answer}.")
    return is_correct, feedback
