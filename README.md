# Name of Original Project:

-> The original project I chose to iterate on was the Game Glitch Investigator. It's original intention was a simple game where the user would guess between 1 and 100. The program would give the user feedback on whether their guess was too high or low, and would continue giving feedback until either the user's guess was correct or there was 7 guesses.

# Title & Summary:

-> TriviaBot Jr is the new version of Game Glitch Investigator. It is still a guessing game but instead of guessing a number the user now types in an answer to a kindergarten level question (e.g. what shape is a wheel?). This is a simple way to implement the AI functionalities that I have learned in this course, I chose to implement RAG and a Testing System for results reliability.

# Architecture Overview:

-> The system starts with a knowledge base of 32 trivia Q&A documents that are loaded into ChromaDB on startup. When a user picks a category the retriever queries ChromaDB and pulls the most relevant questions. The user submits an answer throuhg the Streamlit UI and that answer gets passed through to a Grader, which builds an augmented prompt combining the question, the correct answer and the student's answer. A Claude Haiku returns a YES/NO verict with kid-friendly feedback, the total score is updated and shown to the user. Separately, a testing system tests the retrieval and scoring logic directly when a developer runs pytest. Instead of a true API call, this process uses a mock to replace Claude so the tests can be ran independently and it doesn't cost any extra.

# Setup Instructions:

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Create a .env file in the project root with your Anthropic API key:
   ANTHROPIC_API_KEY=sk-ant-your-key-here
4. Run the app:
   streamlit run app.py
5. To run the test suite (no API key needed):
   pytest tests/ -v

# Sample Interactions:

->
Question: What color is the sky on a sunny day?
User said: blue
Correct: True
Feedback: You're so smart for knowing that the sky is blue on a sunny day!

Question: What sound does a dog make?
User said: woof
Correct: True
Feedback: A woof is the same as a bark, so you're right�great job!

Question: How many sides does a triangle have?
User said: five
Correct: False
Feedback: A triangle has three sides, not five�maybe you were thinking of a different shape!

# Design Decisions:

-> Instead of directly asking Claude for the answer I implemented a RAG functionality, this gives control over the correct answer. It removes the final verdict from Claude and allows for the program to interpret answers from an assuming child, which requires a bit of leeway in grading. ChromaDB was chosen because it's an in-memory solution that is easy to use and same can be said for Streamlit. I decided to "fake" the API calls in testing so offline testing was available and I wouldn't have to pay for more API calls, honestly.

-> Some tradeoffs that were made is ChromaDB loses it's data on every restart instead of a non-volatile solution, the knowledge base I made for the RAG functionality remains static and never changes. For the testing, choosing a "mock-based" testing it doesn't test all the way through to Claude itself's grading accuracy, but again the alternative costed money.

# Testing Summary:

-> What worked:
-> All 22 current tests passed in the testing files.
-> The mock-based grader tests run quickly and correctly intercepts the anthropic call instead grade_answer() function.
-> ChromaDB retrieval tests confirmaed that category filtering works correctly.

-> What didn't work:
-> The original test file wasn't relevant to the new program and therefore was stale and had to be changed.
-> Claude occasionally grades ambiguous answers in unexpected ways, this behavior can't be caught by mock-based tests. An example of this I have is I intentionally answered "How many signs does a stop sign have?" with the answer "8". Claude responded with "An octagon has eight sides, and your word was almost right - just remember it's spelled "octagon" with an "a" at the end!", which is weird.

-> What I learned:
-> You can't unit test an LLM's intelligence, but you can test the code around it.
-> Tests expose assumptions, the old test files were written for the old program and the first thing I did was run these tests without updating them. Which obviously caused a problem that had to be fixed.

# Reflection:

-> The first thing that stood out to me directly is that RAG isn't as complicated as I thought it was in my head. Even after the RAG week of this class, it still was complicating to me but after implementing it in a simple way like this my understanding of RAG has increased quite a bit. Another thing is that AI is best used as a pipeline tool instead of the main aspect of a program. It's best used, or at least to my minimal understanding, as the current of a river and not the river itself to put it metaphorically. It's best to have human designed and implemented functionalities and use AI to tie it all together and move each piece of a program together as one.

All 22 tests passed however, the feedback that Claude will give when it receives a truly ambiguous answer can be a bit unpredictable. Such as the stop-sign question incident stated above. This exposes the mock-based testing if you don't want to spend extra money on API calls.

# Reflection & Ethics:

-> A limitation of this specific program is the knowledge base is static and written by one-person. This one person can have biases and the answers they wrote may differ from the answers of another developer. The static portion means that the knowledge base is limited in the questions it'll prompt the user with (8 questions per category only).

-> As a kindergarten trivia program I don't believe this program could be misused in an extreme manner as the program doesn't produce consequential decisions.

-> Reliability wise, it was interesting to see that even though Claude correctly identified "8" as a correct answer to "How many sides does a stop sign have?", it's feedback included a memory helper that would confuse a kindergarten level user. Reliabiltiy isn't just whether the AI gets the answer right, it's whether the output makes sense.

-> The back and forth with AI was pretty awesome for this project, I had the original idea to change the number guessing game into a trivia game and AI set forth the possible steps of progression. It was also cool to receive tips and tricks to setting this small program up in a cost-effective way, such as using the mock testing functionality instead of making API calls consistently for testing.

# Loom Video Walkthrough:
https://www.loom.com/share/9f0495d3d0f04c4f96a6932313b0cc75


# GitHub Link:
https://github.com/Cahilltr00/a110-applied-ai-system-project