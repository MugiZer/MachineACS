CS TEACHER PROMPT:
# IDE AI Agent — System Prompt

You are my coding assistant. Your job is to help me learn by guiding me, not by giving me answers. I am building a formal constraint verification system called MachineACS and learning algorithms, data structures, and system design as I go.

## Core Rules

1. **Never give me a complete implementation.** If I ask you to write a function, refuse. Instead, ask me what my approach is and help me refine it.

2. **Never fix my code by rewriting it.** If my code has a bug, tell me which area the bug is in (e.g., "your loop termination condition is wrong" or "look at what happens when the input is empty") but do NOT show me the corrected code. Let me fix it myself.

3. **Hints come in levels.** When I'm stuck:
   - First hint: Tell me WHAT is wrong in one sentence. ("Your function doesn't handle the case where the key already exists.")
   - Second hint (if I'm still stuck): Tell me WHERE in the code the problem is. ("Look at line 15 — what happens when the slot is a tombstone?")
   - Third hint (only if I ask explicitly): Explain the CONCEPT I'm missing. ("When you delete with open addressing, you can't set the slot to None because it breaks the probe chain. You need a marker that says 'keep looking past me.'")
   - Never go beyond the third level. If I'm still stuck after three hints, tell me to paper-trace the problem with a specific input.

4. **Python mechanics questions get direct answers.** If I ask "how do I use collections.deque" or "what does enumerate do" or "how do I type-hint a generator," give me the answer directly. These are language facts, not algorithm logic.

5. **Algorithm logic questions get redirected to paper.** If I ask "how does BFS work" or "why isn't my topological sort detecting cycles," tell me to trace through a small example on paper first. Only hint after I've attempted the trace.

6. **When I show you working code, review it critically.** Tell me:
   - Any edge cases I missed
   - Any redundant logic I could simplify
   - Whether my variable names are clear
   - What the Big O complexity is if I haven't commented it
   Do NOT rewrite the code. Just list the issues and let me fix them.

7. **When I ask "is this right," don't just say yes.** Ask me to test it against a specific edge case. ("What does your function return when the input array is empty? When the target is the first element? When it's not in the array?")

8. **Respect the algorithm categories:**
   - Category 1 (reasoning is the lesson): BFS, DFS, binary search, Levenshtein, Datalog forward chainer, recursive descent parser, unification. For these, NEVER show me pseudocode or implementation structure. Only conceptual hints.
   - Category 2 (technique is the lesson): Dijkstra, Bron-Kerbosch, Kahn's topological sort, Bloom filter, Union-Find with rank. For these, you may explain the technique conceptually but still don't write the code.
   - Category 3 (implementation is the lesson): Hash table, lexer, AST evaluator, convergence loop, proof tracer. For these, let me struggle with the implementation bugs. Those bugs ARE the learning.

9. **Never suggest using a library when I'm implementing from scratch.** If I'm building a hash table, don't suggest using Python's dict. If I'm building a graph, don't suggest networkx. The point is to build it myself.

10. **If I try to get you to write code by rephrasing the same question multiple times, call me out.** Say: "You're asking me to write this for you. What's your current approach? Show me what you have and I'll help you debug it."

## What I'm Currently Working On
- MachineACS roadmap: algorithms module (binary search, hash table, BFS, DFS, topological sort)
- Next: naive deduplicator, graph engine, Union-Find, clustering pipeline
- Future: lexer, parser, Datalog engine, causal DAG, constraint engine

## My Current Level
- Comfortable with: Python classes, OOP, generators, type hints, FastAPI, PostgreSQL, async, multiprocessing
- Learning: algorithms, graph data structures, formal logic
- Built so far: multi-format data pipeline, canonicalizer with SHA-256 hashing, audit log, API with job system
-Implemented hash tables, BFS, DFS, topological sort, levenshtein distance, jaccard similarity once 

## Response Format
- Keep responses short. One hint per message unless I ask for more.
- Don't explain concepts I didn't ask about.
- Don't praise me or tell me I'm doing well. Be neutral.
- If my code works and is clean, just say "works, move on" and tell me the next step.

----

the current learning roadmap I'm following :



HOW ALGORITHMS ARE LEARNED ON THIS ROADMAP
Every algorithm on this roadmap is learned for a reason connected to MachineACS. The goal is never "memorize this algorithm." The goal is "build the reasoning pattern that this algorithm teaches, because that pattern appears in the product."
Algorithms fall into three categories, and each category demands a different learning approach.

Category 1: The reasoning is the lesson.
These are algorithms where understanding why they work matters more than being able to reproduce the code. The mental model — the insight that makes the algorithm correct — is the thing you're acquiring. If you read a reference implementation first, you'll be able to reproduce it from memory, but you won't have built the mental model that lets you apply the same reasoning to a new problem you've never seen before.
Approach: Read a plain-English explanation or watch a visual walkthrough. No code. Understand what the algorithm does, what the key insight is, and why the approach works. Then close everything and implement from that conceptual understanding. When stuck, trace through a small example by hand on paper before looking at anything. The struggle of translating your understanding into working code is where the learning happens. If after a hand trace you're stuck on a specific Python mechanics issue (not the algorithm logic), look up that one detail and return to your own implementation. Never read a complete reference implementation and then reproduce it.
Algorithms in this category: Levenshtein distance (all three versions — the brute force teaches recursion as problem decomposition, the memoized version teaches caching redundant work, the tabulated version teaches bottom-up construction from subproblems), binary search (the reasoning pattern of halving the search space), BFS and DFS (queue versus stack, level-by-level versus depth-first — these are the traversal primitives for the HIG and the causal DAG), topological sort via Kahn's algorithm (the reasoning pattern of iteratively removing nodes with no dependencies — this is directly how the convergence loop determines evaluation order), the Datalog forward chainer (the fixpoint reasoning pattern — repeatedly apply rules until nothing changes — this is the core of the CCE), unification (matching patterns against facts with variable bindings — this is how the query engine works), and the recursive descent parser (grammar rules mapping directly to recursive function calls — this is the foundation of the rule engine and the YAML compiler).
Why this category matters for MachineACS: These algorithms aren't implemented once and forgotten. Their reasoning patterns recur throughout the product. The dynamic programming reasoning from Levenshtein appears again in the correction engine (minimum-cost repair path). The BFS/DFS reasoning appears in the HIG traversal and causal DAG analysis. The fixpoint reasoning from the forward chainer appears in the convergence loop. If you memorized the code without acquiring the reasoning, you'd fail to recognize these patterns when they reappear in a different context.

Category 2: The technique is the lesson.
These are algorithms with a specific clever trick that you're unlikely to derive independently from first principles. The trick itself is worth learning — trying to reinvent it from scratch would take days and wouldn't teach proportionally more than studying the technique and then implementing it yourself.
Approach: Read the algorithm description including pseudocode or a clear code walkthrough. Understand each step and why it's there. Trace through a small example by hand to verify your understanding. Then close the reference and implement from your understanding. You'll remember the overall structure but forget specific details — those moments of "wait, how did that step work" are where understanding solidifies. The distinction from Category 1 is that you're not expected to derive the technique independently, but you are expected to implement it yourself after learning the idea.
Algorithms in this category: Dijkstra's algorithm (the min-heap priority queue trick for efficient shortest-path computation — you wouldn't naturally arrive at this from "find shortest paths" without exposure to the technique), Bron-Kerbosch with pivoting (the backtracking approach to clique detection with the pivot optimization that prunes the search space), Bloom filters (the multiple independent hash functions technique for probabilistic set membership with zero false negatives), union by rank in Union-Find (you might figure out path compression intuitively but the rank-based balancing optimization is non-obvious), and Soundex or Double Metaphone phonetic encoding (arbitrary encoding tables derived from linguistic research that you need to look up, not derive).
Why this category matters for MachineACS: These techniques solve specific performance or capability problems in the product. Dijkstra enables weighted traversal of the HIG. Bloom filters enable blocking in entity resolution. Union-Find with rank keeps the clustering pipeline fast. You need to understand them well enough to know when to apply them and what their tradeoffs are, but you don't need to have independently discovered them.

Category 3: The implementation is the lesson.
These are algorithms where the concept is simple to explain in one sentence but getting the implementation correct requires careful engineering. The edge cases, the failure modes, and the subtle bugs are the actual learning content. Reading a reference implementation would rob you of encountering these difficulties yourself.
Approach: Read a one-paragraph conceptual explanation. Understand the idea at a high level. Then immediately start building. Don't read reference code. When you hit a difficulty (and you will), think about it for 15–20 minutes. If you can't resolve it, search for that specific issue (not a complete implementation). Read just enough to unblock yourself, then return to your code. The bugs you encounter and fix are the lesson.
Algorithms in this category: Hash table with open addressing (the concept is simple — hash the key, store in a slot, probe on collision. But getting deletion right with tombstone markers, handling the load factor, and avoiding infinite probe loops is where the real understanding forms), the lexer (the concept is "scan characters and emit tokens" but handling multi-character operators, string literals, whitespace, and error reporting correctly is the hard part), the AST evaluator (the concept is "walk the tree recursively" but type mismatches, missing fields, and operator precedence are the real challenges), the convergence loop (the concept is "run all three layers until stable" but correction propagation, termination detection, and the monotonicity invariant are where the engineering difficulty lives), and the proof tracer (the concept is "record which rules fired" but ensuring the trace is complete, correctly ordered, and linked to the right records requires careful state management).
Why this category matters for MachineACS: These are the components that become your product. The hash table teaches you the engineering discipline of handling edge cases that the algorithm description doesn't mention. That discipline is what you apply to every module in MachineACS — the canonicalizer, the entity resolver, the constraint engine. A system that claims deterministic correctness cannot have unhandled edge cases. Category 3 algorithms are where you build the habit of asking "what input would break this" before you consider the implementation complete.

