# dynamo/log-report — fixed task

Fixes four issues found in the original task bundle:

1. **Format** — `task.toml`'s `artifacts` was a bare string pointing at a
   path (`/app/out.json`) nothing wrote to. Now a top-level array pointing
   at the real output, `/app/report.json`.
2. **Environment** — `Dockerfile` used an unpinned `python:latest` base and
   copied `solution_hint.py` (the reference solution) into the agent's own
   container. Base is now pinned by digest and the leaked file is removed
   from the build context.
3. **Verifier** — `tests/test_outputs.py` only checked that `report.json`
   existed and was non-empty. It now recomputes expected values directly
   from `access.log` and checks `total_requests`, `unique_ips`, and
   `top_path` individually, one test per instruction.md criterion.
4. **Instruction** — `instruction.md` was vague prose with no defined
   output path or schema. Rewritten to specify the exact path and keys the
   verifier checks.

See `solution/` for the reference solve script and `tests/` for the
verifier.
