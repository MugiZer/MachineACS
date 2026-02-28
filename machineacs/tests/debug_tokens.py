from pathlib import Path
import tempfile
import json

class MockTmpPath(type(Path("."))):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

def test_json_structure_preservation_complex(tmp_path):
    print("DEBUG: Running modified test_json_structure_preservation_complex")
    from utils.json_structurer import stream_json_as_tokens
    
    json_path = tmp_path / "complex.json"
    data = {
        "a": [1, {"b": 2}, 3],
        "c": None,
        "d": False,
        "e": 1.23
    }
    json_path.write_text(json.dumps(data), encoding="utf-8")
    output = ""
    for token in stream_json_as_tokens(json_path):
        output += token.serialize(token.content)
    
    print(f"DEBUG: Output repr: {repr(output)}")
    print(f"DEBUG: Output ascii: {[ord(c) for c in output]}")
    
    try:
        json.loads(output)
        print("DEBUG: JSON IS VALID")
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON INVALID: {e}")
        # Print context around error
        pos = e.pos
        start = max(0, pos - 10)
        end = min(len(output), pos + 10)
        print(f"DEBUG Context: ...{output[start:pos]} |^| {output[pos:end]}...")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        try:
            test_json_structure_preservation_complex(tmp_path)
            print("PASS 2")
        except Exception as e:
            print(f"FAIL 2: {e}")
            import traceback
            traceback.print_exc()