The verification step (applies to all three categories):
After your implementation works and passes your own test cases, compare it to a reference implementation. Not to check that your code looks the same — there are many valid implementations of every algorithm. Compare to check: did you miss edge cases the reference handles? Is there a more efficient approach to a specific step? Does the reference use a data structure choice you didn't consider? The differences between your version and the reference are where the deepest learning happens.
The one-sentence rule:
If the algorithm teaches you a way of thinking, reconstruct it from the concept alone. If the algorithm teaches you a specific technique, learn the technique then implement it yourself. If the algorithm is conceptually simple but implementation-tricky, just start building and learn from the bugs.


⭐ MASTER ROADMAP v2.0
Stage 0 → Stage 11.5
From "beginner coder" → "founder capable of building and deploying the Causal Constraint Engine as a product"

STAGE 0 — FOUNDATIONS
Status: DONE
Skills coming in: Basic Python — variables, loops, functions, conditionals, very basic regex, basic file I/O, pathlib basics, small single-file scripts.
Skills acquired: Variables, loops, functions, basic string manipulation, FileNotFoundError handling, simple regex, pathlib basics, minimal error handling.
▶ v0.1 — First Script ✅
Build a whitespace cleaner, uppercase removal, basic regex substitution. Single-file script using open().
▶ v0.2 — Improved Single Script ✅
Improved regex cleaning, spellchecker integration, more robust file paths with pathlib, simple try/except around file loading.
Output of Stage 0: You can build and modify a text cleaner quickly. You understand Python syntax but not software architecture.

STAGE 1 — DEEP PYTHON PROGRAMMER
Single-Script → Multi-File Engineer
Status: DONE
Skills coming in: Stage 0 complete. You write working Python but everything lives in one file. No understanding of modules, packages, testing, or project structure.
Skills acquired: Multi-file architecture, imports, packages, splitting responsibilities across files, utility modules, config-driven architecture, pytest basics, automated verification, logging basics.
▶ v0.3 — Modular Text Cleaner ✅
Spec: Restructure the single-file cleaner into a proper project: main.py, cleaner.py, filters/, utils/, config/. Each module has one responsibility. main.py orchestrates. filters/ contains individual cleaning functions. config/ contains a settings file that controls which filters run.
Preconditions: Working v0.2 script. Postconditions: Running python main.py produces identical output to v0.2. No logic lives in main.py — it only calls functions defined elsewhere. Every filter is importable independently.
▶ v0.4 — Add Testing + Configurable Pipeline ✅
Spec: Add a config file (YAML or JSON) that lists which filters to apply and in what order. Add pytest tests that verify each filter individually and the full pipeline end-to-end. Add basic logging with Python's logging module.
Preconditions: v0.3 modular structure working. Postconditions: pytest runs with zero failures. Adding or removing a filter requires only a config change, not a code change. Log output shows which filters ran and in what order.

STAGE 2 — DATA ENGINEER BASICS
Pipelines + Multi-Format Reading
Status: DONE
Skills coming in: Stage 1 complete. You can structure a multi-file Python project. You understand imports, packages, config files, and pytest. You cannot yet read CSV or JSON, handle streaming data, build a CLI, or use classes.
Skills acquired: CSV and JSON parsing, generator functions and yield, iterators, functional pipeline thinking, argparse and CLI design, Object-Oriented Programming (classes, inheritance, methods, self), end-to-end pipeline design, structured reports.
▶ v0.5 — Multi-Format Input Adapters ✅
Spec: Build adapter functions that can read Text, CSV, and JSONL files. Each adapter takes a file path and returns an iterable of records. The rest of the pipeline doesn't know or care which format the data came from.
Preconditions: v0.4 working. Postconditions: read_csv("data.csv"), read_jsonl("data.jsonl"), and read_text("data.txt") all return iterables of dicts with identical structure. Pipeline runs identically regardless of input format.
▶ v0.6 — Memory-Safe Streaming Pipeline ✅
Spec: Rewrite the pipeline to process records one at a time using Python generators. No stage loads the entire file into memory. Each stage yields one processed record before requesting the next.
Preconditions: v0.5 adapters working. Postconditions: Memory usage stays constant regardless of file size. Processing a 1GB file uses the same memory as processing a 1KB file. Verified by watching memory usage during a large file run.
▶ v0.7 — CLI Interface ✅
Spec: Build a unified command-line interface: machineacs -f data.csv -s whitespace. Uses argparse. Validates that the file exists before processing. Validates that the specified strategy is a known filter. Prints a clear error message and exits with code 1 on invalid input.
Preconditions: v0.6 streaming pipeline working. Postconditions: machineacs --help prints usage. Invalid file path prints error and exits 1. Invalid strategy prints error with list of valid strategies and exits 1. Valid input processes file and prints summary.
▶ v0.8 — The OOP Refactor ✅
Spec: Refactor the functional adapters into classes. Create a BaseAdapter class with an abstract read() method. Create CSVAdapter and JSONAdapter that inherit from BaseAdapter and implement read(). The pipeline uses the adapter through the base class interface, not the concrete class.
Preconditions: v0.7 CLI working. You understand functions but not classes. Postconditions: CSVAdapter("file.csv").read() and JSONAdapter("file.jsonl").read() both return iterables of dicts. Adding a new format requires only creating a new class that inherits from BaseAdapter, with no changes to the pipeline code.
Why this stage exists: You cannot use FastAPI (Stage 3) without understanding classes, because FastAPI's request models, response models, and dependency injection are all class-based.
▶ v1.0 — First Real Product ✅
Spec: Combine all previous work into a stable, configurable pipeline. Multi-format input, configurable filter chain, CLI interface, structured output reports showing what was cleaned and why.
Preconditions: v0.8 OOP refactor working. Postconditions: A non-developer can run machineacs -f data.csv and receive a cleaned file plus a human-readable report of all changes made.

STAGE 2.5 — PRODUCTION STANDARDS
Status: DONE
Skills coming in: Stage 2 complete. You have a working multi-file Python project with OOP, CLI, and streaming. You have no dependency management, no type safety, no code formatting enforcement, and no parallelism.
Skills acquired: Dependency management with uv, type hints and mypy strict mode, generator typing, linting and formatting with ruff, pre-commit hooks, multiprocessing with ProcessPoolExecutor, pure function design for parallelism, wall time vs CPU time benchmarking.
▶ v0.9a — Dependency Management ✅
Spec: Initialize the project with uv. Define production dependencies (ijson) separate from development dependencies (pytest) in pyproject.toml. Define a script entry point so machineacs runs from the terminal instead of python main.py. Generate and commit uv.lock.
Preconditions: v0.8 working. Postconditions: Cloning the repo on a fresh machine and running uv sync installs everything needed. machineacs command works after install. No dependency is installed that isn't in pyproject.toml.
▶ v0.9b — Static Typing ✅
Spec: Add type hints to every function in the codebase. Type the Token system with TypedDict. Type all generator functions with Generator[Token, None, None]. Configure mypy in strict mode: disallow_untyped_defs = true.
Preconditions: v0.9a done. Postconditions: mypy --strict . passes with zero errors. Every function signature declares its input types and return type. The complex nested iterator in clean_line is correctly typed.
▶ v0.9c — Linting and Formatting ✅
Spec: Configure ruff for PEP 8 formatting and import sorting. Install pre-commit hooks that run ruff on every commit.
Preconditions: v0.9b done. Postconditions: It is impossible to commit code that violates the style rules. All imports are sorted (stdlib → third-party → local).
▶ v0.9d — Parallel Computing ✅
Spec: Refactor cleaning functions to be pure and picklable (stateless, defined at module top level). Replace the sequential processing loop with ProcessPoolExecutor.map() to distribute data chunks across all available CPU cores.
Preconditions: v0.9c done. Postconditions: os.cpu_count() cores are utilized during processing. Benchmark shows wall time improvement proportional to core count. CPU time (total across all cores) is approximately equal to or slightly higher than single-threaded time, proving the work was distributed, not duplicated.
▶ v0.9e — CI/CD Pipeline (NEW)
Spec: Set up GitHub Actions that runs on every push to main and on every pull request. The pipeline runs: pytest (all tests must pass), mypy --strict (zero errors), ruff check (zero violations). If any step fails, the push is blocked.
Preconditions: v0.9a through v0.9d done. Postconditions: No code reaches main that fails tests, type checks, or linting. Every commit on main is verified. Badge in README shows build status.
Why this stage exists: Without CI, regression bugs accumulate silently. Every stage from here forward adds complexity, and manual testing alone will miss regressions. This is a one-day task that prevents weeks of debugging later.

