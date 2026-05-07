---
description: "Generate comprehensive pytest test cases for selected Python code. Creates unit tests, integration tests, and edge case coverage."
name: "Generate Unit Tests"
argument-hint: "Select Python code or function to test"
agent: "Test Case Generator"
---

# Generate Unit Test Cases

You are tasked with generating comprehensive pytest test cases for the following Python code.

## Selected Code to Test
```python
{selected_code}
```

## Test Generation Requirements

### 1. Unit Tests
- Test individual functions with various inputs
- Cover normal cases, boundary conditions, and edge cases
- Use parameterized tests for multiple input scenarios
- Include descriptive test names (test_<function>_<scenario>)

### 2. Integration Tests
- Test how functions interact together
- Verify data flows between components
- Test module-level functionality

### 3. Coverage Areas
- **Valid inputs**: Normal use cases
- **Boundary conditions**: Min/max values, empty inputs, None values
- **Invalid inputs**: Wrong types, out-of-range values
- **Error handling**: Exceptions, error messages
- **Edge cases**: Specific patterns or conditions

## Output Format

Generate a pytest-compatible test file with:
1. **Imports**: All necessary test dependencies
2. **Fixtures**: Reusable test setup if needed
3. **Test functions**: Clear naming convention
4. **Assertions**: Descriptive messages explaining what's being tested
5. **Docstrings**: Explain what each test validates
6. **Parametrization**: Use @pytest.mark.parametrize for multiple scenarios
7. **Coverage**: Aim for 80%+ code coverage

## Example Test Structure

```python
import pytest
from module import function_to_test

class TestFunctionToTest:
    """Test cases for function_to_test()"""
    
    def test_valid_input(self):
        """Test with valid input returns expected result"""
        result = function_to_test("valid")
        assert result == expected_value
    
    @pytest.mark.parametrize("input_val,expected", [
        ("case1", "result1"),
        ("case2", "result2"),
        ("edge", "edge_result"),
    ])
    def test_multiple_scenarios(self, input_val, expected):
        """Test multiple input scenarios"""
        assert function_to_test(input_val) == expected
    
    def test_error_handling(self):
        """Test error handling for invalid input"""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

## Quality Checklist

- ✓ All tests are independent and can run in any order
- ✓ Tests have clear, descriptive names
- ✓ Each test has a docstring explaining its purpose
- ✓ Use fixtures for common setup/teardown
- ✓ Parameterized tests for multiple input combinations
- ✓ Assertion messages are descriptive
- ✓ Tests validate behavior, not implementation
- ✓ Edge cases and error conditions covered
- ✓ No code duplication in tests
- ✓ All tests pass when run with: `pytest test_<module>.py -v`

## Deliverable

Generate a complete, runnable pytest test file that:
1. Tests the provided code thoroughly
2. Includes all necessary imports and fixtures
3. Provides clear documentation for each test
4. Can be run immediately with: `pytest filename.py -v`
5. Reports comprehensive coverage of the code

**Execute the tests and confirm they all pass before returning.**
