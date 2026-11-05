/**
 * Shared lookups for the v3 home page and the Research, Publications, Contribute and Updates pages.
 * Everything here reads content; nothing holds copy.
 */
import { getCollection, getEntry, render } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export type Partner = CollectionEntry<'partners'>;
export type Update = CollectionEntry<'updates'>;

/** Partners in `order:` (ST Engineering, NUS, UPenn, CMU) without the funder, and the funder. */
export async function partnersInOrder() {
  const all = (await getCollection('partners')).sort((a, b) => a.data.order - b.data.order);
  const funder = all.find((p) => p.data.role === 'Funding sponsor');
  return { all, partners: all.filter((p) => p !== funder), funder };
}

/** Published updates, newest first. */
export async function allUpdates(): Promise<Update[]> {
  return (await getCollection('updates', (u) => !u.data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
  );
}

/** Load content/programme/<id>.md if it exists (with its rendered body), else undefined. */
export async function optionalSection(id: string) {
  const entry = await getEntry('programme', id);
  if (!entry) return undefined;
  const { Content } = await render(entry);
  return { ...entry.data, Content, hasBody: !!entry.body?.trim() };
}

/** Upper-case the first letter. */
export const upperFirst = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
/** Lower-case the first letter. */
export const lowerFirst = (s: string) => s.charAt(0).toLowerCase() + s.slice(1);

/** The partner file name, e.g. "NUS.md", from the entry's file path. */
export const fileName = (p: Partner) => p.filePath?.split('/').pop() ?? `${p.id}.md`;

/** Lead line for a card: `lead:`, else the person marked `lead`, else the first person with a role ("Name, role"). */
export function leadLine(p: Partner): string | undefined {
  const d = p.data;
  if (d.lead) return d.lead;
  const lead = d.people.find((m) => m.lead);
  if (lead) return lead.name;
  const withRole = d.people.find((m) => m.role);
  return withRole?.role ? `${withRole.name}, ${lowerFirst(withRole.role)}` : undefined;
}

/** A partner's people split by `group:`: ungrouped people first (group undefined), then each group in file order. */
export function peopleGroups<T extends { group?: string }>(people: T[]): { group?: string; people: T[] }[] {
  const out: { group?: string; people: T[] }[] = [];
  const ungrouped = people.filter((m) => !m.group);
  if (ungrouped.length > 0) out.push({ people: ungrouped });
  for (const g of [...new Set(people.map((m) => m.group).filter((g): g is string => !!g))])
    out.push({ group: g, people: people.filter((m) => m.group === g) });
  return out;
}

/** "nus" → "NUS" (falls back to the id). */
export async function shortNames(): Promise<(id: string) => string> {
  const all = await getCollection('partners');
  const map = Object.fromEntries(all.map((p) => [p.id, p.data.short]));
  return (id: string) => map[id] ?? id;
}

/** ISO date for <time datetime>. */
export const isoDay = (d: Date) => d.toISOString().slice(0, 10);

/** Publication status as a plain-text tag. */
export const statusLabel: Record<string, string> = {
  published: 'Published',
  accepted: 'Accepted',
  preprint: 'Preprint',
  workshop: 'Workshop',
};

/**
 * The five research themes, in page order. From content/programme/themes.md when it exists (one item per
 * theme: `title` name, `label` owner, `state` status, `text` one line, `icon` the anchor on the Research
 * page); otherwise derived from tracks.md, command.md, localisation.md and simulation.md (no status).
 * Pass the already-loaded themes section (from `optionalSection('themes')`) to avoid rendering it twice.
 */
export interface Theme {
  id: string;
  name: string;
  owner: string;
  status?: string;
  line?: string;
}
const THEME_IDS = ['learning', 'formal', 'safety', 'localisation', 'simulation'];
export async function themes(file?: Awaited<ReturnType<typeof optionalSection>>): Promise<Theme[]> {
  const short = await shortNames();
  const names = (ids: string[]) => [...new Set(ids)].map(short).join(', ');
  if (file && file.items.length > 0) {
    return file.items.map((t, i) => ({
      id: t.icon ?? THEME_IDS[i] ?? t.title.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
      name: t.title,
      owner: t.label ?? names(t.partners),
      status: t.state,
      line: t.text,
    }));
  }
  const tracks = await getEntry('programme', 'tracks');
  const command = await getEntry('programme', 'command');
  const loc = await getEntry('programme', 'localisation');
  const sim = await getEntry('programme', 'simulation');
  const { partners } = await partnersInOrder();
  const out: Theme[] = [];
  tracks?.data.items.slice(0, 2).forEach((t, i) =>
    out.push({ id: THEME_IDS[i], name: t.label?.split('·').pop()?.trim() ?? t.title, owner: names(t.partners), line: t.title }),
  );
  const filter = command?.data.items.find((c) => /safety/i.test(c.title));
  if (filter) out.push({ id: 'safety', name: filter.title, owner: names(filter.partners), line: filter.text });
  if (loc)
    out.push({
      id: 'localisation',
      name: loc.data.eyebrow,
      owner: names(partners.filter((p) => p.data.work.localisation).map((p) => p.id)),
      line: loc.data.title,
    });
  if (sim)
    out.push({
      id: 'simulation',
      name: sim.data.eyebrow,
      owner: names(sim.data.items.flatMap((c) => c.partners)),
      line: sim.data.title,
    });
  return out;
}