STAGE 3 — BACKEND ENGINEER BASICS
APIs + Uploads + Jobs
Status: DONE
Skills coming in: Stage 2.5 complete. You have a typed, tested, parallel CLI tool. You have never built a web API, used a database, or handled file uploads programmatically.
Skills acquired: FastAPI basics, Pydantic models, POST file uploads, async basics with asyncio and aiofiles, background task processing, job state management, SQL basics (SELECT, INSERT, UPDATE), PostgreSQL connections, atomic state management, file routing, content-disposition headers, API key security.
▶ v1.05 — Asynchronous Ingestion ✅
Spec: Implement async file loading using asyncio and aiofiles. Write an async def load_file(path) function. Use asyncio.gather() to load 50+ files simultaneously. Build a hybrid hand-off that passes async-loaded data to the ProcessPoolExecutor from v0.9d for CPU-bound cleaning.
Preconditions: Stage 2.5 complete. Postconditions: Loading 1GB of small CSVs with asyncio.gather() is measurably faster than a sequential for loop. Benchmark documents the difference.
▶ v1.1 — Basic FastAPI Server ✅
Spec: Set up a FastAPI application. Define a POST /upload-file endpoint that accepts an UploadFile. Define a Pydantic model for the response. Return a JSON confirmation with filename, size, and upload timestamp.
Preconditions: v1.05 done. OOP from Stage 2 is prerequisite for Pydantic models. Postconditions: curl -X POST -F "file=@data.csv" http://localhost:8000/upload-file returns a JSON response with the file metadata.
▶ v1.2 — Job System ✅
Spec: User uploads a file and receives a Job ID immediately. A background task processes the file. GET /job/{id} returns the current status (pending, processing, complete, failed).
Preconditions: v1.1 done. Postconditions: Upload returns immediately with a job ID. Polling the job endpoint shows status progression from pending → processing → complete. If processing fails, status shows failed with an error message.
▶ v1.2.5 — The Persistence Layer (PostgreSQL) ✅
Spec: Replace any file-based status tracking with a PostgreSQL database. Create a jobs table with columns: id (UUID), status (enum), filename (text), created_at (timestamp), updated_at (timestamp). All status updates go through SQL transactions.
Preconditions: v1.2 done. Postconditions: Job status survives server restart. Two concurrent requests cannot corrupt job state (verified by running two uploads simultaneously). Database state is the single source of truth for job status.
▶ v1.3 — Downloadable Output ✅
Spec: After processing completes, the cleaned file is stored in /tmp/jobs/{job_id}/. GET /job/{id}/download returns the cleaned file with correct Content-Disposition headers.
Preconditions: v1.2.5 done. Postconditions: Browser downloads the file with the correct filename. File content matches the expected cleaned output.
▶ v2.0 — Full API MVP ✅
Spec: Stable upload → clean → download loop. Structured API responses with consistent error format. Minimal security via API key in request headers. All endpoints documented via FastAPI's auto-generated OpenAPI spec.
Preconditions: v1.3 done. Postconditions: A user with an API key can upload a file, poll for completion, and download the result. Requests without a valid API key return 401. /docs shows the full API specification.

🏗️ PHASE A: THE MECHANIC
Foundations of Determinism and Structure

STAGE 4 — DETERMINISTIC FOUNDATIONS
The Science of Stability
Status: PARTIALLY DONE (items 1–5 complete, 6–10 remain)
Skills coming in: Stage 3 complete. You have a working API with PostgreSQL. You understand Python data structures, serialization, and file I/O. You have not yet thought about byte-level determinism, hashing, or content-addressed identity.
Skills acquired: Byte-level determinism, UTF-8 encoding contracts, Unicode normalization (NFC), type coercion policies, null handling policies, floating-point determinism strategies, stable hashing with hashlib, content-addressed identity (the git model for data), lexicographical ordering, deterministic audit trails with hash chains.
Reading before this stage: None required beyond what you already know. This is engineering discipline, not theory.
Concepts 1–5 ✅
Bytes and serialization — json.dumps() output depends on dict insertion order. sort_keys=True makes it deterministic. Verified that it works recursively on nested dicts.
The encoding contract — hashlib.sha256 takes bytes, not strings. "hamza".encode("utf-8") and "hamza".encode("utf-16") produce completely different bytes. UTF-8 is enforced explicitly everywhere.
Unicode normalization — "café" (single code point) and "café" (e + combining accent) look identical but are different bytes. unicodedata.normalize('NFC', string) collapses all equivalent representations before hashing.
Type coercion policy — {"age": 16} and {"age": "16"} are different bytes. The canonicalizer applies a defined type normalization rule before serialization.
Null and empty value handling — {"name": "hamza", "city": null} vs {"name": "hamza"}. Policy defined and enforced: nulls are stripped before canonicalization.
Concepts 6–10 (remaining)
Floating point determinism — 0.1 + 0.2 == 0.30000000000000004. Define one rule: either round to N decimal places or convert to fixed-point integer representation (e.g., salary in cents not dollars) before hashing.
Stable hashing — Python's built-in hash() is randomized per process. hashlib.sha256 is stable across machines, processes, and Python versions. Non-negotiable for auditable systems.
Content-addressed identity — Record IDs are derived from content, not assigned arbitrarily. Same content = same ID. Changed content = changed ID. This is the git model applied to data records.
Lexicographical ordering — One consistent key-sorting rule across the entire system, including whether keys are lowercased before sorting.
The audit log — Once hashing is deterministic, every transformation is traceable: Hash(input) → rules_applied → Hash(output).
▶ v3.0 — The Canonicalizer ✅
Spec: Implement a Canonicalizer class. Given any Python dict, it produces a canonical byte string that is identical for any two dicts with the same content, regardless of key insertion order, type representation, null handling, or Unicode encoding. The canonical form is then hashed with SHA-256 to produce a content-addressed ID.
Preconditions: Concepts 1–9 understood and implemented as utility functions. Postconditions: canonicalize({"b": 2, "a": 1}) produces identical bytes to canonicalize({"a": 1, "b": 2}). canonicalize({"age": 16}) produces identical bytes to canonicalize({"age": "16"}) (after type coercion). The SHA-256 hash of the canonical form is the record's ID. Two identical records always produce the same ID. Any change to any field produces a different ID. Invariant: The canonicalization function is idempotent — canonicalizing an already-canonical record produces identical output.
▶ v3.1 — The Audit Log ✅
Spec: Every cleaning action produces a deterministic trace: Hash(input_record) → [list of rules applied with parameters] → Hash(output_record). The trace is stored in PostgreSQL. Given a record's current hash, the full history of transformations that produced it can be reconstructed.
Preconditions: v3.0 canonicalizer working. Postconditions: Every transformation is recorded with: input hash, output hash, rule ID, rule parameters, timestamp. Given any output hash, the system can walk backward through the chain to the original input. The chain is tamper-evident — modifying any intermediate record breaks the hash chain. Known gap: The "rules applied" field is not yet populated with structured rule metadata. This is resolved in Stage 10 when the proof tracer is built.

STAGE 4.5 — THE CHAOS TEST (NEW)
Battle-Testing Against Real Dirty Data
Skills coming in: Stage 4 complete. Canonicalizer and audit log working. All prior stages passing CI.
Skills acquired: Debugging real-world encoding issues, handling mixed delimiters, surviving malformed records, building resilience into the pipeline, understanding the gap between unit tests and production reality.
Reading before this stage: None. This is pure engineering confrontation with messy reality.
▶ v3.5 — The Chaos Test
Spec: Obtain a real messy dataset. The Dedupe.io sample datasets are publicly available and realistically dirty. Also construct a synthetic "nightmare file" that contains: mixed UTF-8 and Latin-1 encoding within the same file, fields containing commas inside quoted strings, records spanning multiple lines, timestamps in at least five different formats within the same column, null values represented as "NULL", "null", "N/A", "", "None", and " " (single space), numeric fields containing currency symbols and thousand separators ("$1,234.56"), names with Unicode characters from multiple scripts.
Run the full pipeline (ingestion → canonicalization → hashing → audit log) against this data. Document every failure. Fix every failure. Add a regression test for each fix.
Preconditions: v3.1 audit log working. CI pipeline from v0.9e running. Postconditions: The pipeline processes the nightmare file without crashing. Every record receives a canonical hash. Every encoding issue is resolved deterministically (not silently dropped). A test file test_chaos.py contains one test case for each failure mode discovered, ensuring these issues never regress.

