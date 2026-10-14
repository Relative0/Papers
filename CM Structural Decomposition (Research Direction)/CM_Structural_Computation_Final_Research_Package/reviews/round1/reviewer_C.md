# Round 1 Reviewer C: Finite-field linear algebra and tensor representations

**Status:** internal AI role-based adversarial review of frozen Draft 1. Not an external referee, separate model, or independently recruited reviewer.

The elementary equalities in Sections 5--6 are correct as written, and inclusion of r=0 is important. The report does not yet explain why the four families deserve joint attention beyond code availability. A small hierarchy analysis would help.

R1-C1: let W be the row span and compare the number of actual rows modulo the all-ones complement direction with rank(W). This quotient yields useful bounds with an explicit distinction according to whether the all-ones vector belongs to W. R1-C2: the inner-product matrix should give a sharp fixed-cut example in which a short GF(2) factorization and a large explicit prototype dictionary differ substantially. Any separation must keep the cut fixed, since regrouping coordinate pairs creates an obvious XOR decomposition.

R1-C3: minimal rank after conditioning is not the retained factor width. Show a factor-only recompression, with cancellation cases, instead of calling the retained width the rank. R1-C4: tensor-train comparison needs a field-sensitive example. A low binary-field rank need not be low real rank; state the example, prove it, and do not present the generic fact as new.

Minor issue: V is both a variable list and a matrix factor. Use U,W for matrix factors. The fatal flaw test is replacing GF(2) matrix multiplication with integer multiplication when counting; the current code avoids it. I found no false theorem in the submitted draft. I would support a substantially strengthened expository/methods report, but priority for the elementary quotient and factorization arguments remains unestablished.
