"""Serialize the actual bounded research record, not a synthetic search history."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

sources = [
 ('P01','Aranda Pino; Goodearl; Perera; Siles Molina','Non-simple purely infinite rings','arXiv:0806.4156; DOI:10.1353/ajm.0.0119','https://arxiv.org/pdf/0806.4156','2008 preprint; 2010 publication','Full text, Definition 2.1 and Lemma 2.2, PDF pp. 5-6','Defines rectangular matrix factorization comparison and its transitivity and zero-padding properties.','Equivalent underlying relation','Later pure-infiniteness results are not imported.','The factorization preorder itself has explicit prior art; CM/LM interpretation remains an application.'),
 ('P02','Antoine; Ara; Bosa; Perera; Vilalta','The Cuntz semigroup of a ring','arXiv:2307.07266v1; DOI:10.1007/s00029-024-01002-9','https://arxiv.org/html/2307.07266v1','2023 preprint','Full text, section 2.5; Lemma 2.6 proof; Lemma 8.2; references [9] and [25]','Same factorization comparison for stabilized matrices; rectangular formulation explicit; uniserial matrices diagonalize.','Equivalent comparison, broader framework','Nearly simple domain computations do not apply to this finite chain ring; addition is block sum, not independent tensor.','Direct antecedent, with backward route to P01 and Hung-Li. No novelty claim for the preorder.'),
 ('P03','Hung; Li','Malcolmson semigroups','arXiv:2201.01432; DOI:10.1016/j.jalgebra.2023.01.031','https://www.math.buffalo.edu/~hfli/malcolmson14.pdf','2023 author manuscript','Full text, Definition 3.1; Lemma 3.6; Proposition 3.7, pp. 8-11; reference [26]','Adds triangular-block erasure to factorization and characterizes the resulting order for Artinian local rings with central principal radical.','Strictly broader order','Its extra generator is not an allowed pure local filter.','Do not import its sufficiency criterion into T09; it explains why filtered-rank inequalities are insufficient there.'),
 ('P04','Jaikin-Zapirain; Lopez-Alvarez','On the space of Sylvester matrix rank functions','arXiv:2012.15844v1','https://arxiv.org/pdf/2012.15844','2020 preprint','Full text, section 2.1, Proposition 2.2; section 2.2, Corollary 2.4','Classifies extreme Sylvester ranks for truncated polynomial rings via regular representations of quotients.','Equivalent normalized one-variable rank functions','Does not claim these rank inequalities characterize pure factorization.','rho_t/(4-t) is established; the multivariable free-target criterion is separately proved by a unit minor.'),
 ('P05','Cao, Yonglin','On the Multiplicative Monoid of n x n Matrices Over Artinian Chain Rings','DOI:10.1080/00927870903133946','https://www.tandfonline.com/doi/abs/10.1080/00927870903133946','2010','Publisher abstract and bibliographic metadata only; full-text route inaccessible','Studies matrices, submodules, Green relations and related monoid classes over Artinian chain rings.','Highly relevant; exact theorem relationship unresolved','No full-text theorem inspected, no theorem-number attribution.','Strong lead for direct T09 attribution; cannot certify the exact classification from an abstract.'),
 ('P06','Byrne; Horlemann; Khathuria; Weger','Density of Free Modules over Finite Chain Rings','arXiv:2106.09403v2; DOI:10.1016/j.laa.2022.06.013','https://arxiv.org/html/2106.09403v2','2022','Full text, section 2.1; section 2.3 Proposition 3 and cited sources','Cyclic decomposition, module type and conjugate shape over finite chain rings.','Standard algebraic ingredients','Density theorems do not by themselves state the operational filter order.','Smith/module labels and counts are classical machinery.'),
 ('P07','The Stacks Project','Fitting ideals','Tag 07Z6; Lemma 15.8.1; Lemma 15.8.7','https://stacks.math.columbia.edu/tag/07Z6','Accessed 2026-09-20','Full text, cited lemmas and proofs','Minor ideals decrease under multiplication; residue dimensions relate to local generator bounds.','Standard ingredients','The explicit free-extraction iff is proved directly in this review, not quoted as a Stacks theorem.','Supports treating R4 as elementary local-ring matrix algebra.'),
 ('P08','Blunck; Havlicek','On distant-isomorphisms of projective lines','arXiv:1304.0226; DOI:10.1007/s00010-004-2745-7','https://arxiv.org/pdf/1304.0226','2005 publication; 2013 arXiv upload','Full text, sections 2.4 and 3.1-3.5; Theorem 5.4 hypotheses','Ring-induced projective maps and radical parallelism; semisimple endomorphism-ring classification.','Adjacent geometry, not the same ambient-linear stabilizer theorem','Theorem 5.4 is for endomorphism rings over fields; A is local with nilpotents.','No field-only classification is transferred to A; exact linear-stabilizer priority remains unresolved.'),
 ('P09','Schumacher; Westmoreland','Almost quantum theory','arXiv:1204.0701v1','https://arxiv.org/html/1204.0701v1','2012','Full text, sections 3.3-3.4, equations 18-24; baseline section 4 analysis retained','Conditional pure states, unobserved mixtures as spans, and complete generalized effects.','Inherited modal semantics','No probabilities, Born rule or complex quantum LOCC conclusions imported.','Resolved versus unresolved disposal is standard modal conditioning; the explicit ring-coordinate witness is an application.'),
]

queries = [
 ('matrix semigroup finite chain ring Green J order invariant factors Smith normal form','Found Cao and algebraic Cuntz comparison leads.'),
 ('matrix over local ring rank modulo maximal ideal invertible minor direct summand','Mixed primary and informal results; informal answers not relied upon.'),
 ('normalizer endomorphism algebra finite local ring semilinear group projective line','No exact primary normalizer theorem verified; direct proof retained.'),
 ('"On the Multiplicative Monoid" "Chain Rings" pdf','Publisher abstract found; full text not obtained.'),
 ('"Green" "chain rings" "invariant" matrices','Cao lead; no theorem-level conclusion from snippets.'),
 ('"The Cuntz semigroup of a ring" arxiv','Located arXiv:2307.07266.'),
 ('site.stacks.math.columbia.edu matrix rank local ring minor invertible','Located Stacks Fitting-ideal material; literal query used site.stacks, not a site: filter.'),
 ('"Yonglin Cao" "3404" pdf','No accessible full-text copy verified.'),
 ('"Malcolmson" "matrix" "semigroup" rank ring Hung Li','Located author manuscript and publisher page.'),
 ('"normalizer" "algebra" "semilinear" "ring" projective','No exact ambient-linear specialization certified.'),
 ('"Purely infinite simple rings" "Cuntz" Ara Goodearl Pardo 2002 pdf','Broader backward search; later identified exact 2008 reference from bibliography.'),
 ('"Schmidt rank" "local filtering" "hidden nonlocality" Popescu 1995 arxiv','No additional primary result adopted from this query.'),
 ('"Non-simple purely infinite rings" arxiv','Located arXiv:0806.4156; inspected Definition 2.1.'),
 ('"Sylvester rank functions" "Artinian" "local" "Jaikin" "López"','Followed Hung-Li reference [26] to arXiv:2012.15844.'),
]

routes = [
 ('https://www.tandfonline.com/doi/full/10.1080/00927870903133946','Direct full-text access','Inaccessible via tool; abstract-only status retained.'),
 ('https://arxiv.org/html/2307.07266v3','Direct open, guessed version','404; corrected from arXiv abstract page to v1; no v3 claims.'),
 ('https://arxiv.org/abs/2307.07266 -> HTML link','Primary archive navigation','Inspected v1 section 2.5 and Lemma 2.6; definitions match rectangular factorization.'),
 ('https://zaguan.unizar.es/record/148932/files/texto_completo.pdf','Repository open','Timed out; arXiv full text used instead.'),
 ('https://arxiv.org/html/2307.07266v1 references [9] and [25]','Backward citations','Inspected Aranda Pino et al. and Hung-Li; not simply title matching.'),
 ('https://www.math.buffalo.edu/~hfli/malcolmson14.pdf reference [26]','Backward citation','Inspected Jaikin-Zapirain and Lopez-Alvarez Proposition 2.2 and Corollary 2.4.'),
 ('https://arxiv.org/html/2012.15844v2','Direct HTML attempt','Failed; inspected arXiv PDF v1, which states its own version.'),
 ('https://arxiv.org/html/2307.07266v1 discussion of Hung-Li and earlier comparison','Forward citation within later primary work','Confirms later use of the earlier comparisons; not a comprehensive citation-index scan.'),
 ('https://arxiv.org/html/2106.09403v2 section 2.1','Baseline primary-source revisit','Verified module type/shape definitions.'),
 ('https://arxiv.org/pdf/1304.0226 sections 2-3 and Theorem 5.4','Baseline primary-source revisit','Checked field-endomorphism hypotheses; cannot substitute for finite-local-ring stabilizer proof.'),
 ('https://stacks.math.columbia.edu/tag/07Z6','Direct primary reference','Inspected minor behavior and local residue/generator lemma.'),
 ('https://arxiv.org/html/1204.0701v1 sections 3.3-3.4','Baseline primary-source revisit','Confirmed distinction between selected coefficient effect and unobserved span.'),
]

def write(name, fields, rows):
    with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(fields)
        w.writerows(rows)

write('LITERATURE_LEDGER.csv',
      ['id','authors','source','identifier','url','date','inspected_material','relevant_result','relationship','limitations','priority_implications'],sources)
write('SEARCH_LOG.csv',['date','route','actual_query_or_location','disposition'],
      [('2026-09-20','web search',query,result) for query,result in queries]+
      [('2026-09-20',route,location,result) for location,route,result in routes])
print(f'Wrote {len(sources)} source rows and {len(queries)+len(routes)} research-route rows.')
