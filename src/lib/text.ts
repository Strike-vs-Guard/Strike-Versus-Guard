/** Small text helpers shared by templates. */

/** Join words as an English list: "a", "a and b", "a, b and c". */
export function listWords(a: string[]): string {
  return a.length < 2 ? a.join('') : `${a.slice(0, -1).join(', ')} and ${a[a.length - 1]}`;
}

/** A date in British style: 'short' gives "3 Nov 2026", 'long' gives "3 November 2026". */
export function fmtDate(d: Date, style: 'short' | 'long'): string {
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: style, year: 'numeric' });
}
