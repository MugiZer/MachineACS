from adapters.format import CSVYielder, TXTYielder, JSONYielder, JSONLYielder
from utils.json_structurer import StructuralToken, KeyToken, StringValueToken
import json

def test_txt_yielder(temp_workspace):
    file_path = temp_workspace / "test.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Line 1\nLine 2\n")
        
    gen = TXTYielder.yield_gen(file_path)
    lines = list(gen)
    assert len(lines) == 2
    assert lines[0].content == "Line 1"
    assert lines[1].content == "Line 2"

def test_csv_yielder(temp_workspace):
    file_path = temp_workspace / "test.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("col1,col2\nval1,val2\n")
        
    gen = CSVYielder.yield_gen(file_path)
    lines = list(gen)
    assert len(lines) == 2
    assert lines[0].content == "col1,col2"

def test_json_streaming(temp_workspace):
    file_path = temp_workspace / "test.json"
    data = {"key": "value", "list": [1, 2]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
        
    gen = JSONYielder.yield_gen(file_path)
    tokens = list(gen)
    
    # Verify stream structure
    # {
    assert isinstance(tokens[0], StructuralToken) and tokens[0].content == "{"
    # "key"
    assert isinstance(tokens[1], KeyToken) and tokens[1].content == "key"
    # "value"
    assert isinstance(tokens[2], StringValueToken) and tokens[2].content == "value"
    # ,
    assert isinstance(tokens[3], StructuralToken) and tokens[3].content == ","
    # "list"
    assert isinstance(tokens[4], KeyToken) and tokens[4].content == "list"
    # [
    assert isinstance(tokens[5], StructuralToken) and tokens[5].content == "["
    # 1 ...
    
    # Just basic check that it tokenizes
    assert any(t.content == "key" for t in tokens)
    assert any(t.content == "value" for t in tokens)

def test_jsonl_streaming(temp_workspace):
    file_path = temp_workspace / "test.jsonl"
    data = [{"a": 1}, {"b": 2}]
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
            
    gen = JSONLYielder.yield_gen(file_path)
    tokens = list(gen)
    
    # Check if we have tokens for both objects
    # Each object: { "a" : 1 } \n
    assert any(isinstance(t, KeyToken) and t.content == "a" for t in tokens)
    assert any(isinstance(t, KeyToken) and t.content == "b" for t in tokens)

def test_token_serialization(sample_config):
    t = StringValueToken("clean me")
    # Config is passed but StringValueToken cleans using filters?
    # Let's check StringValueToken.clean implementation in json_structurer.py
    # Defaults to Token.clean which calls apply_filters
    
    # If we have a filter that changes "clean me", verify it works.
    # regex filter removes spaces if configured? No.
    # Let's assume standard filters.
    
    output = t.process(sample_config)
    # Output should be json dumped string
    assert output == '"clean me"'

