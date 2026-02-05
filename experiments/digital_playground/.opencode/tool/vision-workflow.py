#!/usr/bin/env python3
"""
Vision Workflow Integration for Guardian Framework.
Automatically detects images in conversations and invokes @vision analysis.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class VisionWorkflow:
    """Manages automatic vision analysis integration."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.vision_cache_dir = project_root / ".opencode" / "vision-cache"
        self.vision_cache_dir.mkdir(exist_ok=True)
    
    def detect_image_references(self, content: str) -> List[Dict[str, str]]:
        """
        Detect image references in content.
        Looks for:
        - Markdown image syntax: ![alt](url)
        - Direct image URLs (jpg, png, gif, svg, etc.)
        - References to uploaded images
        """
        images = []
        
        # Pattern 1: Markdown image syntax ![alt](url)
        md_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        for match in re.finditer(md_pattern, content):
            images.append({
                'type': 'markdown',
                'alt': match.group(1),
                'url': match.group(2),
                'full_match': match.group(0)
            })
        
        # Pattern 2: Direct image URLs
        url_pattern = r'(https?://[^\s]+\.(?:jpg|jpeg|png|gif|svg|webp|bmp))'
        for match in re.finditer(url_pattern, content, re.IGNORECASE):
            # Skip if already captured as markdown
            if not any(img['url'] == match.group(1) for img in images):
                images.append({
                    'type': 'direct_url',
                    'url': match.group(1),
                    'full_match': match.group(0)
                })
        
        # Pattern 3: Image upload references (common in chat interfaces)
        upload_pattern = r'\[Image\s*\d*\s*\]\s*\(([^\)]+)\)'
        for match in re.finditer(upload_pattern, content, re.IGNORECASE):
            images.append({
                'type': 'upload_reference',
                'url': match.group(1),
                'full_match': match.group(0)
            })
        
        return images
    
    def should_invoke_vision(self, content: str, conversation_history: List[Dict]) -> Tuple[bool, List[Dict]]:
        """
        Determine if @vision should be invoked based on content and history.
        Returns (should_invoke, image_list)
        """
        images = self.detect_image_references(content)
        
        if not images:
            return False, []
        
        # Check if these images were already analyzed recently
        recent_analyses = self.get_recent_analyses()
        
        new_images = []
        for img in images:
            img_url = img['url']
            if not self.is_recently_analyzed(img_url, recent_analyses):
                new_images.append(img)
        
        return len(new_images) > 0, new_images
    
    def is_recently_analyzed(self, image_url: str, recent_analyses: List[Dict]) -> bool:
        """Check if image was analyzed in the last hour."""
        for analysis in recent_analyses:
            if analysis.get('image_url') == image_url:
                analyzed_at = datetime.fromisoformat(analysis['analyzed_at'])
                time_diff = datetime.now() - analyzed_at
                if time_diff.total_seconds() < 3600:  # 1 hour
                    return True
        return False
    
    def get_recent_analyses(self) -> List[Dict]:
        """Get recent vision analyses from cache."""
        cache_file = self.vision_cache_dir / "recent_analyses.json"
        if not cache_file.exists():
            return []
        
        try:
            return json.loads(cache_file.read_text())
        except Exception:
            return []
    
    def save_analysis(self, image_url: str, analysis_result: str, invoked_by: str):
        """Save vision analysis result to cache."""
        cache_file = self.vision_cache_dir / "recent_analyses.json"
        
        # Load existing
        analyses = []
        if cache_file.exists():
            try:
                analyses = json.loads(cache_file.read_text())
            except Exception:
                analyses = []
        
        # Add new analysis
        analyses.append({
            'image_url': image_url,
            'analysis_result': analysis_result,
            'invoked_by': invoked_by,
            'analyzed_at': datetime.now().isoformat()
        })
        
        # Keep only last 20 analyses
        analyses = analyses[-20:]
        
        # Save
        cache_file.write_text(json.dumps(analyses, indent=2) + "\n")
    
    def generate_vision_prompt(self, images: List[Dict]) -> str:
        """Generate @vision invocation prompt."""
        if not images:
            return ""
        
        prompt = "[@vision] Please analyze the following image(s):\n\n"
        
        for i, img in enumerate(images, 1):
            prompt += f"Image {i}:\n"
            if img.get('alt'):
                prompt += f"- Description: {img['alt']}\n"
            prompt += f"- URL: {img['url']}\n"
            prompt += f"- Type: {img['type']}\n\n"
        
        prompt += """Please provide:
1. A detailed description of each image
2. Key visual elements and their significance
3. Any text visible in the images (transcribed)
4. Colors, layout, and structural information
5. Implementation-relevant details (dimensions, components, states, etc.)
6. Any anomalies or issues you detect

Format your response with clear sections for each image."""
        
        return prompt
    
    def update_plan_prompt(self):
        """Update plan.md to include automatic vision integration."""
        plan_file = self.project_root / ".opencode" / "agent" / "plan.md"
        
        if not plan_file.exists():
            print(f"❌ Plan agent file not found: {plan_file}")
            return False
        
        content = plan_file.read_text()
        
        # Add vision integration to responsibilities
        vision_integration = """8. Automatically invoke `@vision` when images are present in the conversation. Use the vision-workflow.py tool to:
   - Detect image references (markdown, URLs, uploads)
   - Check if images were recently analyzed
   - Generate appropriate @vision prompts
   - Attach vision findings to your analysis and handoffs to @build or @guardian"""
        
        # Find the responsibilities section and add vision integration
        if "Automatically invoke `@vision`" not in content:
            # Add after existing responsibilities
            responsibilities_marker = "Responsibilities:"
            if responsibilities_marker in content:
                # Insert after the existing responsibilities list
                lines = content.split('\n')
                new_lines = []
                in_responsibilities = False
                responsibility_count = 0
                
                for line in lines:
                    new_lines.append(line)
                    
                    if line.strip() == responsibilities_marker:
                        in_responsibilities = True
                    elif in_responsibilities and line.strip().startswith('7.'):
                        # After the 7th responsibility, add our new one
                        new_lines.append(vision_integration)
                        in_responsibilities = False
                
                content = '\n'.join(new_lines)
        
        # Add vision workflow tool to tools section
        if "vision-workflow.py" not in content:
            # Add to the tools section in frontmatter
            content = content.replace(
                "tools:",
                "tools:\n  - vision-workflow.py",
                1
            )
        
        plan_file.write_text(content)
        print(f"✅ Updated Plan agent with vision integration")
        return True


