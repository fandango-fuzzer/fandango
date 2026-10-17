//! Bit-exact replicas of the CPython hashing / set-ordering behavior the
//! Python parser implicitly depends on.
//!
//! `IterativeParser.predict` adds the predicted items of a non-terminal as
//! `table[i].update({ParseState(...) for alternative in alternatives})`, i.e.
//! in the iteration order of a freshly built `set`. That order depends on
//! `ParseState.__hash__`, which is a tuple hash over the (randomized) symbol
//! hashes and the column index. To add items in exactly the same order, we
//! recompute that tuple hash and simulate CPython's set insertion.
//! (Verified against CPython 3.11 to 3.14.)

const XXPRIME_1: u64 = 11400714785074694791;
const XXPRIME_2: u64 = 14029467366897019727;
const XXPRIME_5: u64 = 2870177450012600261;

/// `hash(tuple)` given the hashes of its items (CPython >= 3.8, 64 bit).
pub fn tuple_hash(items: &[i64]) -> i64 {
    let mut acc = XXPRIME_5;
    for &h in items {
        acc = acc.wrapping_add((h as u64).wrapping_mul(XXPRIME_2));
        acc = acc.rotate_left(31);
        acc = acc.wrapping_mul(XXPRIME_1);
    }
    acc = acc.wrapping_add((items.len() as u64) ^ (XXPRIME_5 ^ 3527539));
    if acc == u64::MAX {
        return 1546275796;
    }
    acc as i64
}

const EMPTY: u32 = u32::MAX;
const LINEAR_PROBES: usize = 9;
const PERTURB_SHIFT: u32 = 5;
const MINSIZE: usize = 8;

fn insert_clean(table: &mut [u32], mask: usize, idx: u32, hash: i64) {
    let mut perturb = hash as u64 as usize;
    let mut i = (hash as u64 as usize) & mask;
    loop {
        if table[i] == EMPTY {
            table[i] = idx;
            return;
        }
        if i + LINEAR_PROBES <= mask {
            for j in 1..=LINEAR_PROBES {
                if table[i + j] == EMPTY {
                    table[i + j] = idx;
                    return;
                }
            }
        }
        perturb >>= PERTURB_SHIFT;
        i = (i.wrapping_mul(5).wrapping_add(1).wrapping_add(perturb)) & mask;
    }
}

/// The order in which a `set` built by adding pairwise-unequal elements with
/// the given hashes (in that order) iterates them.
pub fn set_iteration_order(hashes: &[i64]) -> Vec<usize> {
    let mut mask: usize = MINSIZE - 1;
    let mut table: Vec<u32> = vec![EMPTY; MINSIZE];
    let mut fill = 0usize;
    for (idx, &h) in hashes.iter().enumerate() {
        let mut perturb = h as u64 as usize;
        let mut i = (h as u64 as usize) & mask;
        'probe: loop {
            let probes = if i + LINEAR_PROBES <= mask {
                LINEAR_PROBES
            } else {
                0
            };
            for j in 0..=probes {
                if table[i + j] == EMPTY {
                    table[i + j] = idx as u32;
                    break 'probe;
                }
                // Occupied: elements are pairwise unequal, so keep probing.
            }
            perturb >>= PERTURB_SHIFT;
            i = (i.wrapping_mul(5).wrapping_add(1).wrapping_add(perturb)) & mask;
        }
        fill += 1;
        if fill * 5 >= mask * 3 {
            let used = fill;
            let minused = if used > 50000 { used * 2 } else { used * 4 };
            let mut newsize = MINSIZE;
            while newsize <= minused {
                newsize <<= 1;
            }
            let old = std::mem::replace(&mut table, vec![EMPTY; newsize]);
            mask = newsize - 1;
            for e in old {
                if e != EMPTY {
                    insert_clean(&mut table, mask, e, hashes[e as usize]);
                }
            }
        }
    }
    table
        .into_iter()
        .filter(|&e| e != EMPTY)
        .map(|e| e as usize)
        .collect()
}
