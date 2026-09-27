# Literature verification notes

These notes record the primary-source comparisons used for the revised claim boundary. They are not a claim of exhaustive historical priority.

## Cheng, Zhao, Xu - raw aligned truth-vector superposition

**Daizhan Cheng, Yin Zhao, Xiangru Xu, "Matrix Approach to Boolean Calculus," CDC-ECC 2011, pp. 6950-6955, DOI 10.1109/CDC.2011.6160289.**

Proposition 3.3 states, for Boolean functions of the same ordered variables with truth tables/vectors `m_f` and `m_g`, and a binary logical operator sigma, the truth vector of the combined function is obtained by applying sigma entrywise. This is the direct antecedent used to calibrate the manuscript's numeric CM same-frame law.

Primary PDF: https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/0224.pdf

## Bricken - 2x2 logical matrices and bra-matrix-ket evaluation

**William Bricken, "Notes on Matrix Techniques for Logic," technical note internally dated March 1997.**

The note states that a two-variable logic function has a 2x2 table, enumerates all 16 binary logical operators, represents true/false as two-component vectors, and writes Boolean evaluation in the form `<x|B|y>`. Its later arithmetic includes operations outside the manuscript's single XOR-AND coefficient convention, so it is a representation/notation antecedent rather than the same complete calculus.

Primary PDF: https://wbricken.com/pdfs/01bm/01math/03math-supporting/math-tangential/04matrix-tech.pdf

## Gudder and Latremoliere - complementary Boolean frame pattern

**Stan Gudder and Frederic Latremoliere, "Boolean Inner-product Spaces and Boolean Matrices," Linear Algebra and its Applications 431 (2009), DOI 10.1016/j.laa.2009.02.028, arXiv:0902.1290.**

Their Boolean space uses coordinatewise Boolean join as vector addition. A stochastic vector is a mutually disjoint Boolean partition of unity. Example 2.13 cyclically shifts any stochastic vector to obtain an orthonormal basis. Specializing to the two-component stochastic vector `(X, not X)` produces `(X, not X)` and `(not X, X)`, exactly the row/column pattern of the manuscript's `S_X`. This is therefore a close antecedent to the frame geometry, while the global algebras remain distinct because the manuscript uses XOR-AND.

Primary PDF: https://arxiv.org/pdf/0902.1290

## Toffano / Eigenlogic - version-specific Dirac statement

**Zeno Toffano, "Eigenlogic in the spirit of George Boole," arXiv:1512.06632.**

The work was first posted in 2015. The specific statement that bra-ket notation is deliberately not used to emphasize that the method is not restricted to quantum physics occurs in version 12, dated 6 February 2018. The bibliography and prose now say this explicitly rather than attributing that sentence generically to the 2015 version.

Primary PDF for the cited statement: https://arxiv.org/pdf/1512.06632v12

## Published STP reference replacing unresolved placeholder

**Daizhan Cheng, Hongsheng Qi, Zhiqiang Li, _Analysis and Control of Boolean Networks: A Semi-tensor Product Approach_, Springer London, 2011, DOI 10.1007/978-0-85729-097-7.**

The book contains the chapter "Matrix Expression of Logic," pp. 55-65, and is used as a stable published reference for the STP logical-structure-matrix representation.

Publisher page: https://link.springer.com/book/10.1007/978-0-85729-097-7