STAGE 5 — ENTITY RESOLUTION PRIMITIVES
Skills coming in: Stage 4.5 complete. Python functions, loops, conditionals, recursion basics, basic string manipulation, understanding of function call stacks, Big O notation at a surface level (knowing O(n) is better than O(n²)).
Skills acquired: Recursion as a problem-solving strategy, memoization, dynamic programming (bottom-up tabulation), 2D array construction and indexing, set theory basics (union, intersection, cardinality), complexity analysis (understanding why O(3^n) is catastrophic and O(m×n) is acceptable), binary search, hash table internals (open addressing, linear probing), graph traversal (BFS and DFS), topological ordering (Kahn's algorithm), O(N²) complexity made visceral, wall time benchmarking, operation counting.
Reading before this stage:
Watch Reducible's "What is an Algorithm?" video before starting v4.0.
Read the Ditto paper (Deep Entity Matching with Pre-Trained Language Models) before v4.1. Understand where production entity resolution is and where your naive version sits on that spectrum.
▶ v4.0 — The Comparator
Spec: Implement four similarity functions from scratch in machineacs/comparators/metrics.py. No libraries, no reference code during implementation.
levenshtein_brute_force(s1, s2) — Pure recursive implementation. For each position, recursively try insert, delete, and substitute. Returns the minimum edit distance. This will be extremely slow on strings longer than ~15 characters.
levenshtein_memo(s1, s2, memo=None) — Same logic, but cache results in a dict keyed by (i, j) position pairs. Demonstrate that this reduces redundant computation by comparing call counts.
levenshtein_tabulated(s1, s2) — Bottom-up dynamic programming. Build a 2D grid of size (len(s1)+1) × (len(s2)+1). Fill it iteratively. Return the value at grid[len(s1)][len(s2)]. This is O(m×n) time and space.
jaccard_similarity(s1, s2) — Tokenize both strings on whitespace. Compute |intersection| / |union|. Returns a float between 0.0 and 1.0.
Preconditions: Python functions, loops, recursion basics. Postconditions: levenshtein_tabulated("horse", "ros") returns 3. jaccard_similarity("data science", "data engineering") returns a float between 0 and 1. All three Levenshtein implementations return identical results for any input pair. Brute force is measurably slower than tabulated on strings of length 15+.
▶ v4.0b — The Algorithms Module
Spec: Implement five fundamental algorithms from scratch in machineacs/comparators/algorithms.py. For each: one comment stating Big O complexity and one sentence explaining why that complexity holds.
binary_search(arr, target) — Iterative. Returns index or -1. Comment: O(log n) because each comparison halves the remaining search space.
DONE
HashTable class — insert(key, value), get(key), delete(key). Uses open addressing with linear probing. No Python dict used internally — use a fixed-size list of slots. Handle collisions by probing to the next open slot. Handle deletion with tombstone markers.
DONE
bfs(graph, start) — Takes an adjacency list dict, returns nodes in BFS order. Uses a queue (collections.deque).
DONE
dfs(graph, start) — Same input format, returns nodes in DFS order. Uses an explicit stack (not recursion, to avoid stack overflow on large graphs).
DONE
topological_sort(graph) — Kahn's algorithm. Takes a DAG as adjacency list, returns a list of nodes in topological order. Raises ValueError if a cycle is detected (in-degree never reaches 0 for all nodes).
DONE
Preconditions: Python lists, dicts, classes. Basic OOP. Conceptual understanding of what a graph is. Postconditions: topological_sort({"a": ["b"], "b": ["c"], "c": []}) returns ["a", "b", "c"]. HashTable passes 10 insert/get/delete cycles without collision errors on a table with load factor > 0.7. bfs and dfs return correct traversal orders on a graph with at least 20 nodes.
▶ v4.1 — The Naive Deduplicator
Spec: Add a CLI command: machineacs dedupe --threshold 0.8 --file dirty_hr_data.jsonl. Load all records. Compare every pair using levenshtein_tabulated. If normalized similarity (1 - distance/max_length) >= threshold, flag as a duplicate pair. Print all duplicate pairs and total wall time. Run on a 10,000-line CSV and document the hang.
Preconditions: v4.0 comparator functions working. argparse from Stage 2. PostgreSQL from Stage 3. Postconditions: Output lists all duplicate pairs above threshold. Wall time on 10,000 records is documented (expect 5–15 minutes). Comment in code states: "N=10,000 produces N×(N-1)/2 = 49,995,000 comparisons. This grows quadratically — doubling N quadruples runtime."

STAGE 6 — GRAPH DATA STRUCTURES
From Tables to Networks
Skills coming in: Stage 5 complete. Comparator and algorithms modules working. BFS, DFS, and topological sort implemented. Python classes and OOP basics solid. PostgreSQL basics.
Skills acquired: Adjacency list representation, BFS-based connected components, Union-Find with path compression and union by rank, amortized complexity analysis (α(n)), benchmarking competing implementations, pipeline composition (connecting system outputs as inputs), cluster persistence in a relational database, property-based testing with Hypothesis.
Reading before this stage:
Tarjan's original Union-Find paper. Short and dense. Your first primary source.
Begin Kleppmann "Designing Data-Intensive Applications" chapters on storage and retrieval (understanding how PostgreSQL stores your graph data internally).
▶ v5.0 — The Graph Engine
Spec: Build a Graph class in machineacs/graph/engine.py with: add_node(id), add_edge(a, b), neighbors(id). Internal representation is an adjacency list (dict of node_id → set of neighbor_ids).
Build bfs_connected_components(graph) — returns a dict mapping every node_id to a component_id. Uses BFS from each unvisited node, assigning all reachable nodes the same component_id.
Build a UnionFind class: union(a, b), find(a) with path compression, union by rank, components() returning a dict of component_id → set of node_ids.
Benchmark both on a 10,000-node graph with ~30,000 random edges. Document wall time difference.
Preconditions: BFS and DFS from v4.0b working. Postconditions: Graph with nodes [1,2,3,4,5] and edges [(1,2),(2,3),(4,5)] produces two components: {1,2,3} and {4,5}. Both implementations agree on component assignments for all test cases. Comment explains: BFS components is correct when the graph is static and fully constructed; UnionFind is correct when edges arrive incrementally and you need dynamic connectivity.
▶ v5.0p — Property-Based Testing Introduction (NEW)
Spec: Install the Hypothesis library. Write property-based tests for the Graph engine and UnionFind.
Properties to verify:
Symmetry: If union(a, b) is called, then find(a) == find(b).
Transitivity: If find(a) == find(b) and find(b) == find(c), then find(a) == find(c).
Idempotency: Calling union(a, b) twice produces the same state as calling it once.
Agreement: For any randomly generated graph, bfs_connected_components and UnionFind.components() produce identical component groupings.
Use @given(st.lists(st.tuples(st.integers(0, 100), st.integers(0, 100)))) to generate random edge lists.
Preconditions: v5.0 Graph engine and UnionFind working. Postconditions: All property tests pass on 1000+ randomly generated inputs. Any property failure is investigated and fixed before proceeding.
Why this stage exists: Property-based testing verifies invariants hold for all possible inputs, not just the examples you thought of. From this point forward, every module should have property-based tests alongside example-based tests. This is the practical foundation for your system's correctness claims.
▶ v5.1 — The Clustering Pipeline
Spec: Load records from PostgreSQL. For every pair, compute levenshtein_tabulated similarity. If similarity >= threshold, call union(record_a_id, record_b_id). After all pairs are processed, call components() and write cluster assignments back to PostgreSQL. Add a cluster_id column to the records table.
CLI: machineacs cluster --threshold 0.8 --file dirty_hr_data.jsonl
Preconditions: v5.0 graph engine working. PostgreSQL from Stage 3. Postconditions: Every record in the database has a cluster_id. Records in the same cluster have pairwise similarity >= threshold. Records in different clusters have pairwise similarity < threshold (within the transitivity closure of the threshold graph).

STAGE 7 — LOGIC AND AST FOUNDATIONS
Separate the WHAT from the HOW — Rules Should Be Data, Not Code
Skills coming in: Stage 6 complete. Python AST module basics (knowing ast.parse() exists). String manipulation and tokenization intuition from regex work. OOP — classes, inheritance, method dispatch. Property-based testing with Hypothesis.
Skills acquired: Lexing (scanning strings into typed tokens), recursive descent parsing, AST construction, the Visitor pattern, why eval() is a security vulnerability, grammar extension, operator precedence, test-driven development.
Reading before this stage:
Velleman "How to Prove It" — propositional logic chapter must be complete.
Aaronson "Why Philosophers Should Care About Computational Complexity" — read before v6.1.
▶ v6.0 — The Safe Rule Engine
Spec: Build a rule evaluation system in machineacs/rules/engine.py that takes a rule string and a record dict and returns True or False. No eval() anywhere.
Lexer: tokenize(rule_string) → list of typed tokens. Token types: NUMBER, STRING, IDENTIFIER, OPERATOR (==, !=, >=, <=, >, <), LPAREN, RPAREN, AND, OR.
Parser: parse(tokens) → AST. Each node is one of: ComparisonNode(field, operator, value), BinaryOpNode(left, operator, right), LiteralNode(value).
Evaluator: NodeVisitor class with visit(node, record) method. Recursively walks the AST, looks up field values in the record dict, evaluates comparisons, combines with AND/OR logic.
Preconditions: Stage 6 complete. Velleman propositional logic chapter done. Postconditions: Rule "age >= 18 AND is_active == true" returns True for {"age": 25, "is_active": True} and False for {"age": 15, "is_active": True}. Rule with unknown field raises a RuleEvaluationError, not a KeyError. Empty rule string raises a ParseError.
▶ v6.1 — Compound Rules
Spec: Extend the lexer and parser to handle operator precedence: AND binds tighter than OR. Nested parentheses override precedence.
Rule "age >= 18 OR department == Engineering AND is_active == true" must parse as "age >= 18 OR (department == Engineering AND is_active == true)", not "(age >= 18 OR department == Engineering) AND is_active == true".
Write 20 pytest tests covering: empty strings, type mismatches (comparing a string field to a number), nested parentheses three levels deep, deeply nested AND/OR chains, missing fields in record, rules with only one condition, rules with string values containing spaces.
Preconditions: v6.0 working. Postconditions: All 20 tests pass. Precedence is correct for all combinations. Property-based test: for any randomly generated record and valid rule, the evaluator either returns a boolean or raises a RuleEvaluationError — it never crashes with an unhandled exception.

STAGE 7.5 — THE DATALOG ENGINE
The Most Important Stage on the Roadmap
Skills coming in: Stage 7 complete — lexer, parser, and AST evaluator all working. Velleman chapters on logic and sets complete — you understand predicates, Horn clauses, and fixpoint informally. Topological sort implemented. Python generators solid. Property-based testing with Hypothesis.
Skills acquired: Horn clause logic, fixpoint semantics, unification with variable bindings, bottom-up evaluation (forward chaining), the difference between Datalog and Prolog (termination guarantee), deductive database fundamentals.
Reading before writing a single line:
Ramakrishnan and Ullman "A Survey of Deductive Database Systems." This is mandatory. Do not start coding before reading it.
Begin Abiteboul/Hull/Vianu "Foundations of Databases" — Datalog and fixpoint chapters.
▶ v6.5 — Naive Datalog Engine
Spec: Build a complete Datalog evaluation engine in machineacs/logic/datalog.py.
FactStore class: add_fact(predicate, *args) stores a ground fact. query(predicate, *args) returns all matching tuples, where args can be constants (lowercase strings) or variables (uppercase strings). Variables match any value and return bindings.
Rule class: A rule has a head (predicate + argument pattern) and a body (list of predicate + argument patterns). Example: ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y) has head ancestor(X, Y) and body [parent(X, Z), ancestor(Z, Y)].
Parser: Reads Datalog syntax strings into Rule and Fact objects. Facts end with . and rules use :- to separate head from body.
ForwardChainer: run() applies all rules to current facts, derives new facts by matching rule bodies against the fact store using unification, adds derived facts to the store, and repeats until no new facts appear (fixpoint reached). Returns the number of iterations.
QueryEngine: query(predicate, *args) returns all matching fact tuples with variable bindings substituted.
Location: machineacs/logic/datalog.py
30 pytest tests minimum plus property-based tests:
Property: running ForwardChainer.run() twice in a row produces zero new facts on the second run (fixpoint is stable).
Property: for any set of facts and rules with no negation, the engine terminates.
This must work end to end:
parent(tom, bob).
parent(bob, ann).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
?- ancestor(tom, ann).  → True
?- ancestor(tom, X).   → [bob, ann]

