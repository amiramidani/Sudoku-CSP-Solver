import copy, time, math, argparse, sys
from collections import deque
from typing import Dict, List, Optional, Set, Tuple



class SudokuCSP:
    def __init__(self, size: int = 9):
        self.size     = size
        self.box_size = int(math.isqrt(size))
        if self.box_size * self.box_size != size:
            raise ValueError(f"Grid size must be a perfect square; got {size}")

        
        self.grid: List[List[int]] = [[0]*size for _ in range(size)]
        
        self.domains: List[List[set]] = [
            [set(range(1, size+1)) for _ in range(size)]
            for _ in range(size)
        ]
        
        self._peer_cache: Dict[Tuple, List[Tuple]] = {}

        self.nodes_visited: int = 0
        self.backtracks:    int = 0

   

    def load(self, puzzle: List[List[int]]) -> bool:
       
        for r in range(self.size):
            for c in range(self.size):
                v = puzzle[r][c]
                if v != 0:
                    self.grid[r][c]    = v
                    self.domains[r][c] = {v}
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    if not self._propagate(r, c, self.grid[r][c]):
                        return False
        return True

    

    def peers(self, r: int, c: int) -> List[Tuple[int,int]]:
        key = (r, c)
        if key not in self._peer_cache:
            ps: Set[Tuple] = set()
            for cc in range(self.size):           
                if cc != c: ps.add((r, cc))
            for rr in range(self.size):           
                if rr != r: ps.add((rr, c))
            br = (r // self.box_size) * self.box_size  
            bc = (c // self.box_size) * self.box_size
            for rr in range(br, br + self.box_size):
                for cc in range(bc, bc + self.box_size):
                    if (rr, cc) != (r, c):
                        ps.add((rr, cc))
            self._peer_cache[key] = list(ps)
        return self._peer_cache[key]

    

    def _propagate(self, r: int, c: int, value: int) -> bool:
       
        for pr, pc in self.peers(r, c):
            if self.grid[pr][pc] == 0:
                self.domains[pr][pc].discard(value)
                if not self.domains[pr][pc]:
                    return False
        return True



    def unassigned(self) -> List[Tuple[int,int]]:
        return [(r, c) for r in range(self.size)
                for c in range(self.size) if self.grid[r][c] == 0]

    def is_solved(self) -> bool:
        return all(self.grid[r][c] != 0
                   for r in range(self.size) for c in range(self.size))


    def print_grid(self):
        b = self.box_size
        w = len(str(self.size)) + 1         
        sep = ("─" * (self.size * w + b - 1))
        for r in range(self.size):
            if r % b == 0 and r != 0:
                print("  " + sep)
            row = "  "
            for c in range(self.size):
                if c % b == 0 and c != 0:
                    row += "│"
                v = self.grid[r][c]
                row += (f"{v:>{w}}" if v else " " + "."*(w-1))
            print(row)
        print()



def ac3(csp: SudokuCSP) -> Tuple[bool, int]:
    queue: deque = deque()
    for r in range(csp.size):
        for c in range(csp.size):
            for pr, pc in csp.peers(r, c):
                queue.append(((r,c),(pr,pc)))

    removed = 0
    while queue:
        (xi, xj) = queue.popleft()
        ri, ci = xi; rj, cj = xj
        
        new = {v for v in csp.domains[ri][ci]
               if any(v != w for w in csp.domains[rj][cj])}
        delta = len(csp.domains[ri][ci]) - len(new)
        if delta:
            removed += delta
            csp.domains[ri][ci] = new
            if not csp.domains[ri][ci]:
                return False, removed
            
            for pk, pl in csp.peers(ri, ci):
                if (pk,pl) != (rj,cj):
                    queue.append(((pk,pl), (ri,ci)))
    return True, removed



def mrv_select(csp: SudokuCSP) -> Optional[Tuple[int,int]]:
   
    cells = csp.unassigned()
    if not cells:
        return None
    min_d = min(len(csp.domains[r][c]) for r,c in cells)
    candidates = [(r,c) for r,c in cells if len(csp.domains[r][c]) == min_d]
    if len(candidates) == 1:
        return candidates[0]
    
    assigned = {(r,c) for r in range(csp.size)
                for c in range(csp.size) if csp.grid[r][c] != 0}
    def degree(cell):
        r, c = cell
        return sum(1 for p in csp.peers(r,c) if p not in assigned)
    return max(candidates, key=degree)


def naive_select(csp: SudokuCSP) -> Optional[Tuple[int,int]]:
    """Baseline: first unassigned cell in reading order."""
    for r in range(csp.size):
        for c in range(csp.size):
            if csp.grid[r][c] == 0:
                return (r, c)
    return None


def lcv_order(csp: SudokuCSP, r: int, c: int) -> List[int]:
    
    def cost(v):
        return sum(1 for pr,pc in csp.peers(r,c)
                   if csp.grid[pr][pc] == 0 and v in csp.domains[pr][pc])
    return sorted(csp.domains[r][c], key=cost)




def _backtrack(csp: SudokuCSP,
               use_mrv: bool, use_lcv: bool,
               trace: bool, depth: int = 0) -> bool:
    
    csp.nodes_visited += 1

    if csp.is_solved():
        return True

    cell = (mrv_select if use_mrv else naive_select)(csp)
    if cell is None:
        return False
    r, c = cell

    values = lcv_order(csp, r, c) if use_lcv else sorted(csp.domains[r][c])

    for v in values:
        if trace:
            pad = "  " * depth
            dom_size = len(csp.domains[r][c])
            print(f"{pad}→ cell({r+1},{c+1}) = {v}  "
                  f"[domain size was {dom_size}]")

        
        saved_domains = copy.deepcopy(csp.domains)
        saved_grid    = copy.deepcopy(csp.grid)

       
        csp.grid[r][c]    = v
        csp.domains[r][c] = {v}

        
        ok = csp._propagate(r, c, v)
        if ok and _backtrack(csp, use_mrv, use_lcv, trace, depth+1):
            return True

        
        if trace:
            print(f"{'  '*depth}✗ backtrack ({r+1},{c+1})={v}")
        csp.backtracks += 1
        csp.domains = saved_domains
        csp.grid    = saved_grid

    return False


def solve(puzzle: List[List[int]], size: int = 9,
          use_mrv: bool = True, use_lcv: bool = True,
          use_ac3: bool = True, trace: bool = False
          ) -> Tuple[Optional[SudokuCSP], float, int]:
    
    csp = SudokuCSP(size)
    ok  = csp.load(puzzle)
    if not ok:
        return None, 0.0, 0

    ac3_removed = 0
    if use_ac3:
        ok2, ac3_removed = ac3(csp)
        if not ok2:
            return None, 0.0, ac3_removed

    t0      = time.perf_counter()
    solved  = _backtrack(csp, use_mrv, use_lcv, trace)
    elapsed = time.perf_counter() - t0

    return (csp if solved else None), elapsed, ac3_removed




PUZZLE_4 = [
    [1, 0, 0, 4],
    [0, 4, 1, 0],
    [0, 1, 4, 0],
    [4, 0, 0, 1],
]


PUZZLE_9_EASY = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


PUZZLE_9_HARD = [
    [1, 0, 0, 0, 0, 7, 0, 9, 0],
    [0, 3, 0, 0, 2, 0, 0, 0, 8],
    [0, 0, 9, 6, 0, 0, 5, 0, 0],
    [0, 0, 5, 3, 0, 0, 9, 0, 0],
    [0, 1, 0, 0, 8, 0, 0, 0, 2],
    [6, 0, 0, 0, 0, 4, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 7, 0, 0, 0, 3, 0, 0],
]


PUZZLE_16 = [
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0],
    [ 0,  5,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0],
    [ 0,  0, 12,  0,  0,  0,  0,  1,  0,  0,  6,  0,  0,  0,  0,  0],
    [ 0,  0,  0, 16,  0,  0,  0,  0,  3,  0,  0,  0,  0,  4,  0,  0],
    [ 0,  0,  5,  0,  0,  0,  0,  0,  0, 12,  0,  0,  0,  0, 15,  0],
    [ 0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
    [ 0,  0,  0, 14,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [10,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0, 13],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  0,  0, 10,  0,  0,  0],
    [ 7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  4,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0],
    [ 0,  0,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0],
    [ 0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0],
    [ 0,  0,  0,  0, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0,  0,  2],
]


def verify(csp: SudokuCSP) -> bool:
   
    n, b = csp.size, csp.box_size
    exp  = set(range(1, n+1))
    for r in range(n):
        if set(csp.grid[r]) != exp: return False
    for c in range(n):
        if {csp.grid[r][c] for r in range(n)} != exp: return False
    for br in range(0, n, b):
        for bc in range(0, n, b):
            box = {csp.grid[r][c] for r in range(br,br+b)
                                  for c in range(bc,bc+b)}
            if box != exp: return False
    return True
def run_benchmarks():
    sys.setrecursionlimit(10000)
    CFGS = [
        ("Naive",         dict(use_mrv=False,use_lcv=False,use_ac3=False)),
        ("MRV+FC+LCV",    dict(use_mrv=True, use_lcv=True, use_ac3=False)),
        ("MRV+FC+LCV+AC3",dict(use_mrv=True, use_lcv=True, use_ac3=True )),
    ]
    PUZZLES = [
        ("4×4  ",         PUZZLE_4,      4),
        ("9×9 easy",      PUZZLE_9_EASY, 9),
        ("9×9 hard",      PUZZLE_9_HARD, 9),
        ("16×16",         PUZZLE_16,    16),
    ]

    SEP = "=" * 85
    print("\n" + SEP)
    print(f"  {'Puzzle':<14} {'Config':<22} {'Time(s)':>9} "
          f"{'Nodes':>8} {'BT':>8} {'AC3-':>6} {'OK':>3}")
    print(SEP)

    for plabel, puzzle, size in PUZZLES:
        for clabel, cfg in CFGS:
            if size == 16 and clabel == "Naive":
                print(f"  {plabel:<14} {'Naive (skipped)':<22}   "
                      f"{'—':>9}      {'—':>8}      {'—':>8}   {'—':>6}  —")
                continue
            csp_r, t, ac3r = solve(puzzle, size, **cfg)
            ok = "Y" if (csp_r and verify(csp_r)) else "N"
            n  = csp_r.nodes_visited if csp_r else -1
            bt = csp_r.backtracks    if csp_r else -1
            print(f"  {plabel:<14} {clabel:<22} {t:>9.4f} "
                  f"{n:>8} {bt:>8} {ac3r:>6} {ok:>3}")
        print()

    print(SEP)
    print("  BT=backtracks  AC3-=domain values removed by AC-3  "
          "16×16 Naive skipped (too slow)\n")



def solve_with_ortools(puzzle: List[List[int]], size: int = 9):
    try:
        from ortools.sat.python import cp_model
    except ImportError:
        print("  OR-Tools not installed — run: pip install ortools"); return
    b     = int(math.isqrt(size))
    model = cp_model.CpModel()
    slvr  = cp_model.CpSolver()
    cells = [[model.NewIntVar(1, size, f"c{r}{c}")
              for c in range(size)] for r in range(size)]
    for r in range(size):
        for c in range(size):
            if puzzle[r][c]:
                model.Add(cells[r][c] == puzzle[r][c])
    for r in range(size): model.AddAllDifferent(cells[r])
    for c in range(size): model.AddAllDifferent([cells[r][c] for r in range(size)])
    for br in range(0,size,b):
        for bc in range(0,size,b):
            model.AddAllDifferent([cells[r][c]
                for r in range(br,br+b) for c in range(bc,bc+b)])
    t0  = time.perf_counter()
    st  = slvr.Solve(model)
    ela = time.perf_counter()-t0
    if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(f"  OR-Tools CP-SAT: {ela:.4f}s  "
              f"branches={slvr.NumBranches()}  conflicts={slvr.NumConflicts()}")
    else:
        print("  OR-Tools: no solution")




def run_assistant():
    print("\n" + "="*55)
    print("  Sudoku CSP Assistant")
    print("  Enter a 9×9 puzzle row by row.")
    print("  Use 0 or . for empty cells, digits for clues.")
    print("  Or type 'demo' to use the built-in easy puzzle.")
    print("="*55)

    raw = input("  Row 1 (or 'demo'): ").strip()
    if raw.lower() == "demo":
        puzzle, size = PUZZLE_9_EASY, 9
        print("  Loaded built-in easy 9×9 puzzle.")
    else:
        rows = []
        for i in range(1, 9):
            rows.append(raw)
            if i < 8:
                raw = input(f"  Row {i+1}: ").strip()
        rows.append(raw)
        puzzle = []
        size   = 9
        for row in rows:
            nums = [int(ch) if ch.isdigit() else 0
                    for ch in row.replace(".", "0") if ch in "0123456789."]
            if len(nums) != size:
                print(f"  Error: row has {len(nums)} cells, expected {size}. Aborting.")
                return
            puzzle.append(nums)

    print("\n  Input puzzle:")
    csp_disp = SudokuCSP(size)
    csp_disp.load(puzzle)
    csp_disp.print_grid()

    print("  Solving with MRV + AC-3 …")
    result, t, ac3r = solve(puzzle, size, use_mrv=True,
                            use_lcv=True, use_ac3=True)
    if result:
        print(f"  ✓ Solved in {t:.4f}s | "
              f"Nodes={result.nodes_visited} | "
              f"BT={result.backtracks} | AC3-={ac3r}")
        print("  Solution:")
        result.print_grid()
        ok = verify(result)
        print(f"  Verification: {'PASS ✓' if ok else 'FAIL ✗'}")
    else:
        print("  ✗ No solution found (puzzle may be invalid).")



def main():
    sys.setrecursionlimit(10000)
    parser = argparse.ArgumentParser(
        description="Sudoku CSP Solver  —  Topic 3  DS1 2025/2026")
    parser.add_argument("--trace",     action="store_true")
    parser.add_argument("--bench",     action="store_true")
    parser.add_argument("--assistant", action="store_true")
    parser.add_argument("--size",      type=int, default=0,
                        help="Solve built-in puzzle of given size (4, 9, or 16)")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Sudoku CSP Solver  ·  Topic 3  ·  DS1 2025/2026        ║")
    print("║  Backtracking + MRV + Degree + LCV + FC + AC-3          ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    if args.assistant: run_assistant(); return
    if args.bench:     run_benchmarks(); return

    if args.size in (4, 9, 16):
        puzzles = {4: (PUZZLE_4,4), 9: (PUZZLE_9_EASY,9), 16: (PUZZLE_16,16)}
        puz, sz = puzzles[args.size]
        print(f"── Solving {sz}×{sz} puzzle ─────────────────────────────────")
        r, t, ac3r = solve(puz, sz)
        if r:
            r.print_grid()
            print(f"  {t:.4f}s | Nodes={r.nodes_visited} | "
                  f"BT={r.backtracks} | AC3-={ac3r} | "
                  f"{'PASS ✓' if verify(r) else 'FAIL ✗'}")
        else:
            print("  No solution.")
        return

    if args.trace:
        print("── Trace: 4×4 puzzle, MRV + FC + LCV ───────────────────────")
        csp_t = SudokuCSP(4); csp_t.load(PUZZLE_4)
        print("  Input:"); csp_t.print_grid()
        r, t, ac3r = solve(PUZZLE_4, 4, trace=True)
        if r:
            print("  Solution:"); r.print_grid()
            print(f"  {t:.4f}s | Nodes={r.nodes_visited} | "
                  f"BT={r.backtracks} | AC3-={ac3r}")
        return

    
    print("── Demo 1: 4×4 Sudoku ───────────────────────────────────────")
    c4 = SudokuCSP(4); c4.load(PUZZLE_4); print("  Input:"); c4.print_grid()
    r4, t4, a4 = solve(PUZZLE_4, 4)
    if r4:
        print("  Solution:"); r4.print_grid()
        print(f"  {t4:.4f}s | Nodes={r4.nodes_visited} | "
              f"BT={r4.backtracks} | AC3-={a4} | {'PASS ✓' if verify(r4) else 'FAIL'}")

    
    print("\n── Demo 2: 9×9 Easy — Naive vs MRV+AC3 ─────────────────────")
    for lbl, kw in [
        ("Naive              ", dict(use_mrv=False,use_lcv=False,use_ac3=False)),
        ("MRV+FC+LCV         ", dict(use_mrv=True, use_lcv=True, use_ac3=False)),
        ("MRV+FC+LCV+AC3     ", dict(use_mrv=True, use_lcv=True, use_ac3=True )),
    ]:
        r9, t9, a9 = solve(PUZZLE_9_EASY, 9, **kw)
        ok = "Y" if (r9 and verify(r9)) else "N"
        print(f"  {ok} {lbl}  time={t9:.4f}s  "
              f"nodes={r9.nodes_visited if r9 else '—':>5}  "
              f"BT={r9.backtracks if r9 else '—':>5}  AC3-={a9}")

    print("\n  Solution (MRV+FC+LCV+AC3):")
    r9e, _, _ = solve(PUZZLE_9_EASY, 9)
    if r9e: r9e.print_grid()

    
    print("── Demo 3: 9×9 Hard (AI Escargot) ──────────────────────────")
    for lbl, kw in [
        ("MRV+FC+LCV         ", dict(use_mrv=True, use_lcv=True, use_ac3=False)),
        ("MRV+FC+LCV+AC3     ", dict(use_mrv=True, use_lcv=True, use_ac3=True )),
    ]:
        rh, th, ah = solve(PUZZLE_9_HARD, 9, **kw)
        ok = "Y" if (rh and verify(rh)) else "N"
        print(f"  {ok} {lbl}  time={th:.4f}s  "
              f"nodes={rh.nodes_visited if rh else '—':>6}  "
              f"BT={rh.backtracks if rh else '—':>5}  AC3-={ah}")

   
    print("\n── Demo 4: OR-Tools vs Our Solver (9×9 easy) ───────────────")
    r_us, t_us, _ = solve(PUZZLE_9_EASY, 9)
    print(f"  Our solver :  {t_us:.4f}s  nodes={r_us.nodes_visited}  BT={r_us.backtracks}")
    solve_with_ortools(PUZZLE_9_EASY, 9)

    print("\n── Benchmark Table ──────────────────────────────────────────")
    run_benchmarks()


if __name__ == "__main__":
    main()