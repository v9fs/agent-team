# Program Plan: Rust Port of fs/9p and net/9p

## Summary

- Program: port the v9fs kernel filesystem (`fs/9p`, `net/9p`) to Rust
- Human outcome: v9fs gains memory-safe Rust implementations, one proven
  component at a time, without breaking the C path, the mirror contract, or the
  harness
- Evidence version: `v9fs/linux` `upstream` =
  `602042bf29f6efde39cfb5fdd9289bf4854bc0c5` (v7.3-rc6+, 2026-10-07); E0009,
  E0010; `docs/reports/rust-port-inventory.md` (JSON regenerable; `docs/reports/**/*.json` is gitignored)
- This slice: R0, mapping and strategy only (Unmapped → Mapped). No kernel code.
- Strategy: D0003 (Proposed, human decision required)
- GitHub milestone: proposed `M2 - Rust v9fs` (to be created by a human or a
  `gh`-write agent)
- Branch: `cursor/rust-port-map-f6e3`
- Authority: A2 for this mapping PR. Executing the program is materially wider
  scope, so it needs human acceptance of D0003. Agents never merge into
  `v9fs/linux`. Upstream submission is external communication and is
  human-gated.
- Date: 2026-10-07

## Why a full port cannot start as one slice

At the pinned tip, the Rust bindings a filesystem needs do not exist in
mainline:

| Port area | C size (lines) | Kernel surface it needs | Upstream Rust status at `602042bf` |
| --- | --- | --- | --- |
| `net/9p/protocol.c` wire codec | ~800 | byte buffers, `kmalloc`, iov_iter | Enough exists for leaf parsers |
| `net/9p/client.c` RPC core | ~2,300 | spinlocks, idr/xarray, wait queues, kmem_cache, refcount, tracepoints | Mostly present (`sync`, `xarray`, `workqueue`); tracepoints are partial |
| `net/9p/trans_fd.c` (tcp, unix, fd) | ~1,100 | sockets, poll, workqueue | No socket abstraction |
| `net/9p/trans_virtio.c` | ~850 | virtio driver, virtqueue, scatterlist | No virtio abstraction (scatterlist exists) |
| `net/9p/trans_xen.c`, `trans_rdma.c`, `trans_usbg.c` | ~2,300 | Xen grant tables and xenbus, ib_verbs, USB gadget and configfs | None (configfs exists) |
| `fs/9p/*` VFS | 6,251 | file_system_type, fs_context, super, inode, dentry, file, address_space, netfs, fscache, posix_acl, xattr | Only `file.rs` and `kiocb.rs`; the Rust VFS series is RFC-only (E0010) |

The full inventory (ops tables, callback counts, and missing external symbols)
is `docs/reports/rust-port-inventory.md`. Rerun it on any new tag with
`scripts/rust-port-inventory.py`.

## Phases

Each row is one or more work slices under the slice contract. A phase starts
only when its gate is met. The phases don't promise any calendar dates.

| Phase | Outcome | Gate to start | Write scope | Proof target |
| --- | --- | --- | --- | --- |
| R0 (this PR) | Mapped surface, strategy proposal, first-slice design | — | this forge | Mapped |
| R-H | The harness builds and boots a `CONFIG_RUST=y` Image, and the existing suites stay green | D0003 accepted; #6 no longer holds the Image config | `v9fs/test` Image build + this forge | Integration (unchanged suite results with Rust enabled) |
| R1 | `p9dirent_read()` in Rust behind `CONFIG_NET_9P_RUST_DIRENT`, with C kept | R-H landed | `v9fs/linux` topic branch + `v9fs/test` config | Unit (KUnit differential) → Integration |
| R2 | `p9stat_read()` in Rust (9P2000 and .u stat, string ownership returned to `p9stat_free`) | R1 landed | same | Unit → Integration (.u mounts) |
| R3 | Internal typed 9P PDU codec in Rust, used by R1 and R2 and covering every message type | R2 landed | `v9fs/linux` | Unit + Contract (golden PDUs captured from diod) |
| Decision gate G1 | Human decides whether to send Phase 1 upstream and start Phase 2 | R1 and R2 landed with differential proof | — | — |
| R4 | `client.c` RPC core (tags, fids, request lifecycle, flush, error mapping) in Rust behind the same exported C ABI | G1 | `v9fs/linux` | Integration on all harness suites + operational comparison with the prior tag |
| R5 | `trans_fd` and `trans_virtio` in Rust | Upstream socket and virtio Rust abstractions merged (rerun the inventory) | `v9fs/linux` | Integration per transport |
| R6 | `fs/9p` VFS layer in Rust | Upstream Rust VFS, netfs, and fscache abstractions merged | `v9fs/linux` | Integration on all suites + operational |
| R7 | Retire the C implementation | Rust parity across every harness suite for several releases, plus maintainer agreement upstream | `v9fs/linux` | Operational |

Xen, RDMA, and USB gadget transports have no Rust bindings and few users. They
stay in C until a transport-specific trigger appears. They are not claimed by
this program.

## R1 design (first code slice)

- Component: new `net/9p/protocol_rust.rs`. It exports
  `p9dirent_read(clnt, buf, len, dirent)` via `#[export]`, so a signature
  mismatch with `include/net/9p/client.h` fails the build.
- Kconfig: `NET_9P_RUST_DIRENT` (depends on `RUST && NET_9P`, default `n`).
  When it is set, the C `p9dirent_read` is compiled out, and the C version is
  kept as `p9dirent_read_c` for the KUnit differential.
