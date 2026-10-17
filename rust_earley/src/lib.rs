//! Rust port of Fandango's Earley parser
//! (`fandango.language.grammar.parser.iterative_parser.IterativeParser` and
//! `forest.ForestBuilder`).
//!
//! The port is deliberately literal: every data structure of the Python
//! implementation has a counterpart here, and every operation happens in the
//! same order, so that the parse table, the edges of every item, and therefore
//! the order in which derivations are enumerated are identical. Python object
//! identity (`is`) maps to arena indices.
//!
//! What stays in Python (see `rust_iterative_parser.py`):
//! * grammar compilation (`GrammarCompiler`) and symbol interning,
//! * regex matching (called back, results cached per input position),
//! * context-dependent repetitions (called back with the incomplete tree),
//! * turning the derivations into `DerivationTree` objects.

mod pyset;

use indexmap::IndexMap;
use pyo3::exceptions::{
    PyAssertionError, PyIndexError, PyKeyError, PyRecursionError, PyValueError,
};
use pyo3::intern;
use pyo3::{PyTraverseError, PyVisit};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList, PyString, PyTuple};
use rustc_hash::{FxBuildHasher, FxHashMap, FxHashSet};
use smallvec::SmallVec;
use std::sync::Arc;

type FxIndexMap<K, V> = IndexMap<K, V, FxBuildHasher>;

const NONE: u32 = u32::MAX;

// ---------------------------------------------------------------------------
// Grammar
// ---------------------------------------------------------------------------

enum SymKind {
    NonTerminal,
    /// A plain string/bytes terminal, as code points (str) or byte values (bytes).
    Literal(Arc<[u32]>),
    Regex,
    /// A bit terminal; whether it matches bit 0 / bit 1.
    Bits([bool; 2]),
    /// A terminal the scanner cannot handle (the Python parser asserts).
    Invalid,
}

struct Sym {
    kind: SymKind,
    /// `hash(symbol)` in the Python process.
    hash: i64,
    /// Whether the non-terminal is in `GrammarCompiler._rules`.
    in_rules: bool,
    /// Whether the non-terminal is a context rule (`<*ctx_N*>`).
    is_ctx: bool,
}

struct Alt {
    syms: Vec<(u32, u32)>,
    /// Equality class of the Python tuple (tuple `==`).
    eq: u32,
    /// `hash(symbols[0][0] if symbols else None)`.
    first_hash: i64,
}

// ---------------------------------------------------------------------------
// Parse states
// ---------------------------------------------------------------------------

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Filler {
    /// A terminal tree created by a scan.
    Tree(u32),
    State(u32),
    Leo(u32),
    /// A list of trees (the children of a state replaced for a context rule).
    List(u32),
}

#[derive(Clone, Copy, Debug)]
struct Edge {
    previous: u32,
    filler: Filler,
    params: u32,
}

#[derive(Clone)]
struct State {
    nt: u32,
    position: u32,
    alt: u32,
    dot: u32,
    partial: u32,
    fc: bool,
    edges: SmallVec<[Edge; 1]>,
}

/// What `ParseState.__eq__` compares.
type Key = (u32, u32, u32, u32, bool);

#[derive(Clone, Default)]
struct Column {
    states: Vec<u32>,
    waiting: FxHashMap<u32, Vec<u32>>,
    unique: FxHashMap<Key, u32>,
    predicted: FxHashSet<u32>,
    /// `None` is stored as `NONE`.
    leo: FxHashMap<u32, u32>,
    empty_completions: FxHashMap<u32, Vec<u32>>,
}

struct ChainNode {
    head: u32,
    tail: u32,
}

struct LeoEntry {
    top: u32,
    chain: u32,
}

struct LeoNest {
    chain: u32,
    inner: u32,
    top_params: u32,
}

const KIND_NT: u32 = 0;
const KIND_TERM: u32 = 1;
const KIND_BIT: u32 = 2;

/// A node of a (parser) derivation tree.
/// NT: a = symbol, b = params. TERM: input[a..b]. BIT: a = bit.
#[derive(Clone, Copy)]
struct Node {
    kind: u32,
    a: u32,
    b: u32,
    cstart: u32,
    clen: u32,
}

struct Choices {
    picks: Vec<usize>,
    edge_counts: Vec<usize>,
}

struct Enumerator {
    state: u32,
    picks: Vec<usize>,
    done: bool,
}

const REPS_RESET: u8 = 0;
const REPS_INHERIT: u8 = 1;
const REPS_REPETITION: u8 = 2;

struct TreeContext {
    dt_class: Py<PyAny>,
    object_new: Py<PyAny>,
    symbols: Py<PyList>,
    params: Py<PyList>,
    repetition_cb: Py<PyAny>,
    terminal_cb: Py<PyAny>,
}

struct RepInfo {
    mode: u8,
    node: Option<Py<PyAny>>,
    id: Option<Py<PyAny>>,
}

struct TreeAtSession {
    flagged: Vec<(u32, bool)>,
    index: usize,
    enumerator: Option<usize>,
    seen: FxHashSet<(u128, bool)>,
}

struct Frame {
    state: u32,
    path: Option<Vec<Edge>>,
    children: Vec<u32>,
}

impl Frame {
    fn new(state: u32) -> Self {
        Frame {
            state,
            path: None,
            children: Vec::new(),
        }
    }
}

#[pyclass]
struct EarleyCore {
    // grammar
    syms: Vec<Sym>,
    alts: Vec<Alt>,
    rules: Vec<Option<Arc<Vec<u32>>>>,
    hash_none: i64,

    // parse
    states: Vec<State>,
    columns: Vec<Column>,
    saved: Vec<u32>,
    column_index: usize,
    cpb: usize,
    incomplete_mode: bool,
    first_consume: bool,
    start_alt: u32,
    implicit_start: u32,
    consumed: usize,
    /// Where the chunk being consumed starts in `input`.
    chunk_start: usize,
    max_position: i64,
    input: Vec<u32>,
    completed: FxIndexMap<i64, FxIndexMap<Key, u32>>,
    incomplete: FxIndexMap<i64, FxIndexMap<Key, u32>>,
    chains: Vec<ChainNode>,
    leo_entries: Vec<LeoEntry>,
    nests: Vec<LeoNest>,
    lists: Vec<Arc<Vec<u32>>>,

    // forest
    nodes: Vec<Node>,
    node_children: Vec<u32>,
    children_cache: FxHashMap<u32, Arc<Vec<u32>>>,
    ambiguous_cache: FxHashMap<u32, bool>,
    enumerators: Vec<Enumerator>,
    sessions: Vec<TreeAtSession>,
    tree_ctx: Option<TreeContext>,
    rep_info: Vec<Option<RepInfo>>,
    terminal_objs: FxHashMap<u32, Py<PyAny>>,
    sources_objs: FxHashMap<u32, Py<PyAny>>,

    // callbacks, only set during `consume`
    regex_cb: Option<Py<PyAny>>,
    ctx_cb: Option<Py<PyAny>>,
    regex_cache: FxHashMap<(u32, u32, u32, u32), Arc<(Vec<u32>, bool)>>,

    // scratch for graph walks
    mark: Vec<u32>,
    mark_gen: u32,
}

/// `table[index]`, raising `IndexError` like Python when out of range.
fn column_at(table: &[u32], index: i64) -> PyResult<u32> {
    if index < 0 || index as usize >= table.len() {
        return Err(PyIndexError::new_err("list index out of range"));
    }
    Ok(table[index as usize])
}

fn empty_rc() -> Arc<Vec<u32>> {
    Arc::new(Vec::new())
}

impl EarleyCore {
    // ----- state helpers ---------------------------------------------------

    #[inline]
    fn st(&self, s: u32) -> &State {
        &self.states[s as usize]
    }

    #[inline]
    fn alt_len(&self, s: u32) -> usize {
        self.alts[self.st(s).alt as usize].syms.len()
    }

    #[inline]
    fn next_sym(&self, s: u32) -> Option<(u32, u32)> {
        let st = self.st(s);
        self.alts[st.alt as usize]
            .syms
            .get(st.dot as usize)
            .copied()
    }

    #[inline]
    fn next_params(&self, s: u32) -> u32 {
        self.next_sym(s).map(|x| x.1).unwrap_or(0)
    }

    #[inline]
    fn is_finished(&self, s: u32) -> bool {
        let st = self.st(s);
        st.dot as usize >= self.alts[st.alt as usize].syms.len() && st.partial == 0 && !st.fc
    }

    #[inline]
    fn key_of(&self, st: &State) -> Key {
        (
            st.nt,
            st.position,
            self.alts[st.alt as usize].eq,
            st.dot,
            st.fc,
        )
    }

    #[inline]
    fn key(&self, s: u32) -> Key {
        self.key_of(self.st(s))
    }

    #[inline]
    fn next_is_nonterminal(&self, s: u32) -> bool {
        match self.next_sym(s) {
            Some((sym, _)) => matches!(self.syms[sym as usize].kind, SymKind::NonTerminal),
            None => false,
        }
    }

    /// `state.next(force_completed)`, without edges.
    fn advanced(&self, s: u32, force: bool) -> State {
        let st = self.st(s);
        State {
            nt: st.nt,
            position: st.position,
            alt: st.alt,
            dot: st.dot + 1,
            partial: st.partial,
            fc: st.fc || force,
            edges: SmallVec::new(),
        }
    }

    /// `state.copy()` whose edges are replaced right after.
    fn copied(&self, s: u32) -> State {
        let st = self.st(s);
        State {
            nt: st.nt,
            position: st.position,
            alt: st.alt,
            dot: st.dot,
            partial: st.partial,
            fc: st.fc,
            edges: SmallVec::new(),
        }
    }

