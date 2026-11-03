# Computability formulations of the ordinary Andrews–Curtis conjecture

Date: 2026-11-03. This note gives elementary recursion-theoretic reformulations and checked literature boundaries. It proves no AC trivialization, counterexample, undecidability theorem, or independence result. No novelty claim is made.

## Prior reading and chosen focus

Before choosing this direction I read the repository's twenty-five-researcher README and Research B's finite-quotient metric discussion. The earlier search certificates and restricted primitive-free subgroup theorems do not settle the unrestricted orbit question. I chose to distinguish effective search, promise decision, proof compilation, and uniform size bounds; conflating these produces invalid undecidability arguments.

## 1. Two computably enumerable sets

Fix an effective finite-string encoding of balanced presentations

    P=<x_1,...,x_k | r_1,...,r_k>,

and let I_k be the literal tuple (x_1,...,x_k). Work with ordinary unstabilized AC moves, expanded into coordinate inversion, positive right multiplication by another coordinate, and conjugation by a single signed ambient generator. At each fixed rank this instruction alphabet is finite. Conjugation by an arbitrary word is a finite sequence of these elementary conjugations, so expansion changes the metric but not reachability.

Let T be the set of encoded balanced presentations defining the trivial group, and A the set admitting a finite ordinary path to I_k.

**Proposition 1.** Both T and A are computably enumerable; A is a subset of T; the AC conjecture is exactly A=T.

**Proof.** A path certificate is a finite instruction list. Apply it with exact free reduction and compare the endpoint with I_k. This is a decidable verification procedure, so dovetailing over lists enumerates A.

A finite triviality certificate supplies, for every generator x_i, an explicit identity in the ambient free group

    x_i = product_j (g_ij r_(a_ij)^(epsilon_ij) g_ij^-1).

All indices, signs and words are included. Free reduction decides validity. Such identities exist exactly when all generators belong to the relators' normal closure, equivalently when the presented group is trivial. Enumerating certificates therefore enumerates T. Ordinary AC moves preserve that normal closure, giving A⊆T. The asserted equality is precisely the conjecture. QED.

This is a semidecision procedure: if P is AC-trivial the path search eventually halts; otherwise it runs indefinitely. A finite failed search does not decide nonreachability. Even a promise that P belongs to T does not currently make this particular search known to halt.

Write V(P,t) for the decidable triviality-certificate verifier and W(P,s) for the decidable strict-path verifier. The conjecture has the syntactic arithmetic form

    for every P,t there exists s:  not V(P,t) or W(P,s).

Thus it has a Π^0_2 formulation, while its negation has a Σ^0_2 formulation. This is a syntactic upper classification; no completeness or logical-independence theorem is claimed. For a single fixed AK(3) input, existence of a path is Σ^0_1 (there exists a finite verified instruction list), and nonexistence is Π^0_1.

## 2. An exact proof-compiler equivalence

**Proposition 2.** AC is equivalent to existence of a total computable procedure C(P,t) which outputs a valid strict AC path whenever V(P,t) holds, and outputs a designated rejection on invalid inputs.

**Proof.** If AC is true, first verify t. Reject if invalid; if valid, enumerate all strict AC paths until one reaches I_k. The conjecture guarantees termination on every valid input; rejection terminates on all others. Conversely every P in T has some valid t, so such a compiler supplies an AC path for every P in T. QED.

Equivalently, AC holds if and only if there is a total computable function f(m) such that every valid pair (P,t) of total encoded length at most m has an AC path of encoded length at most f(m). From a total compiler, run it on the finitely many strings of length at most m and take the largest output length. Conversely, verify t and exhaust all path certificates up to the stated bound. Invalid encodings are rejected. This bound measures presentation **and triviality proof**, not merely presentation size.

One may study an explicit compiler's correctness and termination, or seek a family for which ordinary normal-closure proofs are much shorter than AC proofs. These are concrete proof-complexity targets, although enumerating paths alone adds no new guarantee of termination.

