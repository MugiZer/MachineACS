from cleaner import clean_line
from utils.json_structurer import Line

# Mocking the generator locally to avoid command line input dependency
def mock_generator_txt(file_path):
    yield from [
        (Line("Hello   world..."), str(file_path), file_path, "txt")
    ]

def test_clean_line_integration(sample_config, sample_file, temp_workspace):
    """
    Tests the clean_line function with a controlled input generator.
    """
    # Create a mock generator that yields the sample file
    # We use a simple list of tokens similar to what adapters yield
    
    # We need to construct tokens that match what clean_line expects
    # clean_line expects: iterator of (token, file_name, file_path, kind)
    # Actually, clean_line expects (gen, file_name, file_path, kind) in generators argument
    # based on: for gen, file_name, file_path, kind in generators:
    
    # So we need to structure our input to clean_line correctly.
    
    # Mock Token that supports .process(config)
    class MockToken:
        def __init__(self, content):
            self.content = content
            
        def process(self, config):
            # We can rely on json_structurer's Token or just simple string processing
            # ensuring we test the pipeline logic
            from config.registry import apply_filters
            return apply_filters(self.content, config)

    # We need to create a generator that yields the tokens
    def token_gen():
        yield MockToken("Hello   world...")

    # The input to clean_line is ONE generator that yields (token_gen, ...)
    input_generators = [
        (token_gen(), "test_file.txt", sample_file, "txt")
    ]
    
    # Run the pipeline
    results = list(clean_line(input_generators, sample_config))
    
    # Assert
    assert len(results) == 1
    output, new_file, new_file_path, kind = results[0]
    
    assert new_file == "cleaned_test_file.txt"
    assert kind == "txt"
    # Note: MockToken doesn't add newline, but Line does.
    # Our test uses MockToken.
    expected = "Hello world."
    assert output == expected, f"Expected '{expected}', got '{output}'"

def test_registry_integration(sample_config):
    """
    Tests that apply_filters works as expected with the registry.
    This effectively tests the integration of config + registry + filters.
    """
    from config.registry import apply_filters
    
    input_line = "Hello...   world!"
    output = apply_filters(input_line, sample_config)
    
    expected = "Hello. world!"
    assert expected in output, f"Expected '{expected}' to be in '{output}'"