    fn push_state(&mut self, st: State) -> u32 {
        let id = self.states.len() as u32;
        self.states.push(st);
        id
    }

    /// `Column.add` for a freshly created state.
    fn add_fresh(&mut self, col: u32, proto: State) -> bool {
        let key = self.key_of(&proto);
        if let Some(&existing) = self.columns[col as usize].unique.get(&key) {
            if !proto.edges.is_empty() {
                // Same item, different derivation: keep it as an alternative.
                self.states[existing as usize]
                    .edges
                    .extend(proto.edges.iter().copied());
            }
            return false;
        }
        let id = self.push_state(proto);
        let next = self.next_sym(id);
        let column = &mut self.columns[col as usize];
        column.states.push(id);
        column.unique.insert(key, id);
        if let Some((sym, _)) = next {
            column.waiting.entry(sym).or_default().push(id);
        }
        true
    }

    /// `Column.replace(old, new)`.
    fn replace(&mut self, col: u32, old: u32, new: u32) -> PyResult<()> {
        let ko = self.key(old);
        let kn = self.key(new);
        let old_next = self.next_sym(old);
        let new_next = self.next_sym(new);
        let pos = {
            let column = &self.columns[col as usize];
            column
                .states
                .iter()
                .position(|&s| self.key(s) == ko)
                .ok_or_else(|| PyValueError::new_err("state not in column"))?
        };
        let waiter_pos = match old_next {
            Some((sym, _)) => {
                let list = self.columns[col as usize]
                    .waiting
                    .get(&sym)
                    .ok_or_else(|| PyKeyError::new_err("symbol not waited for"))?;
                Some((
                    sym,
                    list.iter()
                        .position(|&s| self.key(s) == ko)
                        .ok_or_else(|| PyValueError::new_err("state not waiting"))?,
                ))
            }
            None => None,
        };
        let column = &mut self.columns[col as usize];
        column.unique.remove(&ko);
        column.unique.insert(kn, new);
        column.states[pos] = new;
        if let Some((sym, p)) = waiter_pos {
            column.waiting.get_mut(&sym).unwrap().remove(p);
        }
        if let Some((sym, _)) = new_next {
            column.waiting.entry(sym).or_default().push(new);
        }
        Ok(())
    }

    fn has_children(&self, s: u32) -> bool {
        let mut current = s;
        while current != NONE {
            let st = self.st(current);
            let Some(edge) = st.edges.first() else {
                break;
            };
            match edge.filler {
                Filler::List(l) => {
                    if !self.lists[l as usize].is_empty() {
                        return true;
                    }
                }
                _ => return true,
            }
            current = edge.previous;
        }
        false
    }

    fn push_linked_states(&self, s: u32, out: &mut Vec<u32>) {
        for edge in self.st(s).edges.iter() {
            if edge.previous != NONE {
                out.push(edge.previous);
            }
            match edge.filler {
                Filler::State(f) => out.push(f),
                Filler::Leo(n) => {
                    let nest = &self.nests[n as usize];
                    out.push(nest.inner);
                    let mut c = nest.chain;
                    while c != NONE {
                        out.push(self.chains[c as usize].head);
                        c = self.chains[c as usize].tail;
                    }
                }
                _ => {}
            }
        }
    }

    fn next_mark(&mut self) -> u32 {
        if self.mark.len() < self.states.len() {
            self.mark.resize(self.states.len() + 1024, 0);
        }
        self.mark_gen = self.mark_gen.wrapping_add(1);
        if self.mark_gen == 0 {
            self.mark.iter_mut().for_each(|m| *m = 0);
            self.mark_gen = 1;
        }
        self.mark_gen
    }

    /// `IterativeParser._closes_cycle`.
    fn closes_cycle(&mut self, col: u32, key: &Key, sources: [u32; 2]) -> bool {
        let Some(&target) = self.columns[col as usize].unique.get(key) else {
            return false;
        };
        let gen = self.next_mark();
        let mut pending: Vec<u32> = sources.to_vec();
        while let Some(current) = pending.pop() {
            if current == target {
                return true;
            }
            if self.mark[current as usize] == gen {
                continue;
            }
            self.mark[current as usize] = gen;
            self.push_linked_states(current, &mut pending);
        }
        false
    }

    /// `Column.has_edge`.
    fn has_edge(&self, col: u32, key: &Key, previous: u32, filler: u32) -> bool {
        match self.columns[col as usize].unique.get(key) {
            Some(&known) => self
                .st(known)
                .edges
                .iter()
                .any(|e| e.previous == previous && e.filler == Filler::State(filler)),
            None => false,
        }
    }

    // ----- Earley operations -----------------------------------------------

    /// `IterativeParser._leo_entry`.
    fn leo_entry(&mut self, table: &[u32], column_index: usize, symbol: u32) -> u32 {
        let mut pending: Vec<(usize, u32, u32)> = Vec::new();
        let mut entry = NONE;
        let (mut current_index, mut current_symbol) = (column_index, symbol);
        loop {
            let col = table[current_index] as usize;
            if let Some(&e) = self.columns[col].leo.get(&current_symbol) {
                entry = e;
                break;
            }
            let waiter = match self.columns[col].waiting.get(&current_symbol) {
                Some(w) if w.len() == 1 => w[0],
                _ => {
                    self.columns[col].leo.insert(current_symbol, NONE);
                    break;
                }
            };
            if self.st(waiter).dot as usize != self.alt_len(waiter).wrapping_sub(1)
                || self.st(waiter).partial > 0
            {
                self.columns[col].leo.insert(current_symbol, NONE);
                break;
            }
            pending.push((current_index, current_symbol, waiter));
            current_index = self.st(waiter).position as usize;
            current_symbol = self.st(waiter).nt;
            if current_index > column_index {
                break;
            }
        }
        for &(cached_index, cached_symbol, waiter) in pending.iter().rev() {
            let new_entry = if entry == NONE {
                LeoEntry {
                    top: waiter,
                    chain: NONE,
                }
            } else {
                let old = &self.leo_entries[entry as usize];
                let (top, tail) = (old.top, old.chain);
                let chain = self.chains.len() as u32;
                self.chains.push(ChainNode { head: waiter, tail });
                LeoEntry { top, chain }
            };
            entry = self.leo_entries.len() as u32;
            self.leo_entries.push(new_entry);
            self.columns[table[cached_index] as usize]
                .leo
                .insert(cached_symbol, entry);
        }
        entry
    }

    /// `IterativeParser.complete`.
    fn complete(&mut self, s: u32, table: &[u32], ci: usize, late: Option<u32>) {
        let col = table[ci];
        let force = !self.is_finished(s);
        let (position, nt) = (self.st(s).position, self.st(s).nt);
        if (position as usize) < ci {
            let entry = self.leo_entry(table, position as usize, nt);
            if entry != NONE {
                let (top, chain) = {
                    let e = &self.leo_entries[entry as usize];
                    (e.top, e.chain)
                };
                let mut proto = self.advanced(top, force);
                if force {
                    let key = self.key_of(&proto);
                    if self.closes_cycle(col, &key, [s, top]) {
                        return;
                    }
                }
                let top_params = self.next_params(top);
                let nest = self.nests.len() as u32;
                self.nests.push(LeoNest {
                    chain,
                    inner: s,
                    top_params,
                });
                proto.edges.push(Edge {
                    previous: top,
                    filler: Filler::Leo(nest),
                    params: top_params,
                });
                self.add_fresh(col, proto);
                return;
            }
        }
        let is_empty_completion = !force && position as usize == ci;
        match late {
            None => {
                if is_empty_completion {
                    self.columns[col as usize]
                        .empty_completions
                        .entry(nt)
                        .or_default()
                        .push(s);
                }
                // Iterate the live list: items added while completing an
                // empty item in its own column are seen, as in Python.
                let wcol = table[position as usize] as usize;
                let mut i = 0;
                loop {
                    let waiter = match self.columns[wcol].waiting.get(&nt) {
                        Some(list) if i < list.len() => list[i],
                        _ => break,
                    };
                    i += 1;
                    self.complete_one(s, waiter, col, force, is_empty_completion, false);
                }
            }
            Some(waiter) => {
                self.complete_one(s, waiter, col, force, is_empty_completion, true);
            }
        }
    }

    fn complete_one(
        &mut self,
        s: u32,
        waiter: u32,
        col: u32,
        force: bool,
        is_empty_completion: bool,
        late: bool,
    ) {
        if waiter == s {
            // Only forcing gets here: a state cannot fill its own symbol.
            return;
        }
        let mut proto = self.advanced(waiter, force);
        let key = self.key_of(&proto);
        if late && self.has_edge(col, &key, waiter, s) {
            return;
        }
        if (force || is_empty_completion) && self.closes_cycle(col, &key, [s, waiter]) {
            return;
        }
        let params = self.next_params(waiter);
        proto.edges.push(Edge {
            previous: waiter,
            filler: Filler::State(s),
            params,
        });
        self.add_fresh(col, proto);
    }

