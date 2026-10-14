# CM Next Experiments - Structural Geometry, Retrieval, and Native CM Capabilities

**Purpose:** This file proposes deeper experiments that may demonstrate CM capabilities beyond raw Boolean evaluation speed. The goal is to identify valuable computations that Bitset and CUDD/ROBDD do not naturally provide, or can only infer indirectly with extra machinery.

---

## 1. Why a New Direction Is Needed

Experiments A, B, and C have clarified the computational landscape.

### What is already clear

- **Bitset** is extremely fast for flat truth-table evaluation and semantic truth-output deltas.
- **CUDD** is extremely fast for canonical semantic Boolean reasoning, especially equivalence and symbolic XOR delta.
- **CM** does not currently beat these on their strongest tasks.

### The opportunity

CMs become interesting when the task is not:

> "Evaluate this Boolean function as fast as possible."

but rather:

> "Analyze the operator/basis structure of this Boolean logic."

That includes:

- quotienting
- containment
- structural feature difference
- transformation
- decomposition
- similarity
- retrieval
- clustering
- structural drift
- interpretable change reports

---

## 2. Core New Hypothesis

> **CMs may provide a structural coordinate system for Boolean logic.**

Instead of representing a Boolean expression only as:

```text
assignment -> output
```

or as:

```text
canonical decision graph
```

CMs may represent it in terms of:

```text
operator/basis features
structural coefficients
quotient features
containment relations
transformational relationships
```

This could allow computations such as:

- distance
- similarity
- projection
- clustering
- nearest-neighbor retrieval
- drift over time
- decomposition into structural components

These are not natural first-class outputs of Bitset or CUDD.

---

## 3. Experiment D - Structural Basis Coefficients

### 3.1 Goal

Build feature vectors from CM-derived structural artifacts and test whether they capture meaningful relationships between expressions.

### 3.2 Candidate Feature Vector

For each expression, compute a vector containing:

- counts of 2x2 operator types:
  - AND
  - OR
  - XOR
  - EQV
  - IMP
  - RIMP
  - NAND
  - NOR
  - etc.
- quotient feature counts against family prototypes
- containment counts
- transformation orbit counts
- structural hash subtree counts
- live variable counts
- CM density
- basis feature density
- operator entropy
- depth
- DAG node counts
- repeated subtree counts
- Jaccard similarities to reference expressions

Possible vector:

```text
[
  count_AND,
  count_OR,
  count_XOR,
  count_IMP,
  count_EQV,
  count_NAND,
  count_NOR,
  quotient_to_parent_features,
  quotient_from_parent_features,
  containment_score,
  jaccard_to_parent,
  operator_entropy,
  structural_hash_reuse_ratio,
  cm_density,
  live_var_count,
  expression_depth
]
```

### 3.3 Baselines

Compare CM-derived feature vectors against:

1. **Bitset features**
   - truth-table density
   - Hamming distance
   - output entropy
   - semantic XOR distance

2. **ROBDD/CUDD features**
   - node count
   - path count if available
   - variable support
   - BDD depth
   - semantic equivalence
   - BDD size after reorder

3. **AST features**
   - edit distance
   - operator counts
   - tree depth
   - subtree hashes

### 3.4 Metrics

Use:

- nearest-neighbor accuracy
- cluster purity
- adjusted Rand index
- normalized mutual information
- silhouette score
- retrieval recall@k
- correlation with known mutation distance
- runtime per representation

### 3.5 Why This Could Matter

If CM features recover expression family identity better than Bitset or CUDD metadata, then CMs are demonstrating a useful representation-level capability.

---

## 4. Experiment E - Structural Retrieval

### 4.1 Goal

Given a large library of Boolean expressions, retrieve the most structurally similar expressions to a query.

### 4.2 Dataset

Generate:

- 100 base expressions
- 50 variants per base
- total = 5,000 expressions

Variants:

- subtree mutation
- operator substitution
- operand negation
- operand swap
- implication rewrite
- DeMorgan rewrite
- equivalent rewrite
- near-miss semantic mutation
- shared-block insertion/removal

Each expression has a ground-truth family ID.

### 4.3 Task

For each query expression, retrieve top-k nearest expressions.

Compare representations:

| Representation | Distance |
|---|---|
| Bitset | Hamming distance / normalized semantic XOR |
| CUDD | node-count features, graph metadata, semantic equivalence buckets |
| AST | tree edit distance, subtree hash Jaccard |
| CM | quotient/Jaccard/operator-basis feature distance |

### 4.4 Metrics

- Recall@1
- Recall@5
- Recall@10
- mean reciprocal rank
- cluster purity among retrieved neighbors
- runtime per query
- index build time
- memory footprint

### 4.5 Expected Value

Bitset may retrieve semantically similar expressions, but semantically close expressions are not necessarily structurally close.

CUDD may collapse equivalent expressions but may not preserve design lineage.

CM may recover structural family relationships even when semantic output changes.

### 4.6 Example Output