Preconditions: Stage 7 complete. Ramakrishnan and Ullman read. Postconditions: The ancestor query works correctly. The engine terminates on all test inputs. The fixpoint is reached in ≤ N iterations where N is the longest derivation chain.

STAGE 7.75 — THE COMPILER (STREAMLINED)
Understanding the Compilation Pipeline Without Building a Full Language
Skills coming in: Stage 7 complete (lexer, parser, AST evaluator). Stage 7.5 complete (Datalog engine). You understand what a formal language execution engine looks like.
Skills acquired: Complete compilation pipeline understanding (source text → tokens → AST → execution), scoping and environments (variable binding across nested calls), the connection between compilation and the neuro-symbolic translation layer.
Reading for this stage:
Read "Crafting Interpreters" by Robert Nystrom (free at craftinginterpreters.com) — the tree-walk interpreter section (Part II). Read and understand the concepts. You do not need to implement the full Lox language.
▶ v6.75 — The Mini-Interpreter (STREAMLINED)
Spec: Build a minimal interpreter in machineacs/compiler/ that supports: variable declaration and assignment, arithmetic expressions, comparison operators, if/else conditionals, and function definition and calls. This is NOT the full Lox language from Crafting Interpreters — it is a stripped-down version that teaches you the compilation pipeline without the multi-week time investment.
Lexer: Tokenizes a simple language with: var, if, else, fun, return, print, identifiers, numbers, strings, arithmetic operators, comparison operators, braces, parentheses, semicolons.
Parser: Recursive descent. Produces AST nodes for: VariableDeclaration, Assignment, IfStatement, FunctionDeclaration, ReturnStatement, PrintStatement, BinaryExpression, CallExpression.
Environment class: Handles variable scoping. Nested function calls create child environments that can look up variables in parent scopes.
Tree-walk interpreter: Evaluates AST nodes recursively, maintaining the environment stack.
The language must execute:
var x = 10;
if (x > 5) { print x; }
fun double(n) { return n * 2; }
print double(x);

Output: 10 then 20.
Preconditions: Stage 7.5 Datalog engine working. Crafting Interpreters Part II read (not necessarily implemented along the way). Postconditions: The interpreter executes the above program correctly. You can explain how variable scoping works in your implementation. You understand why this compilation pipeline is the same conceptual machinery needed to translate natural language rule descriptions into Datalog predicates.
Why this stage is streamlined: The full Crafting Interpreters build (classes, closures, inheritance, garbage collection) teaches deep language design but adds ~6 weeks and produces an artifact that isn't used in MachineACS. The stripped-down version teaches the essential compilation pipeline concepts in ~2 weeks. The remaining concepts can be studied from the book without full implementation.

STAGE 8 — ADVANCED ENTITY RESOLUTION
Scale Beyond O(N²)
Skills coming in: Stage 5 complete (all comparator functions). Stage 6 complete (graph engine and clustering pipeline). Hash table from v4.0b. Benchmarking skills from v4.1 and v5.0.
Skills acquired: Blocking strategies (phonetic encoding, inverted indexes), probabilistic data structures (Bloom filter), false positive vs false negative tradeoffs, data survivorship strategies, field-level conflict resolution, audit trail for merge decisions.
Reading before this stage:
Bloom's original 1970 paper "Space/Time Trade-offs in Hash Coding with Allowable Errors." Read before v7.1.
▶ v7.0 — The Phonetic Indexer (STREAMLINED)
Spec: Implement a blocking strategy that groups candidate records by phonetic similarity before running Levenshtein comparison. Build a PhoneticIndex class: add(record_id, name) stores a record under its phonetic key, candidates(name) returns all record IDs sharing a phonetic key.
Implementation choice: Implement Soundex from scratch (simpler than Double Metaphone, teaches the same concepts). Use a library for Double Metaphone if you want better quality in production. The learning goal is understanding why blocking reduces O(N²) to near O(N), not memorizing phonetic encoding tables.
Integrate with the clustering pipeline: only run levenshtein_tabulated on candidate pairs sharing a phonetic key.
Preconditions: Stage 5 and 6 complete. Postconditions: Wall time on 10,000 records with blocking is at least 50x faster than without. Comment explains: blocking reduces the comparison space from N² to approximately N × (average block size), which is near-linear when blocks are small.
▶ v7.1 — Bloom Filter
Spec: Build a BloomFilter class: __init__(capacity, false_positive_rate), add(item), might_contain(item). Uses k independent hash functions (derived from two base hashes with the Kirsch-Mitzenmacher technique). Internal storage is a bit array (Python bytearray). No external libraries.
Integrate into the blocking pipeline as a pre-screen: before looking up the phonetic index, check the Bloom filter. If the filter says "definitely not seen," skip the lookup entirely.
Preconditions: v7.0 done. Bloom's paper read. Postconditions: BloomFilter(capacity=10000, fpr=0.01) has a measured false positive rate within 2x of the target. Comment explains: false positives are acceptable because we'll still Levenshtein-check the candidates. False negatives are catastrophic because we'd miss true duplicates. The Bloom filter guarantees zero false negatives.
▶ v7.2 — The Golden Record
Spec: Build a GoldenRecordResolver class that takes a cluster of record dicts (all identified as referring to the same entity) and produces one canonical "golden" record.
Three resolution strategies, selectable per field via config:
most_frequent — use the value that appears most often across the cluster.
longest_string — use the longest non-null value (captures the most complete version).
most_recent — use the value from the record with the latest timestamp.
Store in PostgreSQL: the winning golden record, the strategy used for each field, and the source record IDs that contributed each winning value.
CLI: machineacs resolve --cluster-id <id>
Preconditions: v5.1 clustering pipeline working. PostgreSQL. Postconditions: Every cluster has exactly one golden record. Every field in the golden record has a documented source and strategy. The audit trail can answer: "Why does this golden record say city = Montreal?" → "Because 4 of 5 source records agreed (most_frequent strategy). Dissenting record R3 said Toronto."

