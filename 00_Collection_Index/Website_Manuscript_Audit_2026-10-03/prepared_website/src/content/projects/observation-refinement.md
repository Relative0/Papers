---
title: Observation Refinement
description: A mathematical model of concept differentiation when a new observation splits a finite state space.
order: 5
phase: Observe
status: Research draft
question: What structural changes occur when a system learns to make a distinction it could not make before?
paperTitle: 'Successive Concept Differentiation as Observation Refinement'
paperStatus: Integrated MIND research draft v0.5, with referee repairs; priority and external review remain open.
paperContribution: Separates signature refinement, carrier splitting, and order thinning, then studies the topology and homology of finite refinement constructions.
paperLocation: See “Observation systems and three kinds of refinement” and “Carrier splitting under a new Boolean observation” in v0.5.
paperPdf: /manuscripts/observation-refinement-r2-v0.5.pdf
paperReadingCopy: 2
paperSourceVersion: Referee-repair draft v0.5, September 29, 2026; author corrected October 3, 2026. Earlier revisions retained in the collection.
paperByline: Brian Theory
---

## The mathematical tool

A small example comes first. With four possible states `00`, `01`, `10`, and `11`, observing only A leaves two pairs that look the same. Learning to observe B separates each pair. [Try the four-state demo](/#observation-example), then [see how ProLT builds observation spaces](/logical-topology/).

The draft asks what happens beyond this simple grouping. A new test may **split an old observational state** into two refined states; the manuscript calls this *carrier splitting*. If a test leaves those states intact but removes some order comparisons, that is *order thinning*. These are different operations, and the draft also studies how their associated complexes can change.

A coarse observer groups states that it cannot yet distinguish. Adding a Boolean observation can split those groups. The current MIND manuscript models this as an observation-product construction and studies how the associated order and topology change.

## What the draft establishes

The work separates carrier splitting from order thinning, classifies a restricted height-at-most-two case, and analyzes more complex interactions through homological methods. It includes explicit examples showing where simpler collapse or local-to-global expectations fail. The draft states its results for its particular finite model; publication priority remains under review.

## Why it matters to Being and Becoming

The coarse representation is one form of **Being**: the states as currently observed. A new observation changes the available distinctions. This is a precise mathematical example of **Becoming** in the research programme, although no psychological learning process is claimed by the theorem.

## Next research question

What kinds of observation updates can be selected, learned, or optimized under constraints? The related [RF-IDENT](/rf-ident/) branch asks one identification question; [Evolutionary Logic](/evolutionary-logic-2/) would ask how such changes unfold in time.