```text
Query: expression_317

Top CM neighbors:
1. expression_314 - same family, Jaccard 0.94
2. expression_322 - same family, Jaccard 0.91
3. expression_299 - same family, Jaccard 0.89

Top Bitset neighbors:
1. expression_112 - different family, Hamming distance 0.02
2. expression_876 - different family, Hamming distance 0.03
```

This would show CM captures a different notion of similarity.

---

## 5. Experiment F - Structural Drift Across Revisions

### 5.1 Goal

Simulate or ingest revision histories and measure how Boolean logic changes over time.

### 5.2 Dataset

Generate revision chains:

```text
program_001_v001
program_001_v002
...
program_001_v100
```

Mutation types:

- small operator replacement
- local subtree insertion
- local subtree deletion
- equivalent rewrite
- safety condition added
- emergency override added
- mode logic refactored
- semantic no-op refactor
- large structural rewrite

### 5.3 CM Change Report

For each adjacent revision:

```text
A -> B

A \ B features removed
B \ A features added
overlap
Jaccard
containment
operator entropy change
dominant operator changes
transformation matches
semantic delta
```

Example:

```text
Revision 42 -> 43

Semantic change:
  2.1% of assignments differ

Structural change:
  Jaccard: 0.87
  Added features: 38
  Removed features: 12
  AND +14
  IMP +8
  XOR unchanged
  containment: false
  closest known pattern: safety interlock insertion
```

### 5.4 Baselines

- Bitset semantic delta: `number of assignments changed`
- CUDD equivalence / delta BDD: `semantic function changed / delta node count`
- CM: `what structural features changed`

### 5.5 Metrics

- correlation with known mutation severity
- classification accuracy for mutation type
- interpretability score
- anomaly detection accuracy
- drift trajectory smoothness

### 5.6 Potential Application

Industrial control logic, PLC revisions, FPGA rule sets, safety interlock changes, product configuration systems.

---

## 6. Experiment G - Operator Entropy and Complexity

### 6.1 Goal

Measure operator diversity and structural complexity using CM-derived features.

### 6.2 Metrics

For each expression:

- operator distribution
- Shannon entropy of operator features
- basis sparsity
- CM density
- quotient sparsity
- transformation orbit size
- containment depth
- decomposition count

### 6.3 Questions

- Do high-entropy expressions correlate with harder evaluation?
- Do certain operator distributions produce large ROBDDs?
- Can CM entropy predict CUDD node explosion?
- Can CM features predict whether Bitset, CUDD, or CM will be the best backend?

### 6.4 Useful Output

A meta-compiler heuristic:

```text
If CM entropy low and structure reused:
  use CM cache/no-reinflate

If ROBDD node count small:
  use CUDD

If flat output needed and n <= threshold:
  use Bitset

If quotient/containment needed:
  use CM
```

---

## 7. Experiment H - CM Decomposition Search

### 7.1 Goal

Use CM operator algebra to discover decompositions of target operators or expressions.

### 7.2 2x2 Decomposition

For every target operator `T`, find all triples:

```text
A Phi B = T
```

where:

- `A` and `B` are among the 16 operators
- `Phi` is among the 16 operators

Examples:

```text
OR = AND XOR XOR
XOR = OR \ AND
NAND = TRUE \ AND
```

### 7.3 Metrics

- number of decompositions per operator
- minimal decomposition size
- operator containment lattice
- decomposition graph connectivity
- unique vs ambiguous decompositions

### 7.4 Why Valuable

This gives a searchable operator algebra.

CUDD can simplify Boolean functions, but it does not naturally report:

```text
Here are all operator-basis decompositions of OR under CM algebra.
```

### 7.5 Slide Artifact

Create a graph:

```text
16 operators as nodes
edges = quotient / containment / transform / decomposition relation
```

This could be visually compelling and mathematically distinctive.

---

## 8. Experiment I - Containment Lattice

### 8.1 Goal

Build the partial order of 2x2 operators under CM feature containment.

Definition:

```text
A contains B iff B \ A = FALSE
```

### 8.2 Expected Relations

- FALSE is contained in everything.
- TRUE contains everything.
- AND is contained in OR.
- AND is contained in TRUE.
- XOR not contained in AND.
- Many pairs are incomparable.

### 8.3 Output

Generate:

- containment adjacency matrix
- Hasse diagram
- lattice levels by feature count
- transitive reduction

### 8.4 Metrics

- number of containment edges
- number of incomparable pairs
- average quotient size
- maximal chains
- minimal generators

### 8.5 Why Valuable

This is a clear, finite demonstration that CMs expose an operator-feature geometry.

---

## 9. Experiment J - Transformation Orbits

### 9.1 Goal

Analyze the group-like action of CM transformations on the 16 operators.

Transformations:

- transpose
- complement
- rotate90
- rotate180
- rotate270
- negate left
- negate right
- negate both

### 9.2 Questions

- Which operators are invariant under transpose?
- Which operators form transformation orbits?
- What is the orbit size of each operator?
- Are some operators central/symmetric?
- Can transformations classify operators?

### 9.3 Example

Known examples:

