/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import * as fs from 'node:fs';
import process from 'node:process';
import { Storage } from '../config/storage.js';

export type OutputStyle =
  | 'default'
  | 'table'
  | 'yaml'
  | 'ultra-concise'
  | 'tts-summary'
  | 'html';

function readJsonIfExists(filePath: string): unknown | null {
  try {
    if (!fs.existsSync(filePath)) return null;
    const raw = fs.readFileSync(filePath, 'utf8');
    if (!raw.trim()) return {};
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function resolveSelectedOutputStyle(): OutputStyle {
  const env = process.env['GEMINI_OUTPUT_STYLE']?.trim();
  if (env && env.length > 0) return mapToStyle(env);

  // Prefer workspace settings over user settings.
  const storage = new Storage(process.cwd());
  const workspaceSettingsPath = storage.getWorkspaceSettingsPath();
  const userSettingsPath = Storage.getGlobalSettingsPath();

  const ws = (readJsonIfExists(workspaceSettingsPath) || {}) as any;
  const usr = (readJsonIfExists(userSettingsPath) || {}) as any;
  const wsStyle: string | undefined = ws?.assistant?.outputStyle;
  const usrStyle: string | undefined = usr?.assistant?.outputStyle;
  if (wsStyle) return mapToStyle(wsStyle);
  if (usrStyle) return mapToStyle(usrStyle);
  return 'default';
}

function mapToStyle(s: string): OutputStyle {
  const t = s.toLowerCase();
  if (t === 'table' || t === 'tables') return 'table';
  if (t === 'yaml' || t === 'yml') return 'yaml';
  if (t === 'ultra' || t === 'concise' || t === 'ultra-concise')
    return 'ultra-concise';
  if (t === 'tts' || t === 'tts-summary' || t === 'speech') return 'tts-summary';
  if (t === 'html' || t === 'genui' || t === 'ui') return 'html';
  return 'default';
}

export function getStyleInstructions(style: OutputStyle): string {
  switch (style) {
    case 'table':
      return `\n\n# Output Style: Markdown Tables\n- Prefer GitHub‑flavored Markdown tables to present lists, comparisons, tasks, or results.\n- Keep each cell concise; wrap code in fenced blocks outside tables.\n- Always include a brief plain‑text summary above the first table.`;
    case 'yaml':
      return `\n\n# Output Style: YAML Only\n- Respond with ONLY valid YAML. Do NOT include backticks or extra prose.\n- Use keys when applicable: task, status, summary, steps, decisions, artifacts, next_steps.\n- Use arrays for steps and artifacts; keep values concise.`;
    case 'ultra-concise':
      return `\n\n# Output Style: Ultra Concise\n- Answer in 3–7 bullet lines max, each ≤ 100 chars.\n- Put critical commands first in monospace. No filler.`;
    case 'tts-summary':
      return `\n\n# Output Style: TTS Summary\n- End with a 1–2 sentence summary prefixed 'TTS:'.\n- If an MCP TTS tool exists, you MAY call it with that summary. Otherwise, just include the 'TTS:' line.`;
    case 'html':
      return `\n\n# Output Style: Generative HTML UI\n- Create a minimal, readable HTML document (inline CSS ok).\n- Use the write_file tool to save to a temp path under .gemini/tmp/ named 'genui-<slug>.html'.\n- Include sections: Title, Summary, Key Actions, Details, Next Steps.\n- After writing, return the saved path. If appropriate, propose opening it with a shell command (requires approval).`;
    default:
      return '';
  }
}
