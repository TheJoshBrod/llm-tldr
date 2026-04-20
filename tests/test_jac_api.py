import sys
import os
from pathlib import Path

try:
    from jaclang.jac0core.compiler import JacCompiler
    from jaclang.jac0core.program import JacProgram
    from jaclang.jac0core.unitree import Archetype, Ability, ModuleItem, Import
    
    compiler = JacCompiler()
    program = JacProgram()
    
    file_path = Path(__file__).parent / "sample.jac"
    module = compiler.compile(str(file_path), program)
    
    print(f"Module Name: {module.name}")
    print(f"Module Doc: {module.doc} (type: {type(module.doc)})")
    if module.doc:
        print(f"Module Doc value: {module.doc.value}")
    
    # Analyze body
    for stmt in module.body:
        if isinstance(stmt, Archetype):
             print(f"  Archetype: {stmt.name.sym_name} ({stmt.arch_type.value})")
             print(f"    Has doc: {hasattr(stmt, 'doc')}")
             if hasattr(stmt, 'doc'):
                 print(f"    Doc type: {type(stmt.doc)}")
                 print(f"    Doc: {stmt.doc}")
                 if stmt.doc:
                     print(f"    Doc value: {getattr(stmt.doc, 'value', 'NO VALUE')}")
             for arch_stmt in stmt.body:
                 if isinstance(arch_stmt, Ability):
                     print(f"      Ability: {arch_stmt.name_ref.sym_name}")
                     if arch_stmt.signature:
                         sig = arch_stmt.signature
                         params = []
                         if hasattr(sig, 'params') and sig.params:
                             for p in sig.params:
                                 p_str = p.name.sym_name
                                 if hasattr(p, 'type_tag') and p.type_tag:
                                     p_str += f": {p.type_tag.tag.unparse()}"
                                 params.append(p_str)
                         print(f"        Params: {params}")
                         if hasattr(sig, 'return_type') and sig.return_type:
                             print(f"        Return: {sig.return_type.unparse()}")
        elif isinstance(stmt, Ability):
             print(f"  Ability: {stmt.name_ref.sym_name}")
        elif isinstance(stmt, Import):
             path = stmt.from_loc.dot_path_str if stmt.from_loc else ""
             items = [item.name.sym_name if hasattr(item.name, 'sym_name') else str(item.name) for item in stmt.items] if stmt.items else []
             print(f"  Import: from {path} import {items}")
except Exception as e:
    import traceback
    traceback.print_exc()
