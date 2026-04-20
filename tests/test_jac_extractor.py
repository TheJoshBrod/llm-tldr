import pytest
from pathlib import Path
from tldr.ast_extractor import extract_jac
from tldr.hybrid_extractor import HybridExtractor

# A more complex sample covering inheritance, multiple archetypes, and complex signatures
THOROUGH_JAC_SAMPLE = """
\"\"\"Root module docstring.\"\"\"

import:py os;
import:jac from base_mod, BaseArch;

# Inheritance test
obj ExtendedArch(BaseArch) {
    has extra_field: str = "default";

    \"\"\"An ability with complex signature.\"\"\"
    can complex_ability(a: int, b: list[int] = [], c: dict = {}) -> bool {
        return True;
    }
}

# Node and Walker tests
node UserNode {
    has username: str;
}

walker SyncWalker {
    has total: int = 0;
    
    can visit UserNode {
        self.total += 1;
    }
}

# Top level ability
def global_helper(x: float) {
    print(x);
}
"""

def test_jac_extraction_thorough(tmp_path):
    jac_file = tmp_path / "thorough.jac"
    jac_file.write_text(THOROUGH_JAC_SAMPLE)
    result = extract_jac(jac_file)
    
    # 1. Module Docstring
    assert result.docstring == "Root module docstring."

    # 2. Inheritance
    extended = next((c for c in result.classes if c.name == "ExtendedArch"), None)
    assert extended is not None
    assert any("BaseArch" in b for b in extended.bases) # Bases might be unparsed strings
    assert "arch:obj" in extended.decorators

    # 3. Complex Signatures & Types
    complex_method = next((m for m in extended.methods if m.name == "complex_ability"), None)
    assert complex_method is not None
    # Note: Param extraction might vary by jaclang version (sometimes includes type, sometimes not)
    # But it should at least pick up the name
    assert any("a" in p for p in complex_method.params)
    assert complex_method.return_type == "bool"

    # 4. Different Archetypes (node, walker)
    user_node = next((c for c in result.classes if c.name == "UserNode"), None)
    assert user_node is not None
    assert "arch:node" in user_node.decorators

    sync_walker = next((c for c in result.classes if c.name == "SyncWalker"), None)
    assert sync_walker is not None
    assert "arch:walker" in sync_walker.decorators
    
    # 5. Top-level functions
    helper = next((f for f in result.functions if f.name == "global_helper"), None)
    assert helper is not None
    assert any("x" in p for p in helper.params)

def test_jac_extraction_empty_file(tmp_path):
    """Ensure it handles empty or whitespace-only files gracefully."""
    empty_file = tmp_path / "empty.jac"
    empty_file.write_text("   \n   ")
    result = extract_jac(empty_file)
    assert result.language == "jac"
    assert len(result.classes) == 0

def test_jac_error_resilience(tmp_path):
    """Ensure it doesn't crash on invalid syntax."""
    bad_file = tmp_path / "bad.jac"
    bad_file.write_text("this is not { valid jac } syntax !!!")
    # Should catch exception internally and return empty ModuleInfo
    result = extract_jac(bad_file)
    assert result.language == "jac"

def test_jac_hybrid_integration(tmp_path):
    """Test that HybridExtractor correctly routes .jac files."""
    jac_file = tmp_path / "test.jac"
    jac_file.write_text("obj Foo { can bar { } }")
    
    extractor = HybridExtractor()
    result = extractor.extract(jac_file)
    
    assert result.language == "jac"
    assert any(c.name == "Foo" for c in result.classes)