- Bindings: add `#include <net/9p/client.h>` to
  `rust/bindings/bindings_helper.h`. This is a shared file, so it needs Rust
  maintainer review upstream.
- Behavioral contract, matching the C code at `602042bf`:
  - Decode `Qqbs` (qid[13], u64 offset, u8 type, u16-length string) from
    `buf[0..len]`.
  - Return the bytes consumed on success.
  - Return `-EFAULT` when the buffer is short. That is what `pdu_read` yields,
    and the R1 KUnit captures it from the C build rather than assuming it.
  - Return `-E2BIG` when the name does not fit `d_name`, which is what
    `strscpy` returns.
  - Never read past `len` and never write past `sizeof(d_name)`.
  - Decide explicitly what a failed call leaves in `*dirent`. In C,
    `pdu_read()` (`net/9p/protocol.c:211`) `memcpy`s the partial bytes into the
    field before reporting a short read, so on failure `*dirent` is partly
    written. The only caller (`vfs_dir.c`) ignores `*dirent` on error. R1
    either reproduces this behavior or documents that it diverges, and KUnit
    compares outputs on failure accordingly.
  - Keep the debug print and `trace_9p_protocol_dump` behavior on failure, or
    explicitly document dropping it.
- Unit proof (KUnit `net/9p/protocol_kunit.c`): run C and Rust on identical
  inputs and compare the return value and every `p9_dirent` field. Inputs:
  well-formed entries captured from a diod readdir; truncation at every byte
  offset; name lengths 0, 255, 256, and 65535; and a deterministic
  pseudo-random corpus.
- Integration proof: `v9fs/test` diod-regression on the R-H Rust Image with
  `NET_9P_RUST_DIRENT=y`. Readdir-heavy suites must PASS with the same XFAIL
  set as the C Image. `v9fs_dir_readdir_dotl()` maps every negative return
  to `-EIO`, so the harness cannot tell errno values apart. Errno parity is
  claimed only at the KUnit level. Negative evidence: the same Image with a deliberately
  broken Rust decoder (wrong `d_off` width) fails KUnit and the readdir suites.

The R1 proof would fail if the Rust leaf were never linked (with the C symbol
still in use) or used a different field width. `/proc/kallsyms` would show the C
`p9dirent_read` instead of the Rust one, or the KUnit differential would report
a `d_off`/`d_type` mismatch at the first truncation offset.

## Proof Plan for this slice (R0)

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Mapped | `python3 scripts/rust-port-inventory.py /path/to/linux@602042bf --md docs/reports/rust-port-inventory.md` | Reproduces the committed Markdown byte-for-byte at the same HEAD |
| Static | `scripts/check-scaffold.sh`; `git diff --check`; `python3 -m py_compile scripts/rust-port-inventory.py` | Pass |
| Negative | Run the inventory on a tree without `rust/kernel` | Exits 2 with `missing rust/kernel`, so it can't report success on a non-kernel tree |
| Unit/Contract/Integration/Operational | not claimed | No Rust code exists yet |

The mapping would be wrong if it used a stale or synthetic tree. The report
embeds the scanned `HEAD`, and rerunning on a different tag changes the counts.

## Backlog Context (proposed horizon after R0 lands)

| Rank | GitHub issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 1 | [#6](https://github.com/v9fs/agent-team/issues/6) | t0013 ACL | Mapped → Integration | Already active; may hold the linux Image config scope | Not changed by this program |
| 2 | to create: R-H harness Rust Image | `CONFIG_RUST=y` Image boots with suites unchanged | Integration, no behavior change | Every Rust slice needs it | Blocked until D0003 is accepted and #6 frees the Image scope |
| 3 | to create: R1 Rust `p9dirent_read` | First Rust leaf with differential proof | Unit → Integration | Smallest untrusted-input leaf with a fixed ABI | Blocked on R-H |

Issues are not created in this run because the agent's `gh` is read-only and
D0003 is unaccepted. The bodies above are ready to paste into
`.github/ISSUE_TEMPLATE/work-slice.md`.

## Team Orchestration

| Role | Agent/thread | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- |
| Orchestrator | human (ericvh) | all | labels, milestone, D0003 decision | accept, amend, or reject D0003; create R-H and R1 issues | first |
| Evidence mapper | this run | `v9fs/linux@602042bf`, upstream lore/LWN | this forge (plan, report, ledgers) | R0 mapping | done in this PR |
| Implementer | later, per slice | per slice | R-H: `v9fs/test`; R1: `v9fs/linux` topic branch | product PRs | after D0003 |
| Independent reviewer | distinct from this run | full PR | review note only | Mapped decision on R0 | before ready |
| CI/proof owner | `v9fs/test` maintainers | harness | none for R0 | confirms the Rust Image is feasible in the docker build | before R-H |
| State closer | after merge | GitHub + records | labels/ledgers | landed reconciliation | last |

## Explicit non-claims

- No Rust code, no kernel build, no KUnit, and no harness run in R0.
- The inventory percentages are lexical name matches. They are not semantic
  coverage of abstractions.
- No commitment that upstream `net/9p` or VFS maintainers will accept Rust
  code.
- Xen, RDMA, and USB gadget transports are out of scope.
- No performance claim.

## Exit Criteria

- [x] Evidence, authority, dependencies, and write scopes are explicit.
- [x] Target behavior and non-claims are bounded.
- [x] Proof rejects the named plausible false positive (stale or synthetic tree).
- [ ] Required review and approval are complete.
- [ ] D0003 accepted or amended by a human; R-H and R1 issues created.
- [ ] GitHub and durable evidence agree after landing.
