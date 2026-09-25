# Type Migration Map

This file records the corrected native typing used in the block rebuild.

| Earlier shorthand object | Native Boolean block object |
|---|---|
| four-bit CM phase pattern `a0a1a2a3` | four-bit phase vector and selector of rotations |
| phase action associated with that pattern | `Lambda(a) = XOR {P^k : ak=1}`, a `4 x 4` Boolean operator |
| quarter rotation | native `P` |
| rotation difference | `N = P XOR I4` |
| former delta-like phase action | `N^2 = I4 XOR P^2` |
| former all-four phase action | `N^3 = I4 XOR P XOR P^2 XOR P^3` |
| one logical state with two phase coefficients | ordinary 8-bit vector |
| `2 x 2` phase-valued gate | ordinary `8 x 8` Boolean block matrix |
| two-logical-bit state | ordinary 16-bit branch-phase vector |
| two-party coefficient/resource matrix | ordinary `8 x 8` Boolean transfer matrix |
| local two-outcome basis | pair of `4 x 8` Boolean effect blocks |
| three-logical-bit state | ordinary 32-bit branch-phase vector |
| teleportation global analyzer | ordinary `32 x 32` Boolean matrix |
| old conjugate-transpose gate condition | ordinary Boolean transpose/orthogonality after block expansion |
| class `(a,b)` | native normal form `diag(N^a,N^b)` |

The important warning is that the original `2 x 2` CM truth-table identity is **not** the same typed object as `N^2`. The former is idempotent under native `2 x 2` CM composition; the latter is a derived `4 x 4` rotation operator and satisfies `(N^2)^2=0`.
