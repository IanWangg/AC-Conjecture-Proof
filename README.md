# Andrews–Curtis research

## Status: no free-group solution established

This repository records a ten-agent investigation begun on 2026-11-02. It does **not** prove AK(3) AC-trivial or non-AC-trivial, and does **not** prove or disprove the Andrews–Curtis conjecture. No novelty or priority claim is made for the partial results.

The target is ordinary, unstabilized AC triviality of

    AK(3) = <x,y | x^3 y^-4, xyx y^-1 x^-1 y^-1>.

The repository was initially empty. Ten research agents have worked with up to three researchers concurrently, the maximum available alongside the coordinating agent. Each read previous work before independently choosing a direction. Reports record sources, rationale, exact proofs or computations, and limitations. Overlapping directions were coordinated explicitly; later reports credit shared discoveries. The coordinating agent reviewed the arguments and replayed the artifacts before publication.

## Current strongest checked results

- **Raw peak at least 22:** a complete cap-21 component has 27,380,372 inversion/permutation orbit states, no total length below 13, and no primitive relators. A separate string-based checker verifies its closure, including 112,696,624 allowed-neighbor checks. See the [packed extension](research/packed-peak-extension.md), [results](results/packed_peak_extension.json), and [independent source review](research/packed-audit-review.md).
- **Cyclic peak at least 15:** an analytic all-n theorem gives cyclic peak at least 2n+9 for AK(n), n>=3. This is a different energy from the raw bound above.
- **No initial primitive replacement, at any length:** neither one-relator deletion quotient permits a primitive free relator as a single quotient-conjugacy replacement for AK(n), n>=3. This unbounded one-step theorem is not preserved after both coordinates change.
- **Constructive infinite-quotient paths:** AK(3)'s image has exact instruction distances 10 in the braid quotient and 8 in the torus quotient. A synchronized 191-strict-move path works in their combined product. A further explicit path works in the nonsolvable braid relation-module extension F/[N,N], with 205 stored word operations expanding to 531,377 strict moves. Its actual free endpoint remains nontrivial.

All these results leave the original four breakthrough objectives unachieved.

## Research reports

| Agent | Result | Scope |
|---|---|---|
| [A](research/research-a.md) | Exact initial nonincreasing quotient-conjugacy plateau for AK(n), n>=3 | Analytic cyclic bound 2n+8, strengthened by F |
| [B](research/research-b.md) | Explicit nilpotent paths and finite-quotient distance principle | Uniform class-2 path; 48-move class-3 AK(3) path with nonzero lifting errors |
| [C](research/research-c.md) | MS(n,y^-1 x^2 y^-1) is ordinary-AC equivalent to AK(n) | Symbolic all-n proof; 6n+14 strict moves, including 32 for n=3; not a trivialization |
| [D](research/research-d.md) | Complete raw cap-18 exclusion in two independent implementations | Original raw bound 19; superseded by the coordinating agent's [cap-21 extension](research/packed-peak-extension.md) |
| [E](research/research-e.md) | Exact distance 10 in the braid quotient B3 | Every quotient annihilating the braid relator has the same uniform upper bound |
| [F](research/research-f.md) | Cyclic peak at least 2n+9 for AK(n), n>=3 | AK(3) cyclic bound 15; explicit length-15 generalized replacement shows where the initial-family argument stops |
| [G](research/research-g.md) | Exact distance 8 in the complementary torus quotient | Exact free lift errors factored into 6 and 5 conjugates of the power relator |
| [H](research/research-h.md) | Uniform torus-family path with 2n+2 strict moves | Jointly develops G's pattern; pseudo-meridian distinction does not obstruct these two-coordinate AC paths |
| [I](research/research-i.md) | Braid lift errors have exact areas 5 and 13 | Nonzero relation-module errors; proper rank-2 endpoint subgroup prevents a Nielsen-only completion |
| [J](research/research-j.md) | Unbounded initial primitive-replacement exclusion | Uniform AK(n), n>=3 theorem using Nielsen uniqueness, traces and free-product normal forms |

Further research:

- [G's product synchronization](research/research-g-product.md) supplies a 191-strict-move path in B3 times T(3,4), with exact fourteen-instruction distance between 13 and 191. [Independent review](results/product_independent_review.json) replays the certificate using separately written quotient evaluators.
- [I's actual first-order correction](research/research-i-first-order.md) removes the braid-kernel module errors in F/[N,N], N the braid-relator normal closure. [Independent free-word and Fox replay](results/first_order_independent_review.json) confirms this quotient endpoint. The actual free words have lengths 230,627 and 946,303. The correction preserves braid images and need not preserve the torus factor; it is not claimed to refine the product result simultaneously.
- The coordinating agent's [finite PSL quotient experiment](research/finite-quotient-experiment.md) is now bounded uniformly by E's ten-move certificate, ruling out distance divergence in that entire representation family.

## Reproduce

Python 3 and its standard library replay all Python certificate checks, formula tests, the cap-18 baseline, and complete short instruction balls:

```sh
python3 experiments/reproduce.py
```

Add the independent original-state C++ cap-18 exhaustion and the long endpoint's subgroup fold:

```sh
python3 experiments/reproduce.py --cpp
```

Regenerate and independently audit the entire cap-21 component, including its primitive-relator scan:

```sh
python3 experiments/reproduce.py --cpp --packed
```

The C++ options require a C++17 compiler. The cap-21 option generates a roughly 356 MB native checkpoint and needs memory for the state sets. The default and `--cpp` runs explicitly report `raw_cap_replayed: 18`; the separately checked published cap-21 evidence is in [results/packed_peak_extension.json](results/packed_peak_extension.json). Only the `--packed` run regenerates that full result. Individual reports give standalone commands and precise finite bounds.

The dependency-free [strict elementary verifier](experiments/elementary_verify.py) accepts only relator inversion, positive right multiplication, and single-generator conjugation, with exact endpoints. It performs no implicit generator changes, stabilization, quotient rewriting, or endpoint normalization. The first-order certificate has a distinct word-conjugation format and [independent verifier](experiments/verify_first_order.py), with its finite ordinary expansion proved explicitly. The compact `.json.gz.b64` certificate contains all actual words after standard-library decoding.

## Completion standard and remaining work

A positive ordinary-AC result needs a complete proof or replayable path to the standard **free** basis. An obstruction must be invariant under all permitted moves at unbounded length. Group triviality, success in a quotient, and finite search failure do not meet either standard. Computations here are checked programs and explicit certificates, not proof-assistant formalizations.

The full cap-21 region has now been classified; cap 22 and higher remain outside the exclusion. The primitive theorem constrains only initial fixed-relator phases. The quotient paths leave nontrivial free errors, even after the first-order module correction. A finite termination argument or a global invariant remains missing. The original goal therefore stays active.

## Primary-literature cautions

- [Lisitsa's corrected published paper (2025)](https://doi.org/10.1016/j.jaca.2025.100041) reports that an earlier stable AK(3) claim depended on an incorrect theorem. That claim is not a solved starting point here.
- [Gilman and Myasnikov, Andrews–Curtis groups](https://gcc.episciences.org/15972/pdf) gives the algebraic setting.
- [Carreras's 2026 certificate preprint](https://arxiv.org/abs/2607.23611) supplies prior n=3 equivalence context credited in C. Restricted graph bounds from other sources are not silently transferred to ordinary AC paths.

Each report links the additional primary sources it used and distinguishes external theorems from deductions and experiments produced here.
