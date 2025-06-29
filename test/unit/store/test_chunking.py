import types
from src.core.knowledge import store

class DummySentence:
    def __init__(self, text, has_vector=True, sim=1.0):
        self.text = text
        self.has_vector = has_vector
        self._sim = sim
    def similarity(self, other):
        return self._sim
    def __str__(self):
        return self.text

class DummyDoc:
    def __init__(self, sents):
        self.sents = sents

def dummy_nlp(text):
    sents = [DummySentence(t) for t in text.split('.') if t]
    return DummyDoc(sents)

def test_chunk_str_long(monkeypatch):
    monkeypatch.setattr(store, 'nlp', dummy_nlp)
    text = "Sentence one is quite long and interesting." * 5
    chunks = store.chunk_str(text)
    assert len(chunks) == 1
    assert text.replace('.', '').strip()[:20] in chunks[0]


def test_chunk_str_short(monkeypatch):
    monkeypatch.setattr(store, 'nlp', dummy_nlp)
    text = "short text"
    assert store.chunk_str(text) == []
