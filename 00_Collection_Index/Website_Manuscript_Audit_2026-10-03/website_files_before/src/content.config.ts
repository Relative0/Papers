import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    image: z.string().optional(),
    order: z.number(),
    phase: z.enum(['Represent', 'Observe', 'Organize', 'Become']),
    status: z.string(),
    question: z.string(),
    paperTitle: z.string().optional(),
    paperStatus: z.string().optional(),
    paperContribution: z.string().optional(),
    paperLocation: z.string().optional(),
    paperPdf: z.string().optional(),
    paperSourceVersion: z.string().optional(),
    paperByline: z.string().optional(),
  }),
});

export const collections = { projects };
