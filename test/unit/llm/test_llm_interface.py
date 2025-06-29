import types
from src.core.llm import LLM
from src.core.memory.schema import Conversation, Message, Role

class DummyClient:
    def __init__(self, host=None):
        pass
    def chat(self, model, messages, stream=True, options=None):
        def gen():
            yield {"message": {"content": "reply"}}
            yield {"prompt_eval_count": 11, "eval_count": 5}
        return gen()

def test_llm_query(monkeypatch):
    monkeypatch.setattr("src.core.llm.ollama.Client", DummyClient)
    llm = LLM(model="mistral", inference_endpoint="http://dummy")
    conv = Conversation(name="c", messages=[
        Message(role=Role.SYS, content="abcd"),
        Message(role=Role.USER, content="hi")
    ])
    chunks = list(llm.query(conv))
    assert chunks[0][0] == "reply"
    assert chunks[1][2] == 5
