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

const STYLES = ['default', 'table', 'yaml', 'ultra-concise', 'tts-summary', 'html'] as const;
type Style = (typeof STYLES)[number];

function parseArgs(args: string): { sub: string; rest: string[] } {
  const parts = args.trim().split(/\s+/).filter(Boolean);
  const [sub, ...rest] = parts.length ? parts : ['list'];
  return { sub, rest };
}

function writeSettings(filePath: string, style: Style) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const json = fs.existsSync(filePath) && fs.readFileSync(filePath, 'utf8').trim()
    ? JSON.parse(fs.readFileSync(filePath, 'utf8'))
    : {};
  json.assistant = json.assistant || {};
  json.assistant.outputStyle = style;
  fs.writeFileSync(filePath, JSON.stringify(json, null, 2), 'utf8');
}

export const outputStyleCommand: SlashCommand = {
  name: 'output-style',
  altNames: ['style'],
  description: 'list or set the assistant output style (e.g., yaml, table, html)',
  kind: CommandKind.BUILT_IN,
  action: async (context: CommandContext, args: string) => {
    const { sub, rest } = parseArgs(args);
    const scopeFlagIndex = rest.findIndex((r) => r === '--scope');
    const scope = scopeFlagIndex >= 0 ? (rest[scopeFlagIndex + 1] || 'user') : 'user';
    const candidates = rest.filter((_, i) => i !== scopeFlagIndex && i !== scopeFlagIndex + 1);

    switch (sub) {
      case 'list': {
        return {
          type: 'message',
          messageType: 'info',
          content: `Available styles: ${STYLES.join(', ')}`,
        };
      }
      case 'set': {
        const style = (candidates[0] || '').toLowerCase() as Style;
        if (!STYLES.includes(style)) {
          return {
            type: 'message',
            messageType: 'error',
            content: `Unknown style '${style}'. Try: ${STYLES.join(', ')}`,
          };
        }

        let filePath: string;
        if (scope === 'workspace') {
          const root = context.services.config?.getProjectRoot() || process.cwd();
          filePath = new Storage(root).getWorkspaceSettingsPath();
        } else {
          filePath = Storage.getGlobalSettingsPath();
        }

        try {
          writeSettings(filePath, style);
          context.ui.reloadCommands();
          return {
            type: 'message',
            messageType: 'info',
            content: `Set output style to '${style}' in ${scope} settings. New chats will use it.`,
          };
        } catch (e) {
          return {
            type: 'message',
            messageType: 'error',
            content: `Failed to write settings: ${e instanceof Error ? e.message : String(e)}`,
          };
        }
      }
      default: {
        return {
          type: 'message',
          messageType: 'info',
          content: `Usage:\n  /output-style list\n  /output-style set <${STYLES.join('|')}> [--scope user|workspace]`,
        };
      }
    }
  },
};

