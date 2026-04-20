import pytest
from pathlib import Path
from tldr.ast_extractor import extract_jac
from tldr.hybrid_extractor import HybridExtractor

JAC_SAMPLE = """
import from os { path }

\"\"\"Calculate something.\"\"\"
def add(a: int, b: int) -> int {
    return a + b;
}

test "math_test" {
    \"\"\"Test addition.\"\"\"
    if add(1, 2) != 3 {
        print("Test failed!");
    }
}

\"\"\"A person archetype.\"\"\"
obj Person {
    has name: str;
    has age: int;

    \"\"\"Greet the world.\"\"\"
    can greet(prefix: str = "Hello") -> str {
        res = f"{prefix}, my name is {self.name} and I am {self.age} years old.";
        print(res);
        return res;
    }
}

walker say_hello {
    can visit Person {
        here.greet();
    }
}
"""

def test_jac_extraction_basic(tmp_path):
    """Test basic extraction of archetypes and abilities from Jac."""
    jac_file = tmp_path / "sample.jac"
    jac_file.write_text(JAC_SAMPLE)
        
    result = extract_jac(jac_file)
    
    assert result.language == "jac"
    
    # Check for Person archetype (ClassInfo)
    person = next((c for c in result.classes if c.name == "Person"), None)
    assert person is not None
    assert "person archetype" in person.docstring.lower()
    
    # Check for methods (Ability)
    greet = next((f for f in person.methods if f.name == "greet"), None)
    assert greet is not None
    assert "prefix" in greet.params
    
    # Check for top-level functions (Ability)
    add_func = next((f for f in result.functions if f.name == "add"), None)
    assert add_func is not None
    
    # Check for tests
    math_test = next((f for f in result.functions if f.name == "test_math_test"), None)
    assert math_test is not None
    assert "test addition" in math_test.docstring.lower()

def test_jac_hybrid_integration(tmp_path):
    """Test that HybridExtractor correctly routes .jac files."""
    jac_file = tmp_path / "test.jac"
    jac_file.write_text("obj Foo { can bar { } }")
    
    extractor = HybridExtractor()
    result = extractor.extract(jac_file)
    
    assert result.language == "jac"
    assert any(c.name == "Foo" for c in result.classes)

def test_jac_import_extraction(tmp_path):
    """Test extraction of imports in Jac."""
    jac_file = tmp_path / "imports.jac"
    jac_file.write_text("import:py sys; import:jac from other_mod, item1, item2;")
    
    result = extract_jac(jac_file)
    
    assert len(result.imports) >= 2
    modules = [imp.module for imp in result.imports]
    assert "sys" in modules
    assert "other_mod" in modules
