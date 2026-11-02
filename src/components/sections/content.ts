import { getEntry, render } from 'astro:content';

/** Load one content/programme/<id>.md section with its rendered body. Throws if the file is missing. */
export async function section(id: string) {
  const entry = await getEntry('programme', id);
  if (!entry) throw new Error(`Missing content/programme/${id}.md`);
  const { Content } = await render(entry);
  return { ...entry.data, Content };
}