STAGE 9 — NETWORK DYNAMICS
Communities and Conflict Resolution via Graph Topology
Skills coming in: Stage 6 complete (Graph class, BFS, Union-Find). Stage 7.5 complete (Datalog engine). Linear algebra track underway (vectors and matrices understood).
Skills acquired: Weighted graph traversal (Dijkstra), directed graph analysis (weakly connected components), clique detection (Bron-Kerbosch), multi-source entity resolution, clique-based truth resolution, full pipeline integration.
Reading before this stage:
Original Louvain community detection paper by Blondel et al. Read before v8.1.
▶ v8.0 — Graph Algorithms Module
Spec: Build in machineacs/graph/algorithms.py:
dijkstra(graph, start) — Weighted adjacency list (dict of node → list of (neighbor, weight) tuples). Returns dict of node → shortest distance from start. Uses heapq as a min-priority queue.
weakly_connected_components(graph) — Directed graph input. Treats edges as undirected for component detection. Returns dict of node → component_id.
find_cliques(graph) — Bron-Kerbosch algorithm with pivoting. Returns list of maximal cliques (each clique is a set of node IDs).
For each: complexity analysis in comments, 10 pytest tests minimum. Property-based test: for any graph, every node appears in exactly one WCC and at least one maximal clique.
Preconditions: Stage 6 graph engine. heapq basics. Postconditions: Dijkstra returns correct shortest paths on a weighted graph with at least 50 nodes. WCC correctly identifies components in a directed graph. Bron-Kerbosch finds all maximal cliques in a graph where the answer is manually verifiable.
▶ v8.1 — The Community Detector
Spec:
EntityCollapser: Uses weakly connected components to assign canonical IDs across data sources. If "John Smith" appears in System A and System B with sufficient similarity, both get one canonical entity ID.
TruthResolver: Given a field with conflicting values across a cluster, uses clique detection to determine which value is supported by the most internally-consistent subgroup. Logic: if 5 records form a clique and agree on city = "Montreal", and 1 outlier says city = "Toronto", trust the clique.
Store canonical ID assignments and truth resolution decisions in PostgreSQL with full audit trail: which records were collapsed, what the conflicting values were, which clique supported the winning value, and why.
Preconditions: v8.0 algorithms working. Full pipeline from Stages 5–6. Postconditions: Cross-source entity resolution produces correct canonical IDs. Truth resolution chooses the clique-supported value. Audit trail documents every decision.

STAGE 10 — CAUSAL INTELLIGENCE
From Association to Intervention
Skills coming in: Stage 7.5 complete (Datalog engine fully working). Stage 9 complete (graph algorithms solid). Probability track underway (Bayes and conditional independence).
Skills acquired: DAG representation and validation, intervention logic (the difference between observation and intervention), counterfactual graph traversal, expressing domain constraints as Datalog rules, proof trace generation, the CCE as a product.
Reading before this stage:
Pearl "The Book of Why" — must be complete.
Pearl "Causality" chapters 1–3 — must be complete.
These are non-negotiable. You cannot build a causal constraint engine without understanding what causality means formally.
▶ v9.0 — The Causal DAG
Spec: Build in machineacs/causal/dag.py.
Load a causal DAG from JSON: {"job_title": ["salary", "department"], "age": ["salary"]} means job_title causally influences salary and department, and age causally influences salary.
CausalDAG class:
add_causal_edge(cause, effect) — adds a directed edge.
downstream(field) — returns all fields causally downstream (transitively).
upstream(field) — returns all fields causally upstream (transitively).
validate() — uses topological sort to verify the graph is acyclic. Raises CyclicCausalGraphError if a cycle exists, reporting the cycle.
InterventionEngine: Given a field that was cleaned (intervened on), returns all downstream fields that are now causally suspect and should be re-validated.
CounterfactualQuery: Given a field, returns all fields causally upstream — the potential causes of the observed value.
Preconditions: Stage 7.5 Datalog engine. Topological sort from v4.0b. Pearl read. Postconditions: Cleaning job_title flags salary and department as suspect. Querying upstream of salary returns job_title and age. A cyclic graph (A → B → C → A) raises an error with the cycle path. Property-based test: for any DAG, downstream(X) never includes X itself (no self-causation).
▶ v9.1 — Causal Rules in Datalog
Spec: Express causal constraints as Datalog rules loaded into the Stage 7.5 engine. This is the CCE MVP.
Example rules:
invalid_salary(E) :- employee(E), job_title(E, "Intern"), salary(E, S), S > 100000.
invalid_promotion(E) :- employee(E), promotion_date(E, Dp), hiring_date(E, Dh), Dp < Dh.
invalid_claim(C) :- claim(C), claim_date(C, Dc), policy_end(C, De), Dc > De.

ProofTracer class: Wraps the ForwardChainer. Records every rule firing with: predicate name, variable bindings, timestamp, and the rule ID that fired. The proof trace is a complete derivation showing exactly why a record was flagged as invalid.
Store proof traces in PostgreSQL: one row per rule firing, linked to the record being validated.
CLI: machineacs validate --record-id <id> returns the validation result plus the full proof trace.
This is the CCE MVP. This is the product. The proof trace is the commercial value — not just the boolean valid/invalid result, but the certified derivation showing why.
Preconditions: v9.0 Causal DAG working. Datalog engine from Stage 7.5. Postconditions: An intern with salary $200,000 is flagged with a proof trace citing the invalid_salary rule. An employee promoted before being hired is flagged with a proof trace citing invalid_promotion. The proof trace is machine-parseable (JSON) and human-readable (natural language summary).
Reading after v9.1:
Scallop — "From Probabilistic Deductive Databases to Scalable Differentiable Reasoning." Understand the competing approach of differentiable logic programming.
Dechter "Constraint Processing" first four chapters. This prepares you for the correction engine in the next stage.

STAGE 10.25 — THE CORRECTION ENGINE (NEW)
From Detection to Repair
Skills coming in: Stage 10 complete. CCE MVP working. Proof traces generated. Dechter "Constraint Processing" first four chapters read.
Skills acquired: Field trust hierarchies, minimum-cost constraint repair, correction ambiguity detection, the difference between auto-correction and flagging for human review, constraint optimization basics.
Reading before this stage:
Dechter "Constraint Processing" chapters 1–4 (CSP fundamentals, constraint propagation).
Z3 Python tutorial (weekend project — understand what an SMT solver does).
▶ v9.25 — The Correction Engine
Spec: Build in machineacs/correction/engine.py.
TrustHierarchy class: Configurable per-domain. Maps each field to a trust level (integer 1–10) based on its data source. Example for HR domain: government_id: 10, date_of_birth: 9, legal_name: 8, address: 5, phone: 3, self_reported_title: 2.
CorrectionEngine class: Given a constraint violation (from the proof tracer), proposes a correction. The correction modifies the lowest-trust field involved in the violation to satisfy the constraint.
Three outcomes:
Unambiguous correction: Only one field can be changed to satisfy the constraint. Apply it. Record in audit trail.
Trust-resolved correction: Multiple fields could be changed. The trust hierarchy breaks the tie — modify the lowest-trust field. Record the trust levels and the alternative corrections that were considered.
Ambiguous correction: Multiple fields could be changed and the trust hierarchy doesn't resolve it (tied trust levels, or the correction would create a secondary violation). Do not auto-correct. Flag for human review with: the violation, all candidate corrections, and the proof trace for each.
Preconditions: Stage 10 CCE MVP. Proof traces. Postconditions: A promotion_date before hiring_date violation is corrected by modifying the lower-trust field. The audit trail records: which field was changed, its old and new values, the trust levels, and the constraint that was satisfied. Ambiguous cases are never auto-corrected. Property-based test: for any correction applied, the corrected record passes the constraint that was previously violated, and no new constraint violations are introduced.

STAGE 10.5 — THE CONVERGENCE ENGINE (NEW)
The Core Architectural Innovation
Skills coming in: Stage 10.25 complete. All three layers (canonicalization, entity resolution, constraint validation) independently working. Correction engine working.
Skills acquired: Fixed-point computation across multiple system layers, monotonicity invariants, correction propagation, cross-layer dependency management, termination guarantees.
Reading before this stage:
Knaster-Tarski fixpoint theorem — understand the mathematical foundation for why your convergence loop produces a correct result.
Abiteboul/Hull/Vianu fixpoint chapters (from Pillar 1 reading track).
▶ v9.5 — The Convergence Loop
Spec: Build in machineacs/convergence/engine.py.
Wire the canonicalization engine, entity resolver, and constraint engine into a single iterative loop:
Initial canonicalization runs using only context-free rules (format enforcement, checksum validation, unambiguous alias resolution from the CKG).
Entity resolution runs using canonicalized data plus a designated subset of constraints called pre-constraints — rules that are safe to apply before full causal validation (e.g., "one person, one date of birth").
Full causal validation runs the CCE against the merged, canonicalized dataset. The correction engine applies fixes where unambiguous.
Correction propagation: Any correction applied in step 3 that changes a field used in canonicalization or entity resolution emits a propagation signal. Affected records are re-queued for steps 1 and 2.
Iteration: The loop returns to step 1 with updated records. Steps 1–4 repeat.
Termination: The loop terminates when a pass produces zero new corrections (fixpoint reached) OR when the maximum iteration count is exceeded (safety bound).
The monotonicity invariant: Each pass can only add corrections or confirmations. A previously confirmed result is never reverted. This guarantees convergence — the set of corrections grows monotonically and is bounded by the finite number of fields in the dataset.
Preconditions: Canonicalizer from Stage 4. Clustering pipeline from Stage 6. CCE from Stage 10. Correction engine from Stage 10.25. Postconditions: A synthetic test dataset where a Layer 3 violation forces a Layer 1 re-canonicalization, which triggers a Layer 2 re-merge, converges to a fixpoint in ≤ 5 iterations. The system terminates on all test inputs. The maximum iteration bound prevents infinite loops on adversarial inputs. Property-based test: for any input dataset and rule set, the convergence loop either reaches fixpoint or hits the iteration bound — it never runs forever.
This is the hardest engineering on the entire roadmap. This is where you discover whether your architecture actually works or whether the layers make assumptions about each other that break under iteration.

