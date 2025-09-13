/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import type { SlashCommand, CommandContext } from './types.js';
import { CommandKind } from './types.js';
import { Storage } from '@google/gemini-cli-core';

type OutputStyle = 'default' | 'table' | 'yaml' | 'ultra-concise' | 'tts-summary' | 'html';

interface WorkflowStep { style: OutputStyle; goal: string }
interface WorkflowDef { name: string; description?: string; steps: WorkflowStep[] }

function styleHint(style: OutputStyle) {
  switch (style) {
    case 'yaml':
      return '\n- Use YAML only (no backticks, no prose).';
    case 'table':
      return '\n- Prefer Markdown tables for structured data.';
    case 'ultra-concise':
      return '\n- Answer in ≤7 short bullets.';
    case 'tts-summary':
      return "\n- End with a 'TTS:' one‑sentence summary; call a TTS MCP tool if available.";
    case 'html':
      return "\n- Generate a standalone HTML file via write_file under .gemini/tmp/<slug>.html and return its path.";
    default:
      return '';
  }
}

function findWorkflowFiles(projectRoot: string): string[] {
  const userDir = path.join(Storage.getGlobalGeminiDir(), 'styles');
  const wsDir = path.join(projectRoot, '.gemini', 'styles');
  const exDir = path.join(projectRoot, 'examples', 'styles');
  const files: string[] = [];
  for (const dir of [userDir, wsDir, exDir]) {
    try {
      if (!fs.existsSync(dir)) continue;
      for (const f of fs.readdirSync(dir)) {
        if (f.endsWith('.json')) files.push(path.join(dir, f));
      }
    } catch {
      // ignore
    }
  }
  return files;
}

function loadWorkflows(projectRoot: string): WorkflowDef[] {
  const files = findWorkflowFiles(projectRoot);
  const defs: WorkflowDef[] = [];
  for (const file of files) {
    try {
      const json = JSON.parse(fs.readFileSync(file, 'utf8')) as WorkflowDef | WorkflowDef[];
      if (Array.isArray(json)) defs.push(...json);
      else defs.push(json);
    } catch {
      // skip invalid
    }
  }
  return defs;
}

function buildPrompt(def: WorkflowDef, topic: string): string {
  const lines: string[] = [];
  lines.push(`Execute the following style workflow for topic: ${topic}`);
  lines.push('Use your tools as needed. Confirm before sensitive actions.');
  def.steps.forEach((s, i) => {
    const n = i + 1;
    lines.push(`\nStep ${n} — Style: ${s.style}`);
    lines.push(s.goal + styleHint(s.style));
  });
  lines.push('\nWhen an HTML step is present, write a single file and return its saved path.');
  lines.push('When a TTS step is present, end with a TTS: one‑sentence summary.');
  return lines.join('\n');
}

function parseArgs(args: string): { sub: string; rest: string[] } {
  const parts = args.trim().split(/\s+/).filter(Boolean);
  const [sub, ...rest] = parts.length ? parts : ['list'];
  return { sub, rest };
}

export const workflowCommand: SlashCommand = {
  name: 'workflow',
  description: 'List or run output‑style workflows composed of smaller style steps',
  kind: CommandKind.BUILT_IN,
  action: async (context: CommandContext, args: string) => {
    const { sub, rest } = parseArgs(args);
    const root = context.services.config?.getProjectRoot() || process.cwd();
    const defs = loadWorkflows(root);

    if (sub === 'list') {
      if (defs.length === 0) {
        return { type: 'message', messageType: 'info', content: 'No workflows found. Add JSON files under ~/.gemini/styles or .gemini/styles.' };
      }
      const list = defs.map(d => `- ${d.name}${d.description ? ` — ${d.description}` : ''}`).join('\n');
      return { type: 'message', messageType: 'info', content: `Available workflows:\n${list}` };
    }

    if (sub === 'run') {
      const name = rest[0];
      const topic = rest.slice(1).join(' ').trim() || '<no topic provided>';
      const def = defs.find(d => d.name === name);
      if (!def) {
        return { type: 'message', messageType: 'error', content: `Workflow '${name}' not found. Use /workflow list.` };
      }
      return { type: 'submit_prompt', content: buildPrompt(def, topic) };
    }

    return { type: 'message', messageType: 'info', content: 'Usage:\n  /workflow list\n  /workflow run <name> [topic...]' };
  },
};