- `AND.T = AND`
- `OR.T = OR`
- `XOR.T = XOR`
- `EQV.T = EQV`
- `IMP.T = RIMP`
- `~AND = NAND`
- `~XOR = EQV`

### 9.4 Outputs

- orbit table
- transformation graph
- invariant operator list
- orbit-size histogram

### 9.5 Why Valuable

This demonstrates matrix-native transformations as a real algebra, not just implementation tricks.

---

## 10. Experiment K - Explainable Change Reports

### 10.1 Goal

Turn CM quotient and structural features into human-readable explanations.

### 10.2 Input

Two expressions:

```text
A
B
```

### 10.3 Output

Report:

```text
Semantic summary:
- equivalent: false
- truth assignments changed: 143 / 4096
- delta density: 0.0349

CM structural summary:
- A \ B features: 657
- B \ A features: 419
- overlap features: 1824
- Jaccard: 0.6467
- A contains B: false
- B contains A: false

Operator changes:
- AND-like features increased
- implication-like features removed
- XOR-like features stable

Transformations detected:
- operand swap detected in sub-block 3
- output complement detected in sub-block 5

Nearest historical design:
- revision 42
- similarity 0.96
```

### 10.4 Baseline Comparison

Compare with:

- Bitset report: `143 assignments differ`
- CUDD report: `semantic equivalent: false; delta BDD nodes: 28`

CM may provide a more actionable answer to "what changed?"

---

## 11. Experiment L - Backend Selection Heuristic

### 11.1 Goal

Use CM-derived structural metrics to predict the best backend.

Possible backends:

- Bitset
- CUDD
- CM no-reinflate
- CM cached
- SymPy
- Espresso if available

### 11.2 Features

- n variables
- expression depth
- operator entropy
- subtree reuse ratio
- live-variable count
- CM density
- quotient sparsity
- CUDD node count after small probe
- bitset output density
- partial-context count

### 11.3 Target

Predict:

- fastest backend
- lowest memory backend
- best explanation backend

### 11.4 Why Valuable

This converts the whole research project into a practical hybrid compiler/router.

---

## 12. Recommended Immediate Next Experiment

The best next experiment is:

> **Experiment D: Structural Geometry and Retrieval**

### Why

It directly tests whether CMs provide a capability that Bitset and CUDD do not naturally provide.

### Minimal version

Generate:

- 20 base expressions
- 50 variants each
- total 1,000 expressions

Compute:

- CM feature vectors
- Bitset semantic vectors or compressed features
- CUDD metadata features
- AST feature vectors

Task:

- retrieve same-family neighbors

Metrics:

- Recall@1
- Recall@5
- MRR
- cluster purity
- runtime

### Expected possible result

CM may not be fastest, but it may retrieve structural relatives better.

That would be a genuinely valuable result.

---

## 13. Codex Prompt Sketch for Experiment D

```text
Implement Experiment D: Structural Geometry and Retrieval.

Generate families of related Boolean expressions with known family labels.
For each expression, compute CM structural feature vectors:
- operator counts
- quotient features against family seed
- containment features
- Jaccard features
- transformation features
- structural hash counts
- entropy/sparsity metrics

Also compute baselines:
- Bitset semantic vector / Hamming distance
- ROBDD/CUDD metadata features
- AST operator-count and subtree-hash features

Run retrieval:
For each expression, find top-k nearest neighbors using each representation.
Evaluate:
- Recall@1
- Recall@5
- Recall@10
- MRR
- cluster purity
- runtime
- memory

Create report:
CM_experiment_D_structural_geometry_retrieval_report.md

Final question:
Do CM-derived structural features retrieve related expressions better than Bitset semantic distance or ROBDD metadata?
```

---

## 14. If Experiment D Works, the Project Thesis Becomes Stronger

If CM structural retrieval works, the thesis becomes:

> **CMs provide an operator-structural coordinate system for Boolean expressions. This enables retrieval, clustering, drift tracking, decomposition, and explainable change reports that are not native to flat truth-table or canonical ROBDD representations.**

That would be a much more novel contribution than raw evaluator speed.

---

## 15. Summary of Most Promising Ideas

Ranked:

1. **Structural Geometry and Retrieval**
   - best chance of showing a unique CM capability

2. **Explainable Change Reports**
   - most practical/industrial value

3. **Containment Lattice**
   - cleanest mathematical artifact

4. **Transformation Orbits**
   - strongest operator-algebra visualization

5. **Structural Drift**
   - useful for versioned systems

6. **Decomposition Search**
   - potentially publishable operator algebra

7. **Backend Selection Heuristic**
   - practical hybrid compiler direction

8. **Operator Entropy**
   - useful diagnostic/predictive metric

---

## 16. Suggested Slide Titles

- From Evaluation Speed to Operator Geometry
- Bitset Sees Outputs; CUDD Sees Semantics; CM Sees Structure
- CM Quotienting: Directional Feature Difference
- The 16-Operator Containment Lattice
- Transformation Orbits of Boolean Operators
- Structural Drift Across Logic Revisions
- Finding Similar Boolean Designs by CM Features
- Toward a Hybrid Boolean Compiler
