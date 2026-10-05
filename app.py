import time
from collections import defaultdict, deque
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='Word Ladder Solver', page_icon='🔤', layout='wide')

DEFAULT_WORDS = '''hit
"hot", "dot", "dog", "lot", "log", "cog",
        "hit", "hog", "hop", "cop", "cot", "cat",
        "bat", "bot", "bog", "bag", "big", "dig",
        "fig", "fog", "fit", "fin", "fun", "bun",
        "but", "cut", "cup", "cop", "map", "mop"
'''.split()

@st.cache_data(show_spinner=False)
def build_index(words):
    word_set = {w.strip().lower() for w in words if w.strip().isalpha()}
    patterns = defaultdict(list)
    for word in word_set:
        for i in range(len(word)):
            patterns[word[:i] + '*' + word[i+1:]].append(word)
    return word_set, dict(patterns)


def bfs(start, target, words, patterns):
    start, target = start.lower().strip(), target.lower().strip()
    if not start.isalpha() or not target.isalpha():
        return [], 0, 'Words must contain letters only.'
    if len(start) != len(target):
        return [], 0, 'Start and target words must have the same length.'
    if start == target:
        return [start], 1, None
    if target not in words:
        return [], 0, 'Target word is not present in the dictionary.'

    queue = deque([start])
    parent = {start: None}
    visited = {start}
    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1
        if current == target:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], explored, None

        for i in range(len(current)):
            pattern = current[:i] + '*' + current[i+1:]
            for neighbor in patterns.get(pattern, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

    return [], explored, 'No valid transformation path exists.'


def load_uploaded_words(uploaded_file):
    if not uploaded_file:
        return DEFAULT_WORDS
    text = uploaded_file.getvalue().decode('utf-8', errors='ignore')
    return [line.strip() for line in text.splitlines() if line.strip()]

st.title('🔤 Word Ladder Solver')
st.caption('Find the shortest word transformation using Breadth-First Search (BFS).')

with st.sidebar:
    st.header('Dictionary')
    uploaded = st.file_uploader('Upload a .txt dictionary', type=['txt'])
    words_source = load_uploaded_words(uploaded)
    st.info(f'{len(words_source):,} words loaded')
    st.markdown('**Rule:** each move changes exactly one letter.')

col1, col2 = st.columns(2)
with col1:
    start = st.text_input('Starting word', 'hit', max_chars=30).lower()
with col2:
    target = st.text_input('Target word', 'cog', max_chars=30).lower()

solve = st.button('🚀 Find Shortest Ladder', type='primary', use_container_width=True)

if solve:
    words, patterns = build_index(words_source)
    if len(start) == len(target):
        filtered_words = {w for w in words if len(w) == len(start)}
        filtered_patterns = {k: v for k, v in patterns.items() if len(k) == len(start)}
        t0 = time.perf_counter()
        path, explored, error = bfs(start, target, filtered_words, filtered_patterns)
        elapsed = time.perf_counter() - t0
    else:
        path, explored, error = [], 0, 'Start and target words must have the same length.'
        elapsed = 0.0

    if error:
        st.error(error)
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric('Transformations', len(path) - 1)
        m2.metric('Words in path', len(path))
        m3.metric('States explored', explored)
        st.success(f'Found a shortest path in {elapsed:.6f} seconds.')

        st.subheader('Shortest transformation')
        st.write(' → '.join(f'**{w.upper()}**' for w in path))

        st.subheader('BFS Levels')
        for level, word in enumerate(path):
            st.write(f'**Level {level}:** `{word}`')

st.divider()
st.markdown('### How it works')
st.markdown('BFS explores the state space level-by-level. Each valid word is a node, and an edge connects two words that differ by one character. Because every transformation has equal cost, the first path reaching the target is shortest.')