    /// `IterativeParser.predict`.
    fn predict(
        &mut self,
        py: Python<'_>,
        s: u32,
        table: &[u32],
        ci: usize,
        hookin: bool,
    ) -> PyResult<()> {
        let (symbol, _) = self.next_sym(s).expect("predict needs a next symbol");
        let col = table[ci];
        let is_ctx = self.syms[symbol as usize].is_ctx;
        if self.columns[col as usize].predicted.contains(&symbol) {
            let completions: Vec<u32> = self.columns[col as usize]
                .empty_completions
                .get(&symbol)
                .cloned()
                .unwrap_or_default();
            for completion in completions {
                self.complete(completion, table, ci, Some(s));
            }
            if !is_ctx {
                return Ok(());
            }
        } else {
            self.columns[col as usize].predicted.insert(symbol);
        }

        if let Some(alts) = self.rules.get(symbol as usize).cloned().flatten() {
            let order: Vec<usize> = if alts.len() <= 1 {
                (0..alts.len()).collect()
            } else {
                let nt_hash = self.syms[symbol as usize].hash;
                let hashes: Vec<i64> = alts
                    .iter()
                    .map(|&a| {
                        let alt = &self.alts[a as usize];
                        pyset::tuple_hash(&[
                            nt_hash,
                            ci as i64,
                            0,
                            alt.syms.len() as i64,
                            alt.first_hash,
                            0,
                        ])
                    })
                    .collect();
                pyset::set_iteration_order(&hashes)
            };
            for idx in order {
                self.add_fresh(
                    col,
                    State {
                        nt: symbol,
                        position: ci as u32,
                        alt: alts[idx],
                        dot: 0,
                        partial: 0,
                        fc: false,
                        edges: SmallVec::new(),
                    },
                );
            }
            return Ok(());
        }
        if is_ctx {
            self.predict_ctx_rule(py, s, table, ci, symbol, hookin)?;
        }
        Ok(())
    }

    /// The states `construct_incomplete_tree` walks through: `s`, then each
    /// first item in the column `s` started in that waits for its symbol.
    fn incomplete_chain(&self, s: u32, table: &[u32]) -> PyResult<Vec<u32>> {
        let mut chain = vec![s];
        let mut seen: FxHashSet<u32> = FxHashSet::default();
        seen.insert(s);
        let mut current = s;
        loop {
            let (position, nt) = (self.st(current).position, self.st(current).nt);
            let col = &self.columns[table[position as usize] as usize];
            let found = col
                .states
                .iter()
                .copied()
                .find(|&t| self.next_sym(t).map(|x| x.0) == Some(nt));
            match found {
                Some(t) => {
                    if !seen.insert(t) {
                        // The Python parser would loop forever here.
                        return Err(PyRecursionError::new_err(
                            "construct_incomplete_tree does not terminate (cyclic waiters)",
                        ));
                    }
                    chain.push(t);
                    current = t;
                }
                None => break,
            }
        }
        Ok(chain)
    }

