# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The game looks bland but functional, looks like an internet page from 2005. The icons don't really make much sense like a rocket for submit guess. If you use the developer debug info to input the correct number the balloons celebration is nice though

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  Bug #1: I guess 48, told me to go lower so I guessed 24, higher, I guessed 31, it said lower, 29 -> higher, 30 -> wrong! The secret was 5

  Bug #2: It lets you put in any number, even out of bounds numbers such as 4340404 and -99

  Bug #3: When you hit new game it doesn't start a new game until you refresh page (this was incorrect but rest of bug is), also the attempts left go from 7 to 8.

  Bug #4: The difficulty level hard is less than the difficulty level for normal, 1-100 for normal, 1-50 for hard.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  For bug #2 Claude suggested that the problem was occurring in the parse_guess function, which was correct. Allowed Claude to make the changes and then after saving the file I ran the program and the problem was fixed.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  Bug #3 was tricky for me to solve, it involved both me being incorrect about the refreshing of the page and this led to a snowball effect that allowed for Claude to suggest a wrong fix. In the end it somehow was fixed but I can't explain to you exactly how that happened. This was a real eye-opener on using AI as a SWE.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I decided to trust the fact that the program would run how I thought it should after the bug was fixed. After fixes were implemented I ran the program again and see if the change worked or not.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  When I first ran the pytest I had three failures, for test_winning_guess, test_guess_too_high and test_guess_too_low. These failures actually showed me a new bug that I didn't catch because I was so focused on the others. I have noticed it before, I wrote about it in here previously but the tests reminded me and led me back to fixing it.

- Did AI help you design or understand any tests? How?

  When I first ran pytest it wouldn't run because lgoic_utils.py wasn't available to the test_game_logic.py, Claude implemented a solution so that utils was accessible to testing. It is the conftest.py page, I haven't looked further into it because everything just worked but I'll look over why that happened and learn about it because of this session with AI.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app. 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
