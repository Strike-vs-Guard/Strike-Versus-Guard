/**
 * Content schema for the Strike vs Guard website.
 *
 * Every Markdown file under /content is checked against these rules when the
 * site builds. If a partner file is missing a field, has a typo in a field
 * name, or points at an image that does not exist, the build fails with a
 * message naming the file and the field. That is what stops a broken edit
 * from reaching the live site.
 *
 * Owned by ST Engineering (see .github/CODEOWNERS). Partners should not need
 * to edit this file.
 */
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

/** The four layers of the system, used to tag partners and the stack section. */
const LAYERS = ['strategy', 'safety', 'flight', 'localisation', 'drones', 'integration'] as const;

/** Partner ids. Must match the partner file names, lower-cased. */
const PARTNER_IDS = ['htx', 'st', 'cmu', 'upenn', 'nus'] as const;

const url = z.string().url();

/**
 * One file per partner: content/partners/<PARTNER>.md
 * Front matter feeds the partner card on the home page.
 * The Markdown body becomes the partner's own page at /partners/<id>/.
 */
const partners = defineCollection({
  loader: glob({
    pattern: '[!_]*.md',
    base: './content/partners',
    generateId: ({ entry }) => entry.replace(/\.md$/, '').toLowerCase(),
  }),
  schema: ({ image }) =>
    z
      .object({
        /** Short name shown on cards and in navigation, e.g. "NUS". */
        short: z.string().max(24),
        /** Full institution name. */
        institution: z.string(),
        /** Lab or group name, e.g. "MARMot Lab". Optional for the sponsor. */
        lab: z.string().optional(),
        /** Lab name written out in full, if `lab` is an acronym. */
        labFull: z.string().optional(),
        /** Principal investigator or lead, e.g. "Prof Guillaume Sartoretti". */
        lead: z.string().optional(),
        /** Role in the programme, shown as a small label on the card. */
        role: z.enum(['Funding sponsor', 'Lead partner', 'Partner']),
        /** What this partner contributes, in a few words (shown on the card). */
        contribution: z.string().max(70),
        /** One or two sentences for the home page card. Keep it under ~40 words. */
        summary: z.string().max(320),
        /**
         * What this partner does on each layer, one short line each (max 90 characters).
         * Shown in the "who does what" grid on the home page. Leave out layers you don't work on.
         */
        work: z
          .object({
            strategy: z.string().max(90).optional(),
            safety: z.string().max(90).optional(),
            flight: z.string().max(90).optional(),
            localisation: z.string().max(90).optional(),
            drones: z.string().max(90).optional(),
            integration: z.string().max(90).optional(),
          })
          .strict()
          .default({}),
        /** Institution logo, relative to this file, e.g. ./NUS/nus.png */
        logo: image(),
        /** Optional lab logo, shown on the partner page. */
        labLogo: image().optional(),
        /** Alt text for the logo. Defaults to the institution name. */
        logoAlt: z.string().optional(),
        /** Lab or institution website. */
        website: url.optional(),
        /** Public contact email for website enquiries (optional). */
        contact: z.string().email().optional(),
        /** Position on the page: lower numbers come first. */
        order: z.number().int(),
        /** Set to false to show only a card with no separate page (used for the sponsor). */
        page: z.boolean().default(true),
        /** Date of the last meaningful edit, YYYY-MM-DD. */
        updated: z.coerce.date(),
      })
      .strict(),
});

/** A media item used in the programme sections (image or short clip). */
const item = (image: any) =>
  z
    .object({
      title: z.string(),
      text: z.string().optional(),
      /** Small label above the title, e.g. "Track A · Learning" or "Year 1". */
      label: z.string().optional(),
      /** Image path relative to the section file, e.g. ./images/flight-cage.jpg */
      image: image().optional(),
      alt: z.string().optional(),
      /** Video file name in public/media, e.g. formation-change.mp4 */
      video: z.string().regex(/^[\w.-]+\.mp4$/).optional(),
      /** Poster image for the video, file name in public/media. */
      poster: z.string().regex(/^[\w.-]+\.(jpg|png|webp)$/).optional(),
      /** Partner ids associated with this item. */
      partners: z.array(z.enum(PARTNER_IDS)).default([]),
      /** Optional strength / limitation lines (used for the two tracks). */
      plus: z.string().optional(),
      minus: z.string().optional(),
      /** Optional date range or period, e.g. "2026 to 2027". */
      when: z.string().optional(),
      /** Marks the current milestone. */
      current: z.boolean().default(false),
      /** Short icon key, used by a few sections. */
      icon: z.string().optional(),
    })
    .strict();

/**
 * Shared programme sections: content/programme/<section>.md
 * Each file is one section of the home page. Front matter holds the headline
 * and any cards; the Markdown body is the section's intro text.
 */
const programme = defineCollection({
  loader: glob({ pattern: '[!_]*.md', base: './content/programme' }),
  schema: ({ image }) =>
    z
      .object({
        /** Small label above the headline. */
        eyebrow: z.string(),
        title: z.string(),
        /** Position on the home page: lower numbers come first. */
        order: z.number().int(),
        /** Optional one-line note shown under the cards. */
        note: z.string().optional(),
        /** Optional hero/feature image for the section. */
        image: image().optional(),
        imageAlt: z.string().optional(),
        caption: z.string().optional(),
        items: z.array(item(image)).default([]),
        /** Optional secondary list, e.g. use cases. */
        tags: z.array(z.string()).default([]),
        tagsLabel: z.string().optional(),
        /** Optional short list of plain statements, e.g. what the drones decide (home-page hero). */
        decisionsLabel: z.string().optional(),
        decisions: z.array(z.string()).default([]),
        /** Optional one-sentence status line, reused by other pages. */
        status: z.string().optional(),
      })
      .strict(),
});

/** News and progress posts: content/updates/YYYY-MM-DD-short-title.md */
const updates = defineCollection({
  loader: glob({ pattern: '[!_]*.md', base: './content/updates' }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string().max(100),
        date: z.coerce.date(),
        /** Partner id of the author's organisation. */
        partner: z.enum(PARTNER_IDS),
        author: z.string().optional(),
        summary: z.string().max(300),
        image: image().optional(),
        imageAlt: z.string().optional(),
        /** Set to true to keep a post out of the live site while you work on it. */
        draft: z.boolean().default(false),
      })
      .strict(),
});

/** Site-wide settings: content/site.yml */
const site = defineCollection({
  loader: file('./content/site.yml'),
  schema: z.object({
    title: z.string(),
    tagline: z.string(),
    description: z.string(),
    contactEmail: z.string().email().optional(),
    repository: url,
    footerNote: z.string(),
  }),
});

export const collections = { partners, programme, updates, site };