def main():
    """Main entry point for vision workflow."""
    if len(sys.argv) < 2:
        print("Usage: vision-workflow.py <command> [options]")
        print("Commands:")
        print("  detect <content>     - Detect images in content")
        print("  should-invoke <content> - Check if vision should be invoked")
        print("  generate-prompt <image_urls> - Generate @vision prompt")
        print("  update-plan          - Update plan.md with vision integration")
        sys.exit(1)
    
    command = sys.argv[1]
    project_root = Path(".")
    workflow = VisionWorkflow(project_root)
    
    if command == "detect":
        content = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
        images = workflow.detect_image_references(content)
        print(json.dumps(images, indent=2))
    
    elif command == "should-invoke":
        content = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
        should_invoke, images = workflow.should_invoke_vision(content, [])
        result = {
            "should_invoke": should_invoke,
            "images": images,
            "count": len(images)
        }
        print(json.dumps(result, indent=2))
    
    elif command == "generate-prompt":
        # Read image JSON from stdin or args
        if len(sys.argv) > 2:
            images_json = sys.argv[2]
        else:
            images_json = sys.stdin.read()
        
        try:
            images = json.loads(images_json)
            prompt = workflow.generate_vision_prompt(images)
            print(prompt)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif command == "update-plan":
        success = workflow.update_plan_prompt()
        sys.exit(0 if success else 1)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