    fn chain_to_py<'py>(&mut self, py: Python<'py>, chain: &[u32]) -> PyResult<Bound<'py, PyList>> {
        let out = PyList::empty(py);
        for &state in chain {
            let children = self.children_cached(state);
            let flat = self.flatten(&children);
            let item = PyTuple::new(
                py,
                [
                    self.st(state).nt.into_pyobject(py)?.into_any(),
                    self.next_params(state).into_pyobject(py)?.into_any(),
                    PyBytes::new(py, u32_bytes(&flat)).into_any(),
                ],
            )?;
            out.append(item)?;
        }
        Ok(out)
    }

    /// `IterativeParser.predict_ctx_rule`.
    fn predict_ctx_rule(
        &mut self,
        py: Python<'_>,
        s: u32,
        table: &[u32],
        ci: usize,
        symbol: u32,
        hookin: bool,
    ) -> PyResult<()> {
        let chain = self.incomplete_chain(s, table)?;
        let chain_py = self.chain_to_py(py, &chain)?;
        let cb = self
            .ctx_cb
            .as_ref()
            .expect("context callback set during consume")
            .clone_ref(py);
        let result = cb.call1(
            py,
            (symbol, self.st(s).alt, self.st(s).dot, chain_py, hookin),
        )?;
        let result = result.bind(py);
        if result.is_none() {
            return Ok(());
        }
        let (new_alt, registrations): (u32, Bound<'_, PyTuple>) = result.extract()?;
        self.register_impl(&registrations)?;

        let children = self.children_cached(s);
        let mut edges: SmallVec<[Edge; 1]> = SmallVec::new();
        if !children.is_empty() {
            let list = self.lists.len() as u32;
            self.lists.push(children);
            edges.push(Edge {
                previous: NONE,
                filler: Filler::List(list),
                params: 0,
            });
        }
        let st = self.st(s);
        let new_state = State {
            nt: st.nt,
            position: st.position,
            alt: new_alt,
            dot: st.dot,
            partial: st.partial,
            fc: st.fc,
            edges,
        };
        let new = self.push_state(new_state);
        let col = table[ci];
        let ks = self.key(s);
        if self.columns[col as usize].unique.contains_key(&ks) {
            self.replace(col, s, new)?;
        }
        self.predict(py, new, table, ci, false)
    }

    fn scan_bit(
        &mut self,
        s: u32,
        bits: [bool; 2],
        word: &[u32],
        table: &[u32],
        ci: usize,
        word_index: usize,
        bit_position: usize,
    ) -> PyResult<()> {
        if word_index >= word.len() {
            return Ok(());
        }
        let bit = (word[word_index] >> bit_position) & 1;
        if !bits[bit as usize] {
            return Ok(());
        }
        let mut next = self.advanced(s, false);
        let tree = self.new_leaf(KIND_BIT, bit, 0);
        next.edges.push(Edge {
            previous: s,
            filler: Filler::Tree(tree),
            params: 0,
        });
        self.add_fresh(column_at(table, ci as i64 + 1)?, next);
        self.max_position = self.max_position.max(word_index as i64);
        Ok(())
    }

    /// The global input range of `_continued_word(state, word, word_index)`.
    fn continued_word(&self, s: u32, global_index: usize) -> PyResult<(usize, usize)> {
        let st = self.st(s);
        if st.partial == 0 {
            return Ok((global_index, 0));
        }
        match st.edges.first().map(|e| e.filler) {
            Some(Filler::Tree(t)) => {
                let node = self.nodes[t as usize];
                if node.kind != KIND_TERM || node.b as usize != global_index {
                    return Err(PyAssertionError::new_err(
                        "partial match does not continue the input",
                    ));
                }
                Ok((node.a as usize, (node.b - node.a) as usize))
            }
            _ => Err(PyAssertionError::new_err("partial match without terminal")),
        }
    }

    fn predecessor(&self, s: u32) -> u32 {
        self.st(s).edges.first().map(|e| e.previous).unwrap_or(NONE)
    }

    #[allow(clippy::too_many_arguments)]
    fn scan_bytes(
        &mut self,
        s: u32,
        word_len: usize,
        table: &[u32],
        ci: usize,
        word_index: usize,
        literal: &[u32],
    ) -> PyResult<()> {
        let global_index = self.chunk_start + word_index;
        let (cstart, _) = self.continued_word(s, global_index)?;
        let cend = self.input.len();
        let check = &self.input[cstart..cend];
        let partial = self.st(s).partial as i64;
        let dot_len = literal.len() as i64;

        let (mut next, match_length) = if check.starts_with(literal) {
            let mut next = self.advanced(s, false);
            next.partial = 0;
            (next, literal.len())
        } else {
            if (word_index as i64 + dot_len - partial) < word_len as i64 {
                return Ok(());
            }
            if !literal.starts_with(check) || check.is_empty() {
                return Ok(());
            }
            let mut next = self.copied(s);
            next.partial = check.len() as u32;
            (next, check.len())
        };
        let previous = if partial > 0 { self.predecessor(s) } else { s };
        let tree = self.new_leaf(KIND_TERM, cstart as u32, (cstart + match_length) as u32);
        next.edges.push(Edge {
            previous,
            filler: Filler::Tree(tree),
            params: 0,
        });
        let target = ci as i64 + (match_length as i64 - partial) * self.cpb as i64;
        self.add_fresh(column_at(table, target)?, next);
        self.max_position = self.max_position.max((word_index + match_length) as i64);
        Ok(())
    }

    fn regex_lengths(
        &mut self,
        py: Python<'_>,
        sym: u32,
        start: usize,
        end: usize,
        min_length: usize,
    ) -> PyResult<Arc<(Vec<u32>, bool)>> {
        let key = (sym, start as u32, end as u32, min_length as u32);
        if let Some(r) = self.regex_cache.get(&key) {
            return Ok(r.clone());
        }
        let cb = self
            .regex_cb
            .as_ref()
            .expect("regex callback set during consume")
            .clone_ref(py);
        let (lengths, can_continue): (Vec<u32>, bool) =
            cb.call1(py, (sym, start, end, min_length))?.extract(py)?;
        let r = Arc::new((lengths, can_continue));
        self.regex_cache.insert(key, r.clone());
        Ok(r)
    }

    fn scan_regex(
        &mut self,
        py: Python<'_>,
        s: u32,
        sym: u32,
        table: &[u32],
        ci: usize,
        word_index: usize,
    ) -> PyResult<()> {
        let global_index = self.chunk_start + word_index;
        let (cstart, prev_len) = self.continued_word(s, global_index)?;
        let cend = self.input.len();
        let partial = self.st(s).partial as i64;
        let predecessor = if partial > 0 { self.predecessor(s) } else { s };
        let found = self.regex_lengths(py, sym, cstart, cend, prev_len + 1)?;
        let mut lengths: Vec<u32> = Vec::new();
        if partial == 0 {
            let empty = self.regex_lengths(py, sym, cstart, cstart, 0)?;
            lengths.extend_from_slice(&empty.0);
        }
        lengths.extend_from_slice(&found.0);
        let can_continue = found.1;
        for length in lengths {
            let mut next = self.advanced(s, false);
            next.partial = 0;
            let tree = self.new_leaf(KIND_TERM, cstart as u32, cstart as u32 + length);
            next.edges.push(Edge {
                previous: predecessor,
                filler: Filler::Tree(tree),
                params: 0,
            });
            let target = ci as i64 + (length as i64 - partial) * self.cpb as i64;
            self.add_fresh(column_at(table, target)?, next);
            self.max_position = self.max_position.max(word_index as i64 + length as i64);
        }
        if can_continue {
            // The input ends inside the regex; keep it open for the next chunk.
            let check_len = cend - cstart;
            let mut next = self.copied(s);
            next.partial = check_len as u32;
            let tree = self.new_leaf(KIND_TERM, cstart as u32, cend as u32);
            next.edges.push(Edge {
                previous: predecessor,
                filler: Filler::Tree(tree),
                params: 0,
            });
            let target = ci as i64 + (check_len as i64 - partial) * self.cpb as i64;
            self.add_fresh(column_at(table, target)?, next);
        }
        Ok(())
    }

    /// `deepcopy(column)`: fresh copies of its states (edges shared).
    fn copy_column(&mut self, col: u32) -> u32 {
        let mut memo: FxHashMap<u32, u32> = FxHashMap::default();
        fn cp(core: &mut EarleyCore, memo: &mut FxHashMap<u32, u32>, s: u32) -> u32 {
            if let Some(&c) = memo.get(&s) {
                return c;
            }
            let st = core.states[s as usize].clone();
            let c = core.push_state(st);
            memo.insert(s, c);
            c
        }
        let old = self.columns[col as usize].clone();
        let mut new = Column {
            states: Vec::with_capacity(old.states.len()),
            predicted: old.predicted.clone(),
            ..Default::default()
        };
        for &s in &old.states {
            new.states.push(cp(self, &mut memo, s));
        }
        for (&sym, list) in &old.waiting {
            let l = list.iter().map(|&s| cp(self, &mut memo, s)).collect();
            new.waiting.insert(sym, l);
        }
        for (&k, &s) in &old.unique {
            let c = cp(self, &mut memo, s);
            new.unique.insert(k, c);
        }
        for (&sym, &entry) in &old.leo {
            if entry == NONE {
                new.leo.insert(sym, NONE);
                continue;
            }
            let (top, chain) = {
                let e = &self.leo_entries[entry as usize];
                (e.top, e.chain)
            };
            let top = cp(self, &mut memo, top);
            let mut heads = Vec::new();
            let mut c = chain;
            while c != NONE {
                heads.push(self.chains[c as usize].head);
                c = self.chains[c as usize].tail;
            }
            let mut new_chain = NONE;
            for &h in heads.iter().rev() {
                let head = cp(self, &mut memo, h);
                self.chains.push(ChainNode {
                    head,
                    tail: new_chain,
                });
                new_chain = self.chains.len() as u32 - 1;
            }
            self.leo_entries.push(LeoEntry {
                top,
                chain: new_chain,
            });
            new.leo.insert(sym, self.leo_entries.len() as u32 - 1);
        }
        for (&sym, list) in &old.empty_completions {
            let l = list.iter().map(|&s| cp(self, &mut memo, s)).collect();
            new.empty_completions.insert(sym, l);
        }
        self.columns.push(new);
        self.columns.len() as u32 - 1
    }

    fn new_column(&mut self) -> u32 {
        self.columns.push(Column::default());
        self.columns.len() as u32 - 1
    }

    fn consume_impl(&mut self, py: Python<'_>, word: &[u32]) -> PyResult<()> {
        let consumed = self.consumed;
        self.chunk_start = consumed;
        self.consumed = consumed + word.len();
        self.input.extend_from_slice(word);
        let cpb = self.cpb;
        let mut table = self.saved.clone();
        for _ in 0..word.len() * cpb {
            let c = self.new_column();
            table.push(c);
        }
        if self.first_consume {
            let col = *table
                .get(self.column_index)
                .ok_or_else(|| PyIndexError::new_err("list index out of range"))?;
            self.add_fresh(
                col,
                State {
                    nt: self.implicit_start,
                    position: 0,
                    alt: self.start_alt,
                    dot: 0,
                    partial: 0,
                    fc: false,
                    edges: SmallVec::new(),
                },
            );
            self.first_consume = false;
        }
        let mut ci = self.column_index;
        let mut word_index = 0usize;
        while ci < table.len() {
            let bit_position = 7 - (ci % 8);
            if ci == table.len() - 1 {
                let mut saved = table.clone();
                let last = *table.last().unwrap();
                *saved.last_mut().unwrap() = self.copy_column(last);
                self.saved = saved;
                self.column_index = ci;
            }
            let at_end = word_index >= word.len();
            let offset = (consumed + word_index) as i64;
            let col = table[ci] as usize;
            let mut i = 0;
            while i < self.columns[col].states.len() {
                let s = self.columns[col].states[i];
                i += 1;
                if self.is_finished(s) {
                    if self.st(s).nt == self.implicit_start && (ci % cpb == 0 || at_end) {
                        let key = self.key(s);
                        self.completed.entry(offset).or_default().insert(key, s);
                    }
                    self.complete(s, &table, ci, None);
                    continue;
                }
                if self.st(s).partial == 0 && self.next_is_nonterminal(s) {
                    self.predict(py, s, &table, ci, true)?;
                    continue;
                }
                let Some((sym, _)) = self.next_sym(s) else {
                    return Err(PyAssertionError::new_err("scan without next symbol"));
                };
                match &self.syms[sym as usize].kind {
                    SymKind::Bits(bits) => {
                        let bits = *bits;
                        self.scan_bit(s, bits, word, &table, ci, word_index, bit_position)?;
                    }
                    SymKind::Regex => {
                        self.scan_regex(py, s, sym, &table, ci, word_index)?;
                    }
                    SymKind::Literal(lit) => {
                        let lit = Arc::clone(lit);
                        self.scan_bytes(s, word.len(), &table, ci, word_index, &lit)?;
                    }
                    _ => {
                        return Err(PyAssertionError::new_err("cannot scan this terminal"));
                    }
                }
            }

            if self.incomplete_mode && at_end {
                let mut i = 0;
                while i < self.columns[col].states.len() {
                    let s = self.columns[col].states[i];
                    i += 1;
                    if self.is_finished(s) {
                        continue;
                    }
                    if self.st(s).nt == self.implicit_start {
                        if self.has_children(s) {
                            let key = self.key(s);
                            self.incomplete.entry(offset).or_default().insert(key, s);
                        }
                        continue;
                    }
                    if self.has_children(s) || (offset == 0 && !self.next_is_nonterminal(s)) {
                        self.complete(s, &table, ci, None);
                    }
                }
            }

            ci += 1;
            if ci % cpb == 0 {
                word_index += 1;
            }
        }
        Ok(())
    }

    // ----- forest ------------------------------------------------------------

    fn new_leaf(&mut self, kind: u32, a: u32, b: u32) -> u32 {
        self.nodes.push(Node {
            kind,
            a,
            b,
            cstart: 0,
            clen: 0,
        });
        self.nodes.len() as u32 - 1
    }

    fn new_inner(&mut self, sym: u32, params: u32, children: &[u32]) -> u32 {
        let cstart = self.node_children.len() as u32;
        self.node_children.extend_from_slice(children);
        self.nodes.push(Node {
            kind: KIND_NT,
            a: sym,
            b: params,
            cstart,
            clen: children.len() as u32,
        });
        self.nodes.len() as u32 - 1
    }

    /// `ForestBuilder._wrap_completed`, appended to `out`.
    fn wrap_completed_into(&mut self, nt: u32, children: &[u32], params: u32, out: &mut Vec<u32>) {
        if self.syms[nt as usize].in_rules {
            let n = self.new_inner(nt, params, children);
            out.push(n);
        } else {
            out.extend_from_slice(children);
        }
    }

    fn nest_states(&self, n: u32) -> Vec<u32> {
        let nest = &self.nests[n as usize];
        let mut needed = vec![nest.inner];
        let mut c = nest.chain;
        while c != NONE {
            needed.push(self.chains[c as usize].head);
            c = self.chains[c as usize].tail;
        }
        needed
    }

    /// `resolve` of `children_of`: cached mode when `built` is None.
    fn resolve(
        &mut self,
        target: u32,
        built: Option<&mut FxHashMap<u32, Arc<Vec<u32>>>>,
    ) -> Arc<Vec<u32>> {
        match built {
            None => self
                .children_cache
                .get(&target)
                .cloned()
                .unwrap_or_else(empty_rc),
            Some(b) => match b.remove(&target) {
                Some(c) => c,
                None => self.children_cached(target),
            },
        }
    }

    /// `ForestBuilder._expand_leo`.
    fn expand_leo(
        &mut self,
        n: u32,
        mut built: Option<&mut FxHashMap<u32, Arc<Vec<u32>>>>,
    ) -> Vec<u32> {
        let (chain, inner, top_params) = {
            let nest = &self.nests[n as usize];
            (nest.chain, nest.inner, nest.top_params)
        };
        let params = if chain != NONE {
            self.next_params(self.chains[chain as usize].head)
        } else {
            top_params
        };
        let inner_children = self.resolve(inner, built.as_deref_mut());
        let mut first = Vec::new();
        let inner_nt = self.st(inner).nt;
        self.wrap_completed_into(inner_nt, &inner_children, params, &mut first);
        let mut segments: Vec<Vec<u32>> = vec![first];
        let mut node = chain;
        while node != NONE {
            let (waiter, rest) = {
                let c = &self.chains[node as usize];
                (c.head, c.tail)
            };
            let waiter_nt = self.st(waiter).nt;
            if self.syms[waiter_nt as usize].in_rules {
                let mut children: Vec<u32> = self.resolve(waiter, built.as_deref_mut()).to_vec();
                for segment in segments.iter().rev() {
                    children.extend_from_slice(segment);
                }
                let parent_params = if rest != NONE {
                    self.next_params(self.chains[rest as usize].head)
                } else {
                    top_params
                };
                let mut wrapped = Vec::new();
                self.wrap_completed_into(waiter_nt, &children, parent_params, &mut wrapped);
                segments = vec![wrapped];
            } else {
                let r = self.resolve(waiter, built.as_deref_mut());
                segments.push(r.to_vec());
            }
            node = rest;
        }
        let mut payload = Vec::new();
        for segment in segments.iter().rev() {
            payload.extend_from_slice(segment);
        }
        payload
    }

    /// `ForestBuilder.children_of(state)` (no choices; cached).
    fn children_cached(&mut self, state: u32) -> Arc<Vec<u32>> {
        if let Some(c) = self.children_cache.get(&state) {
            return c.clone();
        }
        let mut in_progress: FxHashSet<u32> = FxHashSet::default();
        let mut pending: Vec<Frame> = vec![Frame::new(state)];
        in_progress.insert(state);
        while !pending.is_empty() {
            let top = pending.len() - 1;
            if pending[top].path.is_none() {
                // `_path` without choices: the first edge all the way back.
                let mut path = Vec::new();
                let mut current = pending[top].state;
                while current != NONE {
                    let Some(&edge) = self.st(current).edges.first() else {
                        break;
                    };
                    path.push(edge);
                    current = edge.previous;
                }
                pending[top].path = Some(path);
            }
            let mut descend: Vec<u32> = Vec::new();
            let mut path = pending[top].path.take().unwrap();
            let mut children = std::mem::take(&mut pending[top].children);
            while let Some(edge) = path.pop() {
                match edge.filler {
                    Filler::Tree(t) => children.push(t),
                    Filler::List(l) => children.extend_from_slice(&self.lists[l as usize]),
                    Filler::Leo(n) => {
                        let missing: Vec<u32> = self
                            .nest_states(n)
                            .into_iter()
                            .filter(|needed| {
                                !self.children_cache.contains_key(needed)
                                    && !in_progress.contains(needed)
                            })
                            .collect();
                        if !missing.is_empty() {
                            path.push(edge);
                            descend.extend(missing.iter().rev());
                            break;
                        }
                        let payload = self.expand_leo(n, None);
                        children.extend_from_slice(&payload);
                    }
                    Filler::State(f) => {
                        let filler_children = if let Some(c) = self.children_cache.get(&f) {
                            c.clone()
                        } else if in_progress.contains(&f) {
                            empty_rc()
                        } else {
                            path.push(edge);
                            descend.push(f);
                            break;
                        };
                        let nt = self.st(f).nt;
                        self.wrap_completed_into(nt, &filler_children, edge.params, &mut children);
                    }
                }
            }
            pending[top].path = Some(path);
            pending[top].children = children;
            if !descend.is_empty() {
                for d in descend {
                    pending.push(Frame::new(d));
                    in_progress.insert(d);
                }
                continue;
            }
            let frame = pending.pop().unwrap();
            in_progress.remove(&frame.state);
            self.children_cache
                .insert(frame.state, Arc::new(frame.children));
        }
        self.children_cache
            .get(&state)
            .cloned()
            .unwrap_or_else(empty_rc)
    }

    /// `ForestBuilder._is_ambiguous`.
    fn is_ambiguous(&mut self, state: u32) -> bool {
        if let Some(&c) = self.ambiguous_cache.get(&state) {
            return c;
        }
        let mut seen: FxHashSet<u32> = FxHashSet::default();
        let mut stack = vec![state];
        let mut found = false;
        while let Some(current) = stack.pop() {
            if seen.contains(&current) || self.ambiguous_cache.get(&current) == Some(&false) {
                continue;
            }
            seen.insert(current);
            if self.st(current).edges.len() > 1 {
                found = true;
                break;
            }
            self.push_linked_states(current, &mut stack);
        }
        if !found {
            for s in seen {
                self.ambiguous_cache.insert(s, false);
            }
        }
        found
    }

    /// `ForestBuilder.children_of(state, choices)`.
    fn children_choices(&mut self, state: u32, choices: &mut Choices) -> Arc<Vec<u32>> {
        let mut built: FxHashMap<u32, Arc<Vec<u32>>> = FxHashMap::default();
        let mut pending: Vec<Frame> = vec![Frame::new(state)];
        while !pending.is_empty() {
            let top = pending.len() - 1;
            if pending[top].path.is_none() {
                // `_path` with choices.
                let mut path = Vec::new();
                let mut prefix: Vec<u32> = Vec::new();
                let frame_state = pending[top].state;
                let mut current = frame_state;
                while current != NONE && !self.st(current).edges.is_empty() {
                    if current != frame_state && !self.is_ambiguous(current) {
                        prefix = self.children_cached(current).to_vec();
                        break;
                    }
                    let edges = &self.st(current).edges;
                    let edge = if edges.len() == 1 {
                        edges[0]
                    } else {
                        let fork = choices.edge_counts.len();
                        choices.edge_counts.push(edges.len());
                        let pick = if fork < choices.picks.len() {
                            choices.picks[fork]
                        } else {
                            0
                        };
                        edges[pick]
                    };
                    path.push(edge);
                    current = edge.previous;
                }
                pending[top].path = Some(path);
                pending[top].children = prefix;
            }
            let mut descend: Vec<u32> = Vec::new();
            let mut path = pending[top].path.take().unwrap();
            let mut children = std::mem::take(&mut pending[top].children);
            while let Some(edge) = path.pop() {
                match edge.filler {
                    Filler::Tree(t) => children.push(t),
                    Filler::List(l) => children.extend_from_slice(&self.lists[l as usize]),
                    Filler::Leo(n) => {
                        let mut missing = Vec::new();
                        for needed in self.nest_states(n) {
                            let ready = built.contains_key(&needed) || !self.is_ambiguous(needed);
                            if !ready {
                                missing.push(needed);
                            }
                        }
                        if !missing.is_empty() {
                            path.push(edge);
                            descend.extend(missing.iter().rev());
                            break;
                        }
                        let payload = self.expand_leo(n, Some(&mut built));
                        children.extend_from_slice(&payload);
                    }
                    Filler::State(f) => {
                        let ready = built.contains_key(&f) || !self.is_ambiguous(f);
                        if !ready {
                            path.push(edge);
                            descend.push(f);
                            break;
                        }
                        let filler_children = self.resolve(f, Some(&mut built));
                        let nt = self.st(f).nt;
                        self.wrap_completed_into(nt, &filler_children, edge.params, &mut children);
                    }
                }
            }
            pending[top].path = Some(path);
            pending[top].children = children;
            if !descend.is_empty() {
                for d in descend {
                    pending.push(Frame::new(d));
                }
                continue;
            }
            let frame = pending.pop().unwrap();
            built.insert(frame.state, Arc::new(frame.children));
        }
        self.resolve(state, Some(&mut built))
    }

    /// Preorder records `[node, kind, a, b, n_children]` of the trees
    /// `roots` (shared nodes repeated), prefixed by the number of roots.
    /// The node ids let Python reproduce which tree objects are shared.
    fn flatten(&self, roots: &[u32]) -> Vec<u32> {
        let mut out = Vec::with_capacity(1 + roots.len() * 5);
        out.push(roots.len() as u32);
        let mut stack: Vec<u32> = roots.iter().rev().copied().collect();
        while let Some(n) = stack.pop() {
            let node = self.nodes[n as usize];
            out.extend_from_slice(&[n, node.kind, node.a, node.b, node.clen]);
            let cs = node.cstart as usize;
            for i in (0..node.clen as usize).rev() {
                stack.push(self.node_children[cs + i]);
            }
        }
        out
    }

    /// A 128 bit structural fingerprint of the tree: equal trees (same
    /// symbols, parameters and terminal values) have the same fingerprint.
    /// Stands in for `hash(tree)` when dropping duplicate derivations.
    fn fingerprint(&self, root: u32) -> u128 {
        let mut memo: FxHashMap<u32, u128> = FxHashMap::default();
        let mut stack: Vec<(u32, bool)> = vec![(root, false)];
        let mut buf: Vec<u8> = Vec::new();
        while let Some((n, expanded)) = stack.pop() {
            if memo.contains_key(&n) {
                continue;
            }
            let node = self.nodes[n as usize];
            let cs = node.cstart as usize;
            if !expanded && node.clen > 0 {
                stack.push((n, true));
                for i in 0..node.clen as usize {
                    stack.push((self.node_children[cs + i], false));
                }
                continue;
            }
            buf.clear();
            buf.extend_from_slice(&node.kind.to_le_bytes());
            match node.kind {
                KIND_TERM => {
                    for &u in &self.input[node.a as usize..node.b as usize] {
                        buf.extend_from_slice(&u.to_le_bytes());
                    }
                }
                _ => {
                    buf.extend_from_slice(&node.a.to_le_bytes());
                    buf.extend_from_slice(&node.b.to_le_bytes());
                    for i in 0..node.clen as usize {
                        let c = memo[&self.node_children[cs + i]];
                        buf.extend_from_slice(&c.to_le_bytes());
                    }
                }
            }
            memo.insert(n, xxhash_rust::xxh3::xxh3_128(&buf));
        }
        memo[&root]
    }

    /// One step of `ForestBuilder.derivations_of`: the next derivation.
    fn advance(&mut self, handle: usize) -> PyResult<Option<u32>> {
        let (state, picks) = {
            let e = self
                .enumerators
                .get(handle)
                .ok_or_else(|| PyIndexError::new_err("no such enumerator"))?;
            if e.done {
                return Ok(None);
            }
            (e.state, e.picks.clone())
        };
        let mut choices = Choices {
            picks,
            edge_counts: Vec::new(),
        };
        let children = self.children_choices(state, &mut choices);
        if children.len() != 1 {
            return Err(PyValueError::new_err(format!(
                "expected 1 value to unpack, got {}",
                children.len()
            )));
        }
        let tree = children[0];
        let mut picks = choices.picks;
        let counts = choices.edge_counts;
        if counts.len() > picks.len() {
            picks.resize(counts.len(), 0);
        }
        while let Some(&last) = picks.last() {
            let idx = picks.len() - 1;
            let count = *counts
                .get(idx)
                .ok_or_else(|| PyIndexError::new_err("list index out of range"))?;
            if last + 1 == count {
                picks.pop();
            } else {
                break;
            }
        }
        let e = &mut self.enumerators[handle];
        if picks.is_empty() {
            e.done = true;
        } else {
            *picks.last_mut().unwrap() += 1;
        }
        e.picks = picks;
        Ok(Some(tree))
    }

    fn rep_info(&mut self, py: Python<'_>, ctx: &TreeContext, sym: u32) -> PyResult<()> {
        if self.rep_info.len() <= sym as usize {
            self.rep_info.resize_with(sym as usize + 1, || None);
        }
        if self.rep_info[sym as usize].is_none() {
            let (mode, node): (u8, Option<Py<PyAny>>) =
                ctx.repetition_cb.call1(py, (sym,))?.extract(py)?;
            let id = match &node {
                Some(n) => Some(n.getattr(py, intern!(py, "id"))?),
                None => None,
            };
            self.rep_info[sym as usize] = Some(RepInfo { mode, node, id });
        }
        Ok(())
    }

    /// `ForestBuilder.to_derivation_tree` of the derivation `root`.
    ///
    /// Python converts the trees by occurrence, in preorder (numbering the
    /// repetitions), and then builds them bottom-up, looking children up by
    /// node: a node occurring twice yields one shared object. Objects are
    /// created with exactly the attributes `DerivationTree.__init__` sets.
    fn build_tree(&mut self, py: Python<'_>, root: u32) -> PyResult<Py<PyAny>> {
        let ctx = match &self.tree_ctx {
            Some(c) => TreeContext {
                dt_class: c.dt_class.clone_ref(py),
                object_new: c.object_new.clone_ref(py),
                symbols: c.symbols.clone_ref(py),
                params: c.params.clone_ref(py),
                repetition_cb: c.repetition_cb.clone_ref(py),
                terminal_cb: c.terminal_cb.clone_ref(py),
            },
            None => return Err(PyValueError::new_err("tree context not set")),
        };

        // Preorder pass: (node, reps) per occurrence.
        struct Open<'py> {
            mode: u8,
            reps: Bound<'py, PyList>,
            id: Option<Bound<'py, PyAny>>,
            iteration: Option<Bound<'py, PyAny>>,
        }
        let mut occurrences: Vec<(u32, Bound<'_, PyList>)> = Vec::new();
        let mut opened: Vec<Open<'_>> = Vec::new();
        // (node, parent occurrence, index among the parent's children)
        let mut todo: Vec<(u32, usize, usize)> = vec![(root, usize::MAX, 0)];
        while let Some((n, parent, index)) = todo.pop() {
            let reps = if parent == usize::MAX {
                PyList::empty(py)
            } else {
                let p = &opened[parent];
                match p.mode {
                    REPS_RESET => PyList::empty(py),
                    REPS_INHERIT => PyList::new(py, p.reps.iter())?,
                    _ => {
                        let l = PyList::new(py, p.reps.iter())?;
                        let item = PyTuple::new(
                            py,
                            [
                                p.id.as_ref().unwrap().clone(),
                                p.iteration.as_ref().unwrap().clone(),
                                index.into_pyobject(py)?.into_any(),
                            ],
                        )?;
                        l.append(item)?;
                        l
                    }
                }
            };
            let node = self.nodes[n as usize];
            let mut open = Open {
                mode: REPS_RESET,
                reps: reps.clone(),
                id: None,
                iteration: None,
            };
            if node.kind == KIND_NT {
                self.rep_info(py, &ctx, node.a)?;
                let info = self.rep_info[node.a as usize].as_ref().unwrap();
                open.mode = info.mode;
                if info.mode == REPS_REPETITION {
                    let cf = info.node.as_ref().unwrap().bind(py);
                    let iteration = cf.getattr(intern!(py, "iteration"))?.add(1)?;
                    cf.setattr(intern!(py, "iteration"), &iteration)?;
                    open.id = Some(info.id.as_ref().unwrap().bind(py).clone());
                    open.iteration = Some(iteration);
                }
            }
            let occurrence = occurrences.len();
            occurrences.push((n, reps));
            opened.push(open);
            let cs = node.cstart as usize;
            for i in (0..node.clen as usize).rev() {
                todo.push((self.node_children[cs + i], occurrence, i));
            }
        }

        // Bottom-up pass.
        let symbols = ctx.symbols.bind(py);
        let params = ctx.params.bind(py);
        let none = py.None().into_bound(py);
        let falsy = false.into_pyobject(py)?.to_owned().into_any();
        let mut built: FxHashMap<u32, (Bound<'_, PyAny>, Bound<'_, PyDict>)> = FxHashMap::default();
        for (n, reps) in occurrences.into_iter().rev() {
            let node = self.nodes[n as usize];
            let (symbol, sender, recipient) = if node.kind == KIND_NT {
                let (sender, recipient): (Bound<'_, PyAny>, Bound<'_, PyAny>) =
                    params.get_item(node.b as usize)?.extract()?;
                (symbols.get_item(node.a as usize)?, sender, recipient)
            } else {
                let symbol = match self.terminal_objs.get(&n) {
                    Some(t) => t.bind(py).clone(),
                    None => {
                        let t = ctx
                            .terminal_cb
                            .bind(py)
                            .call1((n, node.kind, node.a, node.b))?;
                        self.terminal_objs.insert(n, t.clone().unbind());
                        t
                    }
                };
                (symbol, none.clone(), none.clone())
            };
            let sources = match self.sources_objs.get(&n) {
                Some(s) => s.bind(py).clone(),
                None => {
                    let s = PyList::empty(py).into_any();
                    self.sources_objs.insert(n, s.clone().unbind());
                    s
                }
            };
            let children = PyList::empty(py);
            let cs = node.cstart as usize;
            for i in 0..node.clen as usize {
                let child = &built[&self.node_children[cs + i]];
                children.append(&child.0)?;
            }
            let dict = PyDict::new(py);
            dict.set_item(intern!(py, "hash_cache"), &none)?;
            dict.set_item(intern!(py, "_parent"), &none)?;
            dict.set_item(intern!(py, "_sender"), sender)?;
            dict.set_item(intern!(py, "_recipient"), recipient)?;
            dict.set_item(intern!(py, "_symbol"), symbol)?;
            dict.set_item(intern!(py, "_children"), &children)?;
            dict.set_item(intern!(py, "_sources"), sources)?;
            dict.set_item(intern!(py, "origin_repetitions"), reps)?;
            dict.set_item(intern!(py, "read_only"), &falsy)?;
            dict.set_item(intern!(py, "_size"), &none)?;
            let obj = ctx.object_new.bind(py).call1((ctx.dt_class.bind(py),))?;
            obj.setattr(intern!(py, "__dict__"), &dict)?;
            for i in 0..node.clen as usize {
                let child = &built[&self.node_children[cs + i]];
                child.1.set_item(intern!(py, "_parent"), &obj)?;
            }
            built.insert(n, (obj, dict));
        }
        Ok(built.remove(&root).unwrap().0.unbind())
    }

    // ----- registration ------------------------------------------------------

    fn register_impl(&mut self, regs: &Bound<'_, PyTuple>) -> PyResult<()> {
        let syms: Vec<(u32, u8, i64, bool, bool, Bound<'_, PyAny>)> =
            regs.get_item(0)?.extract()?;
        let alts: Vec<(u32, u32, Vec<(u32, u32)>, i64)> = regs.get_item(1)?.extract()?;
        let rules: Vec<(u32, Vec<u32>)> = regs.get_item(2)?.extract()?;
        for (id, kind, hash, in_rules, is_ctx, payload) in syms {
            let kind = match kind {
                0 => SymKind::NonTerminal,
                1 => SymKind::Literal(payload.extract::<Vec<u32>>()?.into()),
                2 => SymKind::Regex,
                3 => {
                    let (b0, b1): (bool, bool) = payload.extract()?;
                    SymKind::Bits([b0, b1])
                }
                _ => SymKind::Invalid,
            };
            let sym = Sym {
                kind,
                hash,
                in_rules,
                is_ctx,
            };
            if id as usize != self.syms.len() {
                return Err(PyValueError::new_err("symbols must be registered in order"));
            }
            self.syms.push(sym);
        }
        for (id, eq, syms, first_hash) in alts {
            if id as usize != self.alts.len() {
                return Err(PyValueError::new_err(
                    "alternatives must be registered in order",
                ));
            }
            self.alts.push(Alt {
                syms,
                eq,
                first_hash,
            });
        }
        for (sym, alt_ids) in rules {
            if self.rules.len() <= sym as usize {
                self.rules.resize(sym as usize + 1, None);
            }
            self.rules[sym as usize] = Some(Arc::new(alt_ids));
        }
        Ok(())
    }

    fn reset_parse(&mut self) {
        self.states.clear();
        self.columns.clear();
        self.saved.clear();
        self.completed.clear();
        self.incomplete.clear();
        self.chains.clear();
        self.leo_entries.clear();
        self.nests.clear();
        self.lists.clear();
        self.nodes.clear();
        self.node_children.clear();
        self.children_cache.clear();
        self.ambiguous_cache.clear();
        self.enumerators.clear();
        self.sessions.clear();
        self.terminal_objs.clear();
        self.sources_objs.clear();
        self.regex_cache.clear();
        self.input.clear();
        self.mark.clear();
        self.mark_gen = 0;
    }
}

fn u32_bytes(v: &[u32]) -> &[u8] {
    // SAFETY: u32 has no padding; the slice covers exactly the same memory.
    unsafe { std::slice::from_raw_parts(v.as_ptr() as *const u8, std::mem::size_of_val(v)) }
}

#[pymethods]
impl EarleyCore {
    #[new]
    fn py_new(hash_none: i64) -> Self {
        EarleyCore {
            syms: Vec::new(),
            alts: Vec::new(),
            rules: Vec::new(),
            hash_none,
            states: Vec::new(),
            columns: Vec::new(),
            saved: Vec::new(),
            column_index: 0,
            cpb: 1,
            incomplete_mode: false,
            first_consume: true,
            start_alt: 0,
            implicit_start: 0,
            consumed: 0,
            chunk_start: 0,
            max_position: -1,
            input: Vec::new(),
            completed: FxIndexMap::default(),
            incomplete: FxIndexMap::default(),
            chains: Vec::new(),
            leo_entries: Vec::new(),
            nests: Vec::new(),
            lists: Vec::new(),
            nodes: Vec::new(),
            node_children: Vec::new(),
            children_cache: FxHashMap::default(),
            ambiguous_cache: FxHashMap::default(),
            enumerators: Vec::new(),
            sessions: Vec::new(),
            tree_ctx: None,
            rep_info: Vec::new(),
            terminal_objs: FxHashMap::default(),
            sources_objs: FxHashMap::default(),
            regex_cb: None,
            ctx_cb: None,
            regex_cache: FxHashMap::default(),
            mark: Vec::new(),
            mark_gen: 0,
        }
    }

    /// Register symbols, alternatives and rules:
    /// `(syms, alts, rules)` with
    /// `syms = [(id, kind, hash, in_rules, is_ctx, payload)]`,
    /// `alts = [(id, eq, [(sym, params)], first_hash)]`,
    /// `rules = [(sym, [alt])]`.
    fn register(&mut self, regs: &Bound<'_, PyTuple>) -> PyResult<()> {
        self.register_impl(regs)
    }

    fn new_parse(
        &mut self,
        implicit_start: u32,
        start_alt: u32,
        incomplete: bool,
        cpb: usize,
        column_index: usize,
    ) {
        self.reset_parse();
        self.implicit_start = implicit_start;
        self.start_alt = start_alt;
        self.incomplete_mode = incomplete;
        self.cpb = cpb;
        self.column_index = column_index;
        let c = self.new_column();
        self.saved.push(c);
        self.first_consume = true;
        self.max_position = -1;
        self.consumed = 0;
    }

    /// Continue the parse with `data`: UTF-32-LE code points if `is_str`,
    /// else raw bytes.
    fn consume(
        &mut self,
        py: Python<'_>,
        data: &[u8],
        is_str: bool,
        regex_cb: Py<PyAny>,
        ctx_cb: Py<PyAny>,
    ) -> PyResult<()> {
        let word: Vec<u32> = if is_str {
            data.chunks_exact(4)
                .map(|c| u32::from_le_bytes([c[0], c[1], c[2], c[3]]))
                .collect()
        } else {
            data.iter().map(|&b| b as u32).collect()
        };
        self.regex_cb = Some(regex_cb);
        self.ctx_cb = Some(ctx_cb);
        let result = self.consume_impl(py, &word);
        self.regex_cb = None;
        self.ctx_cb = None;
        result
    }

    fn can_continue(&mut self) -> bool {
        if self.saved.len() <= 1 {
            return true;
        }
        let mut table = self.saved.clone();
        let ci = self.column_index;
        table[ci] = self.copy_column(self.saved[ci]);
        let col = table[ci] as usize;
        let mut i = 0;
        while i < self.columns[col].states.len() {
            let s = self.columns[col].states[i];
            i += 1;
            if self.is_finished(s) {
                self.complete(s, &table, ci, None);
            }
        }
        self.columns[col]
            .states
            .iter()
            .any(|&s| self.st(s).partial > 0 || !self.is_finished(s))
    }

    fn parsed_positions(&self) -> Vec<i64> {
        self.completed.keys().copied().collect()
    }

    /// The states `tree_at` enumerates, as `(state, is_complete)`.
    fn flagged(&self, offset: i64, incomplete: bool) -> Vec<(u32, bool)> {
        let mut out: Vec<(u32, bool)> = self
            .completed
            .get(&offset)
            .map(|m| m.values().map(|&s| (s, true)).collect())
            .unwrap_or_default();
        if incomplete {
            if let Some(m) = self.incomplete.get(&offset) {
                out.extend(m.values().map(|&s| (s, false)));
            }
        }
        out
    }

    /// Start enumerating the derivations of `state` (`derivations_of`).
    fn derivations(&mut self, state: u32) -> usize {
        self.enumerators.push(Enumerator {
            state,
            picks: Vec::new(),
            done: false,
        });
        self.enumerators.len() - 1
    }

    /// Objects the tree building needs: the `DerivationTree` class, the
    /// symbol list (indexed by symbol id), `(sender, recipient)` per params
    /// id, and callbacks for repetition info per symbol and terminal
    /// symbols per tree node.
    fn set_tree_context(
        &mut self,
        py: Python<'_>,
        dt_class: Py<PyAny>,
        symbols: Py<PyList>,
        params: Py<PyList>,
        repetition_cb: Py<PyAny>,
        terminal_cb: Py<PyAny>,
    ) -> PyResult<()> {
        let object_new = py
            .import("builtins")?
            .getattr("object")?
            .getattr("__new__")?
            .unbind();
        self.tree_ctx = Some(TreeContext {
            dt_class,
            object_new,
            symbols,
            params,
            repetition_cb,
            terminal_cb,
        });
        Ok(())
    }

    /// Start `tree_at(offset, incomplete=incomplete)`.
    fn tree_at_start(&mut self, offset: i64, incomplete: bool) -> usize {
        let flagged = self.flagged(offset, incomplete);
        self.sessions.push(TreeAtSession {
            flagged,
            index: 0,
            enumerator: None,
            seen: FxHashSet::default(),
        });
        self.sessions.len() - 1
    }

    /// The next `(DerivationTree, is_complete)` of a `tree_at` session.
    fn tree_at_next<'py>(
        &mut self,
        py: Python<'py>,
        session: usize,
    ) -> PyResult<Option<(Py<PyAny>, bool)>> {
        loop {
            let (state, flag, enumerator) = {
                let s = self
                    .sessions
                    .get(session)
                    .ok_or_else(|| PyIndexError::new_err("no such session"))?;
                let Some(&(state, flag)) = s.flagged.get(s.index) else {
                    return Ok(None);
                };
                (state, flag, s.enumerator)
            };
            let enumerator = match enumerator {
                Some(e) => e,
                None => {
                    let e = self.derivations(state);
                    self.sessions[session].enumerator = Some(e);
                    e
                }
            };
            let Some(root) = self.advance(enumerator)? else {
                let s = &mut self.sessions[session];
                s.enumerator = None;
                s.index += 1;
                continue;
            };
            let fp = self.fingerprint(root);
            if !self.sessions[session].seen.insert((fp, flag)) {
                continue;
            }
            let tree = self.build_tree(py, root)?;
            return Ok(Some((tree, flag)));
        }
    }

    /// The chain for `current_tree()`, or None.
    fn current_tree_chain<'py>(&mut self, py: Python<'py>) -> PyResult<Option<Bound<'py, PyList>>> {
        let saved = self.saved.clone();
        if self.columns[saved[self.column_index] as usize]
            .states
            .is_empty()
        {
            return Ok(None);
        }
        for &col in saved.iter().rev() {
            let Some(&last) = self.columns[col as usize].states.last() else {
                continue;
            };
            let chain = self.incomplete_chain(last, &saved)?;
            return Ok(Some(self.chain_to_py(py, &chain)?));
        }
        Ok(None)
    }

    fn max_position(&self) -> i64 {
        self.max_position
    }

    /// Sizes of the internal arenas, for diagnostics.
    fn stats(&self) -> (usize, usize, usize, usize) {
        (
            self.states.len(),
            self.columns.len(),
            self.nodes.len(),
            self.regex_cache.len(),
        )
    }

    /// The saved table with every edge, for differential testing.
    /// Per column a list of `(state, [edge])`, where a state is
    /// `(nt, position, alt, dot, partial, fc)` and an edge is
    /// `(previous state or None, kind, payload, params)` with kind
    /// 0 = tree `(node, node kind, a, b)`, 1 = state, 2 = Leo nest
    /// `(inner, [chain heads], top_params)`, 3 = list (flattened trees).
    fn dump_table<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let desc = |s: u32| -> (u32, u32, u32, u32, u32, bool) {
            let st = self.st(s);
            (st.nt, st.position, st.alt, st.dot, st.partial, st.fc)
        };
        let out = PyList::empty(py);
        for &c in &self.saved {
            let col = PyList::empty(py);
            for &s in &self.columns[c as usize].states {
                let edges = PyList::empty(py);
                for e in self.st(s).edges.iter() {
                    let prev = if e.previous == NONE {
                        py.None().into_bound(py)
                    } else {
                        desc(e.previous).into_pyobject(py)?.into_any()
                    };
                    let (kind, payload): (u32, Bound<'py, PyAny>) = match e.filler {
                        Filler::Tree(t) => {
                            let n = self.nodes[t as usize];
                            (0, (t, n.kind, n.a, n.b).into_pyobject(py)?.into_any())
                        }
                        Filler::State(f) => (1, desc(f).into_pyobject(py)?.into_any()),
                        Filler::Leo(n) => {
                            let nest = &self.nests[n as usize];
                            let mut heads = Vec::new();
                            let mut ch = nest.chain;
                            while ch != NONE {
                                heads.push(desc(self.chains[ch as usize].head));
                                ch = self.chains[ch as usize].tail;
                            }
                            (
                                2,
                                (desc(nest.inner), heads, nest.top_params)
                                    .into_pyobject(py)?
                                    .into_any(),
                            )
                        }
                        Filler::List(l) => {
                            let flat = self.flatten(&self.lists[l as usize]);
                            (3, PyBytes::new(py, u32_bytes(&flat)).into_any())
                        }
                    };
                    edges.append((prev, kind, payload, e.params))?;
                }
                col.append((desc(s), edges))?;
            }
            out.append(col)?;
        }
        Ok(out)
    }

    /// Let Python's garbage collector see the objects held here: the tree
    /// context refers back to the Python parser, which holds this core.
    fn __traverse__(&self, visit: PyVisit<'_>) -> Result<(), PyTraverseError> {
        if let Some(ctx) = &self.tree_ctx {
            visit.call(&ctx.dt_class)?;
            visit.call(&ctx.object_new)?;
            visit.call(&ctx.symbols)?;
            visit.call(&ctx.params)?;
            visit.call(&ctx.repetition_cb)?;
            visit.call(&ctx.terminal_cb)?;
        }
        for info in self.rep_info.iter().flatten() {
            if let Some(node) = &info.node {
                visit.call(node)?;
            }
            if let Some(id) = &info.id {
                visit.call(id)?;
            }
        }
        for obj in self.terminal_objs.values().chain(self.sources_objs.values()) {
            visit.call(obj)?;
        }
        if let Some(cb) = &self.regex_cb {
            visit.call(cb)?;
        }
        if let Some(cb) = &self.ctx_cb {
            visit.call(cb)?;
        }
        Ok(())
    }

    fn __clear__(&mut self) {
        self.tree_ctx = None;
        self.rep_info.clear();
        self.terminal_objs.clear();
        self.sources_objs.clear();
        self.regex_cb = None;
        self.ctx_cb = None;
    }

    #[getter]
    fn hash_none(&self) -> i64 {
        self.hash_none
    }
}