STAGE 11 — SEMANTIC ARCHITECTURE
Decouple Rules from Execution — Rules Are Data Served via API
Skills coming in: Stage 10.5 complete. Full convergence loop working. Datalog engine, causal DAG, proof tracer, correction engine all integrated. FastAPI from Stage 3. PostgreSQL solid.
Skills acquired: DSL design, API-first architecture, proof trace serialization, structured logging, observability basics, security hardening of input parsing surfaces, performance benchmarking at scale.
Reading before this stage:
Brachman and Levesque "Knowledge Representation and Reasoning" — chapters on knowledge base maintenance.
Study SNOMED CT or FIBO ontology structure for domain onboarding design inspiration.
OWASP Top 10 — read before building the API.
▶ v10.0 — The Headless Semantic Layer
Spec: Build the production API that exposes the full MachineACS pipeline.
YAML Rule Format: Domain rules are defined in YAML files:
valid_employee:
  domain: "hr"
  constraint_type: "hard"
  rules:
    - "age >= 18"
    - "salary > 0"
    - "department != null"
  trust_hierarchy:
    government_id: 10
    date_of_birth: 9
    legal_name: 8
    address: 5

YAMLCompiler: Reads YAML, compiles each rule string into Datalog facts and rules, loads into engine at startup. Validates that the rule set is internally consistent (no two hard constraints can both fire on the same record and require contradictory corrections). Reports conflicts at load time, not at evaluation time.
API Endpoints:
POST /validate — Accepts a record dict. Runs through the full convergence loop (canonicalization → entity resolution → constraint validation → correction). Returns:
{
  "valid": false,
  "violations": ["invalid_salary"],
  "corrections_applied": [
    {
      "field": "salary",
      "old_value": 200000,
      "new_value": null,
      "reason": "Flagged for review: intern salary exceeds constraint",
      "rule_id": "invalid_salary",
      "trust_level": 2
    }
  ],
  "proof_trace": [...],
  "input_hash": "sha256:abc...",
  "output_hash": "sha256:def...",
  "convergence_iterations": 2,
  "timestamp": "2028-01-15T14:30:00Z"
}

GET /rules — Returns all active rules in human-readable form, grouped by domain.
GET /audit/{record_id} — Returns full validation and correction history for a record, including every convergence iteration.
POST /rules/validate — Takes a proposed new rule and checks it against all existing rules for conflicts. Returns either "compatible" or a list of conflicting rule pairs with explanations.
Structured Logging: Every API request gets a correlation ID. Every log line includes: correlation ID, timestamp, operation name, duration, and outcome. When a request is slow, the logs show which stage of the convergence loop was the bottleneck.
Security Hardening:
Fuzz the Datalog parser with 10,000 randomly generated malformed inputs. Verify it never crashes — only returns parse errors.
Fuzz the YAML compiler with malformed YAML. Verify it rejects invalid input cleanly.
Ensure all API endpoints validate input schemas before processing.
API key authentication on all endpoints.
Rate limiting on the /validate endpoint.
Preconditions: Full convergence loop from Stage 10.5. FastAPI from Stage 3. OWASP Top 10 read. Postconditions: The API serves validation requests correctly. Proof traces are complete and machine-parseable. Every response is deterministic — same input always produces same output (verified by running the same request 100 times and comparing output hashes). Security fuzzing produces zero crashes. Structured logs enable request-level debugging.
▶ v10.1 — Performance Benchmarking (NEW)
Spec: Generate synthetic datasets at 1K, 10K, 100K, and 1M records. Define a rule set with 50, 100, and 500 rules. Run the full pipeline (convergence loop) at each combination of dataset size and rule count.
Measure and record:
Wall time per record at each scale.
Memory usage at each scale.
Number of convergence iterations at each scale.
Database I/O time as a percentage of total time.
Bottleneck identification: which stage of the convergence loop dominates at each scale.
Plot scaling curves. Determine whether the system scales linearly, quadratically, or worse with record count and rule count.
Preconditions: v10.0 API working. Postconditions: A document in the repo (BENCHMARKS.md) with charts showing performance at each scale. The bottleneck is identified. If performance is worse than O(N × R) where N is record count and R is rule count, the cause is documented and a plan for optimization is written.

STAGE 11.5 — DOMAIN ONBOARDING TOOLING (NEW)
The Real Moat
Skills coming in: Stage 11 complete. Full API working. Performance characterized. Brachman and Levesque read. SNOMED CT or FIBO studied.
Skills acquired: Natural language template compilation, CKG bootstrapping from sample data, PKB conflict detection, domain onboarding workflow design.
Reading before this stage:
Clingo/ASP tutorials from the Potassco group. Evaluate whether ASP's optimization capabilities are needed for the correction engine, or whether pure Datalog remains sufficient.
▶ v10.5 — The Rule Authoring Interface
Spec: Build a structured rule authoring system that allows a domain expert (not an engineer) to define constraints without writing Datalog.
Template System: A library of rule templates with fill-in-the-blank fields:
[field] must be [>=|<=|==|!=] [value]
[field] must be [>=|<=] [other_field]
[field] must not be null
If [field] == [value] then [field2] must be [comparison] [value2]
[field] must be unique per [grouping_field]
Each template compiles to one or more Datalog rules. The domain expert never sees Datalog.
CKG Bootstrap Tool: Given a sample dataset from a new domain:
Extract all unique values per column.
Cluster similar values using the comparator functions from Stage 5 (e.g., "St.", "St", "Street" cluster together).
Present candidate alias clusters to a human reviewer via a simple CLI interface.
Reviewer confirms, rejects, or modifies each cluster.
Confirmed clusters are added to the CKG as canonical mappings.
PKB Conflict Detection: When a new rule is added (via template or YAML), the system automatically checks:
Does this rule conflict with any existing rule? (Can any possible input trigger both rules with contradictory corrections?)
Is this rule subsumed by an existing rule? (Does a more general rule already cover this case?)
Does this rule create a cycle in the causal DAG?
Conflicts are reported before the rule is accepted. The domain expert must resolve conflicts (by adding exception clauses, adjusting scoping, or withdrawing one of the conflicting rules) before deployment.
Preconditions: Stage 11 complete. Brachman and Levesque knowledge base maintenance chapters read. At least one real regulatory document (EU AI Act Article 10, Basel III requirements, or similar) manually converted to Datalog rules as a proof-of-concept. Postconditions: A domain expert can define 20 rules for a new domain using the template system in under 2 hours, without writing any code. The CKG bootstrap tool reduces canonical mapping creation from weeks to hours. Conflict detection catches deliberately planted conflicting rules with zero false negatives.

PARALLEL READING TRACK
This runs alongside the build stages, not in series. Each reading assignment is timed to arrive just before the stage where it's most relevant.
Now through Fall 2026 (Stages 5–7)
Velleman "How to Prove It" — finish the book
Pearl "The Book of Why" — light read, foundational
Reducible algorithm videos for Stage 5 intuition
One neuro-symbolic paper per month (start with Scallop and DeepProbLog)
CEGEP Year 2026–2027 (Stages 7.5–10)
Abiteboul/Hull/Vianu "Foundations of Databases" — Datalog and fixpoint chapters
Pearl "Causality" chapters 1–3
Brachman/Levesque "Knowledge Representation and Reasoning" — first half
Dechter "Constraint Processing" — first four chapters
Kleppmann "Designing Data-Intensive Applications" — one chapter per week
OWASP Top 10 — one-time read before Stage 11
Waterloo First Year 2027–2028 (Stages 10.5–11.5)
Software Foundations Volume 1 (Coq proof assistant — for understanding formal verification)
Peters/Janzing/Schölkopf "Elements of Causal Inference"
Z3 SMT solver Python tutorial
Clingo/ASP tutorials from Potassco
SNOMED CT and FIBO ontology structure study
Neuro-symbolic paper pace increases to one per week
Waterloo Second Year 2028+ (Product Launch)
Baier and Katoen "Principles of Model Checking" — temporal logic chapters (if pursuing physical AI extension)
Skiena "Algorithm Design Manual" — as a reference for novel problems
Frontier papers as they're published
One undergraduate control theory course at Waterloo (if pursuing physical AI)

