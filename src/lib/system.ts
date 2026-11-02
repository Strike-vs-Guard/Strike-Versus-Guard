/**
 * Data for the system diagrams (the annotated drone and the connection diagram).
 * Built from content/programme/stack.md (the layers) and content/partners/*.md
 * (who works on which layer, from each partner's `work:` lines), so partners
 * still only edit their own file.
 */
import { getCollection, getEntry } from 'astro:content';
import { getImage } from 'astro:assets';
import { url } from './url';

export const LAYER_IDS = ['strategy', 'safety', 'flight', 'drones', 'integration'] as const;
export type LayerId = (typeof LAYER_IDS)[number];

export async function getSystemData() {
  const stack = await getEntry('programme', 'stack');
  if (!stack) throw new Error('Missing content/programme/stack.md');
  let n = 0;
  const layers = stack.data.items
    .filter((i) => LAYER_IDS.includes(i.icon as LayerId))
    .map((i) => ({
      id: i.icon as LayerId,
      n: i.icon === 'integration' ? null : ++n,
      title: i.title,
      desc: i.text ?? '',
    }));

  const all = (await getCollection('partners')).sort((a, b) => a.data.order - b.data.order);
  const members = all.filter((p) => p.data.role !== 'Funding sponsor');
  const sponsor = all.find((p) => p.data.role === 'Funding sponsor');

  const logos: Record<string, string> = {};
  const labs: Record<string, string> = {};
  for (const p of members) {
    logos[p.id] = (await getImage({ src: p.data.logo, height: 96, format: 'png' })).src;
    labs[p.id] = p.data.labLogo ? (await getImage({ src: p.data.labLogo, height: 96, format: 'png' })).src : logos[p.id];
  }

  return {
    section: { eyebrow: stack.data.eyebrow, title: stack.data.title, intro: '' },
    layers,
    partners_in_display_order: members.map((p) => ({
      id: p.id,
      short: p.data.short,
      institution: p.data.institution,
      lab: p.data.lab ?? '',
      role: p.data.role,
      lead: p.data.lead ?? '',
      href: url(`partners/${p.id}/`),
      work: Object.fromEntries(Object.entries(p.data.work).filter(([, v]) => !!v)),
    })),
    sponsor: { id: sponsor?.id ?? 'htx', name: sponsor?.data.short ?? 'HTX', note: `Funded by ${sponsor?.data.short ?? 'HTX'}` },
    logos,
    labs,
  };
}
export type SystemData = Awaited<ReturnType<typeof getSystemData>>;
