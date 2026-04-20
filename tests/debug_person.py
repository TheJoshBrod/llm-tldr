import sys
import os
from pathlib import Path

try:
    from jaclang.jac0core.compiler import JacCompiler
    from jaclang.jac0core.program import JacProgram
    from jaclang.jac0core.unitree import Archetype, Ability, Test

    compiler = JacCompiler()
    program = JacProgram()
    file_path = Path(__file__).parent / "sample.jac"
    module = compiler.compile(str(file_path), program)

    for stmt in module.body:
        if isinstance(stmt, Test):
            print(f"Test node: {stmt}")
            print(f"Name: {stmt.name}")
            print(f"Description: {stmt.description}")
            print(f"Doc: {stmt.doc}")
            if stmt.doc:
                print(f"Doc value: {stmt.doc.value}")
except Exception as e:
    import traceback
    traceback.print_exc()
