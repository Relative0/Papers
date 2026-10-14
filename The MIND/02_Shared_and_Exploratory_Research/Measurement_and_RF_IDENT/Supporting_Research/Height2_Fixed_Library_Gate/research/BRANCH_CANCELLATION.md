# H1: branch cancellation

## Statement

Let S be a current support with observational preorder <=_Phi, and let T={x in S:q(x)=b}. Under the canonical identification of realized signatures,

  P_(Phi union {q},T) ~= P_(Phi,S)|T

when the old signature is injective on S. In particular, for an initially post-T0 protocol using only query refinement followed by answer conditioning,

  P_h ~= P0|S_h.

Legality of q is not needed for this identity.

## Proof

For x,y in T the new order condition is

  x <=_Phi y and q(x)<=q(y).

Both new values equal b, so the second condition is automatic. Existing coordinates remain unchanged. Thus the new preorder on T is exactly the old induced preorder. Injectivity supplies a canonical bijection between worlds and quotient vertices. At a later history every previously acquired query coordinate is constant; induction proves the stated identity.

Before T0 the same preorder equality still holds, but a careless statement about an induced subposet on worlds would conflate worlds and quotient vertices. The current gate avoids that issue by its initial post-T0 hypothesis.

## Consequences

1. Adding q may genuinely thin the order before its answer; that thinning has no internal effect inside either answer fiber.
2. The next state is the induced ORIGINAL order on the surviving support, not the unconditioned globally thinned order.
3. A query used earlier is constant on every descendant, and cannot usefully reappear.
4. Height and T0 are preserved; a memoized solver needs only a support bitmask for a fixed input (P0,Q).

This is an elementary specialization of coordinate restriction, and was already used in A1. It is not a new general decision-tree theorem.
