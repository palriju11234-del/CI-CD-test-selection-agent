import math
import pytest
from src.complex_processor import ComplexProcessor

def test_math_operations():
    processor = ComplexProcessor([])
    
    # Test negative number
    assert processor._math_operations(-5) == 25
    
    # Test zero
    assert processor._math_operations(0) == 0
    
    # Test positive number
    expected = math.sqrt(16) * math.pi
    assert processor._math_operations(16) == expected

def test_string_operations():
    processor = ComplexProcessor([])
    
    # Test empty string
    assert processor._string_operations("") == ""
    
    # Test normal string
    result = processor._string_operations("hello")
    assert result.startswith("olleh-")
    assert len(result) == 6 + 10 # 5 for olleh, 1 for -, 10 for hash prefix

def test_process_data():
    data = [-2, 0, "test", None]
    processor = ComplexProcessor(data)
    
    results = processor.process_data()
    
    assert len(results) == 4
    assert results[0] == 4
    assert results[1] == 0
    assert results[2].startswith("tset-")
    assert results[3] is None

def test_aggregate_results():
    processor = ComplexProcessor([])
    
    # Test empty results
    assert processor.aggregate_results([]) == 0
    
    # Test mixed results
    results = [10.5, "string1", "string2", 5, None]
    # Sum of numbers: 15.5. Count of strings: 2. Total: 17.5
    assert processor.aggregate_results(results) == 17.5
