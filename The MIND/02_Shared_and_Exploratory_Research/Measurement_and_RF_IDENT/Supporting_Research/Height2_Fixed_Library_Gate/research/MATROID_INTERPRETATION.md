# Matroid interpretation

Use the notation D,A,B from REPAIR_GRAPH_DYNAMICS.md.

## The actual column matroid

Identify all formal roots to a distinguished root *. Since distinct coarse components have no shared nonroot vertices, this identification introduces no new cycle. The reduced incidence matrix remains B. Its column matroid M(B), on deleted triangles A, is a standard graphic matroid.

For induced T, every retained column is zero in every removed row. Therefore

  M(B_T)=M(B)|A_T.

This is exactly a matroid restriction (deletion of the missing triangle elements), not merely a conjectured analogy. No contraction is needed for this statement. Dependencies cannot be created under conditioning.

However, safety is not just "the actual triangles form a basis of their own column matroid." That statement misses full row rank: a rootless tree has independent columns spanning its column space but leaves a nonzero relative H1 defect.

## Full-rank augmentation and an exact minor

Adjoin one artificial edge s_e from * to each deleted-edge vertex e. The augmented reduced incidence matrix is

  [B | I_D].

This is still a graphic matroid and has rank |D|. The actual triangle set A is a basis of this augmented matroid iff B is square invertible, exactly repair safety.

Let J=D\D_T. Contract the artificial edges s_e for e in J and delete the actual triangle columns A\A_T. The unit columns being contracted are independent; contraction quotients out their coordinate directions. In the remaining representation the contracted rows disappear, leaving

  [B_T | I_(D_T)].

Thus conditioning IS an exact standard graphic-matroid minor in this augmented, provenance-aware representation. Retained actual columns were zero in the contracted rows, so the construction agrees with the direct restriction theorem.

The abstract column matroid alone forgets world/triangle provenance and the row target. It cannot by itself say which support deletions are permitted or detect lost anchors. One must carry the support labels and augmented root data.

## Priority

Incidence representations, graphic bases, deletion and contraction are standard. The relevant derived result is their exact fit to this particular support-restriction operation, together with the obstruction interpretation. A claim that conditioning has "no matroid-minor description" is too strong and is rejected.