/// Reads the attributes of a tree node: straight from the instance dict
/// for the classes whose properties just return them, else via getattr.
struct NodeReader<'py> {
    fast: [Bound<'py, PyAny>; 2],
}

impl<'py> NodeReader<'py> {
    fn get(
        &self,
        node: &Bound<'py, PyAny>,
        dict: &Option<Bound<'py, PyDict>>,
        private: &Bound<'py, PyString>,
        public: &Bound<'py, PyString>,
    ) -> PyResult<Bound<'py, PyAny>> {
        if let Some(d) = dict {
            if let Some(v) = d.get_item(private)? {
                return Ok(v);
            }
        }
        node.getattr(public)
    }

    fn dict(&self, node: &Bound<'py, PyAny>) -> PyResult<Option<Bound<'py, PyDict>>> {
        let t = node.get_type();
        if self.fast.iter().any(|f| f.is(&t)) {
            Ok(Some(
                node.getattr(intern!(node.py(), "__dict__"))?
                    .cast_into::<PyDict>()?,
            ))
        } else {
            Ok(None)
        }
    }
}

/// `ForestBuilder._collapse(tree)[0]`: drop control-flow nodes (`<__...>`).
/// Same traversal, same objects shared, same `KeyError` where Python's
/// `collapsed.pop(id(child))` fails.
#[pyfunction]
fn collapse<'py>(
    py: Python<'py>,
    tree: Bound<'py, PyAny>,
    dt_class: Bound<'py, PyAny>,
    pdt_class: Bound<'py, PyAny>,
    nt_class: Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyAny>> {
    let reader = NodeReader {
        fast: [dt_class.clone(), pdt_class],
    };
    let k_children = (intern!(py, "_children"), intern!(py, "children"));
    let k_symbol = (intern!(py, "_symbol"), intern!(py, "symbol"));
    let k_sources = (intern!(py, "_sources"), intern!(py, "sources"));
    let k_read_only = (intern!(py, "read_only"), intern!(py, "read_only"));
    let k_recipient = (intern!(py, "_recipient"), intern!(py, "recipient"));
    let k_sender = (intern!(py, "_sender"), intern!(py, "sender"));
    let k_reps = (
        intern!(py, "origin_repetitions"),
        intern!(py, "origin_repetitions"),
    );
    let object_new = py
        .import("builtins")?
        .getattr("object")?
        .getattr("__new__")?;

    // (node, its dict if read directly, its children)
    let mut order: Vec<(
        Bound<'py, PyAny>,
        Option<Bound<'py, PyDict>>,
        Bound<'py, PyAny>,
    )> = Vec::new();
    let mut stack: Vec<Bound<'py, PyAny>> = vec![tree.clone()];
    while let Some(node) = stack.pop() {
        let dict = reader.dict(&node)?;
        let children = reader.get(&node, &dict, k_children.0, k_children.1)?;
        for child in children.try_iter()? {
            stack.push(child?);
        }
        order.push((node, dict, children));
    }

    let none = py.None().into_bound(py);
    let mut collapsed: FxHashMap<usize, Vec<Bound<'py, PyAny>>> = FxHashMap::default();
    let mut control_flow: FxHashMap<usize, bool> = FxHashMap::default();
    for (node, dict, children) in order.iter().rev() {
        let mut reduced: Vec<Bound<'py, PyAny>> = Vec::new();
        for child in children.try_iter()? {
            let child = child?;
            match collapsed.remove(&(child.as_ptr() as usize)) {
                Some(v) => reduced.extend(v),
                None => return Err(PyKeyError::new_err(child.as_ptr() as usize)),
            }
        }
        let symbol = reader.get(node, dict, k_symbol.0, k_symbol.1)?;
        let key = symbol.as_ptr() as usize;
        let is_control_flow = match control_flow.get(&key) {
            Some(&b) => b,
            None => {
                let b = symbol.is_instance(&nt_class)?
                    && symbol
                        .call_method0(intern!(py, "name"))?
                        .extract::<String>()?
                        .starts_with("<__");
                control_flow.insert(key, b);
                b
            }
        };
        if is_control_flow {
            collapsed.insert(node.as_ptr() as usize, reduced);
            continue;
        }
        // DerivationTree(node.symbol, children=reduced, sources=node.sources,
        //   read_only=node.read_only, recipient=node.recipient,
        //   sender=node.sender, origin_repetitions=node.origin_repetitions)
        let sources = reader.get(node, dict, k_sources.0, k_sources.1)?;
        let read_only = reader.get(node, dict, k_read_only.0, k_read_only.1)?;
        let recipient = reader.get(node, dict, k_recipient.0, k_recipient.1)?;
        let sender = reader.get(node, dict, k_sender.0, k_sender.1)?;
        let mut reps = reader.get(node, dict, k_reps.0, k_reps.1)?;
        if reps.is_none() {
            reps = PyList::empty(py).into_any();
        }
        let sources = if sources.is_none() {
            PyList::empty(py).into_any()
        } else {
            sources
        };
        let children_list = PyList::new(py, &reduced)?;
        let new_dict = PyDict::new(py);
        new_dict.set_item(intern!(py, "hash_cache"), &none)?;
        new_dict.set_item(intern!(py, "_parent"), &none)?;
        new_dict.set_item(intern!(py, "_sender"), sender)?;
        new_dict.set_item(intern!(py, "_recipient"), recipient)?;
        new_dict.set_item(intern!(py, "_symbol"), symbol)?;
        new_dict.set_item(intern!(py, "_children"), &children_list)?;
        new_dict.set_item(intern!(py, "_sources"), &sources)?;
        new_dict.set_item(intern!(py, "origin_repetitions"), reps)?;
        new_dict.set_item(intern!(py, "read_only"), read_only)?;
        new_dict.set_item(intern!(py, "_size"), &none)?;
        let obj = object_new.call1((&dt_class,))?;
        obj.setattr(intern!(py, "__dict__"), &new_dict)?;
        for source in sources.try_iter()? {
            source?.setattr(intern!(py, "_parent"), &obj)?;
        }
        for child in &reduced {
            child.setattr(intern!(py, "_parent"), &obj)?;
        }
        collapsed.insert(node.as_ptr() as usize, vec![obj]);
    }
    let mut result = collapsed
        .remove(&(tree.as_ptr() as usize))
        .unwrap_or_default();
    if result.is_empty() {
        return Err(PyIndexError::new_err("list index out of range"));
    }
    Ok(result.swap_remove(0))
}

#[pymodule]
fn fandango_earley_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<EarleyCore>()?;
    m.add_function(wrap_pyfunction!(collapse, m)?)?;
    Ok(())
}
