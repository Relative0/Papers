"""Exploratory matched instrumentation ablation; preserves supplied source files.

No timing is performed here. The root auditor may time returned clean_base.lower_anf
and clean_p6.lower_p6 on exactly the same sources as their original counterparts.
The transformation removes only ANF statistics, disabled selector instrumentation,
and the unconditional output_unique_nodes traversal used only for reporting.
Stats containers/return shapes remain for API compatibility and are not meaningful.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import inspect
import json
import random
import sys
import textwrap
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / "primary" / "ASTRA_P1_P13_AUDIT_PACKAGE"


def load_harnesses():
    for path in [PACKAGE / "03_N1_BASELINE"] + [
        PACKAGE / "04_EXPERIMENTS" / f"P{i:02d}" for i in range(1, 14)
    ] + [PACKAGE / "04_EXPERIMENTS" / "P07B"]:
        sys.path.insert(0, str(path))
    import n2_p6_harness as p6
    return p6.base, p6.p3, p6


class RemoveInstrumentation(ast.NodeTransformer):
    def __init__(self):
        self.removed = []

    @staticmethod
    def statistic_target(target):
        return (isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id in {"st", "ast"})

    def visit_Assign(self, node):
        if any(self.statistic_target(t) for t in node.targets):
            self.removed.append(ast.unparse(node))
            return None
        return self.generic_visit(node)

    def visit_AugAssign(self, node):
        if self.statistic_target(node.target):
            self.removed.append(ast.unparse(node))
            return None
        return self.generic_visit(node)

    def visit_Expr(self, node):
        call = node.value
        if isinstance(call, ast.Call):
            func = call.func
            is_peak = ((isinstance(func, ast.Name) and func.id == "update_peak")
                       or (isinstance(func, ast.Attribute) and func.attr == "update_peak"))
            if is_peak:
                self.removed.append(ast.unparse(node))
                return None
        return self.generic_visit(node)

    def visit_If(self, node):
        # The intended measured P6 arm always uses collect_stats=False.
        if isinstance(node.test, ast.Name) and node.test.id == "collect_stats":
            self.removed.append("if collect_stats: " + ast.unparse(node))
            return [self.visit(stmt) for stmt in node.orelse]
        node = self.generic_visit(node)
        if not node.body:
            node.body = [ast.Pass()]
        return node

    def visit_keyword(self, node):
        if node.arg == "output_unique_nodes":
            self.removed.append(ast.unparse(node.value))
            node.value = ast.Constant(0)
        return self.generic_visit(node)


def transform(function, namespace):
    original = textwrap.dedent(inspect.getsource(function))
    tree = ast.parse(original)
    cleaner = RemoveInstrumentation()
    tree = cleaner.visit(tree)
    ast.fix_missing_locations(tree)
    cleaned = ast.unparse(tree) + "\n"
    exec(compile(tree, f"<stats-free:{function.__name__}>", "exec"), namespace)
    return namespace[function.__name__], original, cleaned, cleaner.removed


def make_backend(base, p3, p6, artifact_dir=None):
    """Return namespace copies without mutating any imported original module."""
    clean_base = types.SimpleNamespace(**vars(base))
    clean_p3 = types.SimpleNamespace(**vars(p3))
    clean_p6 = types.SimpleNamespace(**vars(p6))
    base_globals = dict(vars(base))
    p3_globals = {**vars(p3), "base": clean_base}
    p6_globals = {**vars(p6), "base": clean_base, "p3": clean_p3}
    artifacts = []
    for owner, name, globals_dict in [
        (clean_base, "mul_poly", base_globals),
        (clean_base, "lower_anf", base_globals),
        (clean_p3, "apply_tf_poly", p3_globals),
        (clean_p6, "lower_p6", p6_globals),
    ]:
        fn, original, cleaned, removed = transform(getattr(owner, name), globals_dict)
        setattr(owner, name, fn)
        artifacts.append((name, original, cleaned, removed))
    if artifact_dir is not None:
        out = Path(artifact_dir)
        out.mkdir(parents=True, exist_ok=True)
        manifest = {}
        for name, original, cleaned, removed in artifacts:
            (out / f"{name}.py").write_text(cleaned, encoding="utf-8")
            (out / f"{name}.diff").write_text("".join(difflib.unified_diff(
                original.splitlines(True), cleaned.splitlines(True),
                fromfile=f"original/{name}.py", tofile=f"stats_free/{name}.py")), encoding="utf-8")
            manifest[name] = {"original_sha256": hashlib.sha256(original.encode()).hexdigest(),
                              "cleaned_sha256": hashlib.sha256(cleaned.encode()).hexdigest(),
                              "removed": removed}
        (out / "transformation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return clean_base, clean_p3, clean_p6


def verify():
    base, p3, p6 = load_harnesses()
    cb, cp3, cp6 = make_backend(base, p3, p6, HERE / "stats_free_generated")
    seed = 20260918 ^ 0x57A7
    rng = random.Random(seed)
    cases = []
    for i in range(80):
        nvars = rng.randrange(2, 7)
        f = base.Factory()
        root = base.random_expr(rng, nvars, rng.randrange(2, 7), f)
        cases.append((f"random:{i}", root, nvars))
    for depth in (2, 4, 6, 8):
        for i in range(3):
            _, root, nvars = base.gatep_case(rng, depth, i)
            cases.append((f"gatep_exploratory:{depth}:{i}", root, nvars))
    failures = []
    for cid, root, nvars in cases:
        rr, inf = p6.build_innode(root)
        expected, _ = base.lower_anf(root)
        direct, _ = cb.lower_anf(root)
        original_folded, _, _ = p6.lower_p6(rr, inf, collect_stats=False)
        cleaned_folded, _, _ = cp6.lower_p6(rr, inf, collect_stats=False)
        truth = base.eval_node_bitset(root, nvars)
        if not (expected == direct == original_folded == cleaned_folded):
            failures.append({"case": cid, "kind": "polynomial equality"})
        if base.anf_to_bitset(cleaned_folded, nvars) != truth:
            failures.append({"case": cid, "kind": "truth equality"})
    result = {"label": "exploratory correctness diagnostic, no timing", "seed": seed,
              "cases": len(cases), "failures": failures,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "All original algebra and selector conditions retained; ANF counters/peak scans and disabled selector reporting removed."}
    (HERE / "stats_free_verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    verify()
