# 🔤 Word Ladder Solver Using Breadth-First Search

An interactive Streamlit application that finds the shortest transformation sequence between two words using **Breadth-First Search (BFS)**.

## Demo

Deploy this repository on Streamlit Community Cloud and share the generated URL.

## Features

- Shortest-path Word Ladder using BFS
- Fast wildcard-pattern indexing for neighbor lookup
- Input validation
- Number of transformations and states explored
- Execution-time measurement
- Upload your own `.txt` dictionary
- Clean Streamlit interface

## Example

`HIT → HOT → DOT → DOG → COG`

Each step changes exactly one letter and every intermediate word must be in the dictionary.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Select **Create app**.
4. Choose your GitHub repository and branch.
5. Set the main file to `app.py`.
6. Deploy.

No secrets or API keys are required.

## Project Structure

```text
word-ladder-solver/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── tests/
    └── test_solver.py
```

## Algorithm

BFS uses a FIFO queue. The solver stores parent relationships so the shortest path can be reconstructed after the target is reached. A wildcard index such as `*ot` allows fast discovery of words that differ at one position.

### Complexity

Let `N` be the number of dictionary words and `L` the word length. Building the index is approximately `O(NL)`. BFS then performs near-constant-time hash lookups for indexed patterns, with overall work depending on the number of reachable words and their pattern buckets.

## License

MIT License.