## 3. Why a presentation-size bound is stronger

Use any effective presentation-size encoding with finitely many strings of size at most n. Let L(P) be shortest strict ordinary path length, or infinity if no path exists.

**Proposition 3.** The following two assertions are equivalent:

1. A is decidable on all balanced presentations.
2. There is a total computable B(n) such that every P in A satisfies L(P)≤B(size(P)).

**Proof.** A bound decides membership by a finite finitely branching path search. Conversely, use the decider to select the finitely many P of size at most n that belong to A. Run path search on all selected inputs until all finish, and take the largest path length. This computes B(n). QED.

Consequently the existence of a total computable bound applying to **every trivial balanced presentation**, with a path guaranteed within that bound, is equivalent to

    AC is true AND T is decidable.

Indeed such a bound first implies every trivial input is AC-trivial, and bounded path search then decides T. Conversely AC plus a decider for T gives the same finite-list construction. AC alone does not currently justify this stronger recursive bound depending only on presentation size. Finiteness of the list of trivial inputs of bounded size does not make that list effectively identifiable.

The same conclusions hold for a uniform **raw intermediate total-length** bound. Such a bound leaves finitely many rank-k tuples to search. Conversely a path of length l from raw size N has raw size at most 2^l(N+2)-2 throughout: multiplication at most doubles total length and generator conjugation adds at most two. Thus recursive path bounds and recursive raw-peak bounds are interconvertible. No claim about unbounded conjugating tails follows merely from counting bounded cyclic representatives.

## 4. Undecidability and lower-bound cautions

The general Adian–Rabin theorem does not settle balanced triviality. A recent primary source still explicitly lists the existence of an undecidable triviality family consisting entirely of balanced presentations as open: Kegel–Li–Ren, *Small undecidable groups and unrecognizable 4-manifolds*, arXiv:2609.10461v1 (9 September 2026), Section 1.1 after Definition 1.2. Its new families have unequal generator/relator counts. [Primary source](https://arxiv.org/html/2609.10461).

Bridson constructs AC-trivial balanced presentations of rank at least four whose required moves grow beyond every fixed-height exponential tower as input length grows. These are large **computable** lower bounds, valid even with the stronger allowed moves in that paper. They neither prove nonrecursive growth nor settle rank-two AK(3). The same paper explains that a restricted family can have efficiently decidable AC-triviality despite enormous shortest move sequences. See Theorem A and Section 7.3 of [Bridson, arXiv:1504.04187v1](https://arxiv.org/pdf/1504.04187).

Large lower bounds are not confined to higher rank: [Lishak, *Balanced finite presentations of the trivial group*, arXiv:1504.00418v2](https://arxiv.org/pdf/1504.00418), constructs two-generator, two-relator examples with non-elementary triviality-proof area and simplification complexity, and discusses their AC-triviality in the introduction. This is a different explicit family; it does not identify AK(3) as a counterexample or establish nonrecursive complexity.

A genuine undecidability route to refuting AC would have to preserve the **all-inputs-trivial promise**: for example, an effectively constructed family of balanced trivial presentations on which AC reachability is undecidable. If AC held, the constant YES answer would decide that promise problem, a contradiction. This would require substantial new structure. Showing undecidability of unrestricted group triviality or unrestricted presentation questions does not provide it, nor would it by itself identify AK(3) as a counterexample.

## What this says about AK(3)

An exact path enumerator is a legitimate program whose halting is equivalent to AK(3) being ordinarily AC-trivial. A proof that this particular program never halts would prove non-AC-triviality. Simulating it for a large finite time does not prove nonhalting. The halting problem is a universal undecidability theorem, not a theorem that this specific machine's behavior cannot be proved.

The current cyclic-peak lower bound and finite kernel certificates are rigorous restrictions on candidate computations. They do not yet supply a complete halting proof, a nonhalting invariant under every ordinary move, or a proof compiler with established termination. The computability reformulation clarifies the remaining task without resolving the four original breakthrough objectives.