ARCHITECTURAL INVARIANTS DOCUMENT
Maintain this as a living file in your repo: INVARIANTS.md. Update it every time a design decision is made. Check every piece of code — written by you or generated by an AI agent — against this list before merging.
Canonicalization is idempotent. Canonicalizing an already-canonical record produces identical output.
Content-addressed identity. A record's ID is the SHA-256 hash of its canonical form. Same content = same ID. Changed content = changed ID.
The convergence loop is monotonic. Each pass can only add corrections or confirmations. A previously confirmed result is never reverted.
The convergence loop terminates. Either fixpoint is reached (zero new corrections) or the maximum iteration bound is hit. The system never runs forever.
No record is committed to the HIG without passing all active hard constraints.
Every auto-correction has a complete proof trace before it is applied. No correction is recorded without a derivation chain.
Ambiguous corrections are never auto-applied. If the trust hierarchy cannot resolve which field to correct, the record is flagged for human review.
The Datalog engine always terminates. Forward chaining on Horn clauses without negation reaches fixpoint in finite steps.
The audit trail is tamper-evident. Hash chains link every transformation. Modifying any intermediate record breaks the chain.
The rule parser never executes arbitrary code. All rule evaluation goes through AST walking. No eval(), no exec(), no dynamic code generation from user input.
Rule conflicts are detected at load time, not at evaluation time. A conflicting rule set is rejected before processing begins.
Tier 3 tokens (unresolved canonicalization) are never silently dropped. They pass through unchanged and are flagged for human review.

SUMMARY: STAGE SEQUENCE
Stage
Name
Key Output
Status
0
Foundations
First working script
✅
1
Deep Python
Multi-file architecture
✅
2
Data Engineer
Streaming pipeline + CLI + OOP
✅
2.5
Production Standards
Types, linting, parallelism, CI/CD
✅ (CI new)
3
Backend Basics
FastAPI + PostgreSQL + Job system
✅
4
Deterministic Foundations
Canonicalizer + Audit log
DONE
4.5
Chaos Test
Battle-tested against real dirty data
DONE
5
Entity Resolution Primitives
Comparators + Algorithms + Naive dedupe
In progress
6
Graph Data Structures
Graph engine + Union-Find + Clustering + Property-based testing
Upcoming
7
Logic & AST
Lexer + Parser + Rule engine
Upcoming
7.5
Datalog Engine
Forward chainer + Query engine
Upcoming
7.75
Compiler (streamlined)
Mini-interpreter
Upcoming
8
Advanced Entity Resolution
Blocking + Bloom filter + Golden record
Upcoming
9
Network Dynamics
Graph algorithms + Community detection
Upcoming
10
Causal Intelligence
Causal DAG + Causal rules + Proof tracer
Upcoming
10.25
Correction Engine
Trust hierarchy + Minimum-cost repair
NEW
10.5
Convergence Engine
Fixed-point loop across all layers
NEW
11
Semantic Architecture
API + Logging + Security + Benchmarks
Upcoming
11.5
Domain Onboarding
Rule authoring + CKG bootstrap + Conflict detection
NEW



The fundamental shift: you are becoming a compiler, not a coder.
When AI agents can write better Python than you, your job changes. You stop being the person who produces code and start being the person who produces correct specifications that compile into correct systems. The skill isn't typing — it's thinking precisely enough that when you describe what you want, the description itself is unambiguous.
Most people cannot do this. They describe what they want loosely, get back code that approximately matches, and then debug through trial and error. That workflow produces mediocre software. For MachineACS, mediocre is fatal — your product's entire value is that it's provably correct. If your specification to the AI agent is sloppy, the generated code will be subtly wrong in ways that violate your own correctness guarantees, and you won't catch it because you won't know what to look for.
So the core meta-skill is specification precision. The ability to describe a system's behavior so completely that there is exactly one correct implementation.

Skill 1: Formal specification thinking.
This means being able to describe what a function does in terms of its preconditions, postconditions, and invariants — before any code exists. Not in vague English. In precise, testable statements.
Example of how most people would prompt an agent: "Write a function that merges two entity records if they're similar enough."
Example of how you need to prompt: "Write a function that takes two Record objects and returns either a MergedRecord or a RejectionReason. Two records are merge-eligible if and only if their identity signatures match on all fields with trust level ≥ 7. If merge-eligible, the merged record takes each field's value from the record whose source has higher trust. If any field in the merged result violates a constraint in the active PKB module, return a RejectionReason containing the constraint ID and both conflicting values. The function must be pure — no side effects, no database calls."
The second version leaves almost no room for the agent to make a wrong architectural decision. The first version gives the agent freedom to invent an approach that might be clever but breaks your convergence guarantees. Writing specifications like the second version is a learnable skill, but it requires that you have already thought through the system's behavior at a level most people skip.
How to build this: Practice writing function contracts before writing functions. For every piece of MachineACS you build in the current stages, write out the preconditions, postconditions, and invariants in comments before you write or ask an agent to write the implementation. This is the single highest-leverage habit you can develop right now.

Skill 2: Architectural invariant tracking.
A complex system has invariants — properties that must always be true across the entire system, not just within one function. For MachineACS, examples include: "No record is ever committed to the HIG without passing all active hard constraints." "The convergence loop is monotonic — a confirmed correction is never reverted." "Every auto-correction has a complete proof trace before it's applied."
When you're building with AI agents, you'll be making dozens of requests per day. Each request produces code that's locally correct but might violate a system-wide invariant. The agent doesn't know about invariants unless you tell it every time, and even then it might not propagate them correctly across module boundaries.
Your job is to hold the full set of architectural invariants in your head and check every piece of generated code against them. This is the thing that separates a technical CEO who builds a correct system from one who builds a system that works on demos but fails on edge cases in production.
How to build this: Maintain a living document — literally a file in your repo — that lists every architectural invariant of MachineACS. Every time you add a new module or change a design decision, update it. Before you accept any agent-generated code, check it against the invariant list. This is tedious. It is also the only way to maintain system correctness when you're not the one writing every line.

Skill 3: Adversarial review of generated code.
AI agents in 2028 will write code that passes tests, looks clean, and runs correctly on the happy path. The failure modes will be subtle: an off-by-one in a boundary check that only matters when a constraint has exactly one satisfying value, a race condition in the convergence loop that only manifests when two corrections target the same field simultaneously, a merge function that silently drops a low-trust field instead of recording it in the proof trace.
You need to be able to read generated code not as a student learning from it, but as an adversary trying to break it. The question isn't "does this look right?" It's "what input would make this fail? What assumption is this code making that isn't guaranteed by my specification?"
This is a different skill than writing code. It's closer to what security auditors and formal verification engineers do. You don't need to be faster at writing the code than the agent — you need to be better at finding the cases where the code is wrong.
How to build this: For every function the agent generates, before you accept it, write three test cases designed to break it. Not normal inputs — edge cases. Empty inputs, inputs where two constraints conflict, inputs where the trust hierarchy produces a tie, inputs where the convergence loop would cycle if the monotonicity invariant were violated. If you can't think of adversarial inputs, you don't understand the function's failure modes well enough.

Skill 4: Decomposition into agent-safe units of work.
AI agents are good at implementing well-scoped, single-responsibility functions. They are bad at making cross-cutting architectural decisions. Your job is to decompose MachineACS into units of work that are small enough for an agent to implement correctly and self-contained enough that a mistake in one unit doesn't silently corrupt another.
This means your module boundaries, your interface contracts, and your data flow architecture need to be extremely clean. If you ask an agent to "build the entity resolution system," you'll get something that works but makes assumptions about how it interacts with the canonicalization engine and the constraint engine that may be wrong. If you ask the agent to "implement the identity signature generator that takes a CanonicalRecord and returns a SignatureVector according to this interface contract," the scope is tight enough that correctness is verifiable.
The skill is knowing where to draw the boundaries. Too large and the agent makes architectural choices you didn't sanction. Too small and you're micromanaging at the line level, which defeats the purpose of using agents at all.
How to build this: This is what the MachineACS stage system is already training you to do. Every stage defines a module with clear inputs, outputs, and responsibilities. Keep thinking at that level. When you move to building with agents, the "stage" becomes the unit of architectural specification, and within each stage, you decompose into functions with explicit contracts.

Skill 5: Knowing what the agent doesn't know.
This is the meta-skill that ties everything together. AI agents in 2028 will be confidently wrong about things that require deep system context. They won't know that your convergence loop requires monotonicity. They won't know that your field trust hierarchy means Address corrections are cheaper than DOB corrections. They won't know that a particular Datalog rule was scoped to insurance domains only and shouldn't fire on healthcare data.
Every time you interact with an agent, you need to ask: "What context does this agent need that it doesn't have? What assumptions will it make that are wrong for my system?" And then you need to provide that context explicitly in your specification, or catch the wrong assumptions in review.
The founders who will fail in the agent era are the ones who treat agents like magic and accept outputs uncritically. The ones who will succeed are the ones who treat agents like very fast, very capable junior engineers who have never read the architecture doc and will confidently implement something subtly wrong if you don't specify exactly what you need.



