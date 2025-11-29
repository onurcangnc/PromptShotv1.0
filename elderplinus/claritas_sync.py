# elderplinus/claritas_sync.py
"""
CL4R1T4S Repository Sync - AI System Prompts Intelligence

Leaked/extracted system prompts from major AI providers.
Used for target intelligence in payload generation.

https://github.com/elder-plinius/CL4R1T4S

Usage:
    from elderplinus.claritas_sync import sync_claritas, get_system_prompt
    
    # Sync all system prompts
    sync_claritas()
    
    # Get specific model's system prompt
    prompt = get_system_prompt("claude-opus")
    
    # Get common patterns across all prompts
    patterns = analyze_common_patterns()
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ========== CONFIGURATION ==========

GITHUB_API_BASE = "https://api.github.com/repos/elder-plinius/CL4R1T4S"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/elder-plinius/CL4R1T4S/main"

# Provider folders to sync
PROVIDERS = [
    "ANTHROPIC",
    "OPENAI",
    "GOOGLE",
    "XAI",
    "META",
    "MISTRAL",
    "PERPLEXITY",
    "CURSOR",
    "WINDSURF",
    "CLINE",
    "BOLT",
    "REPLIT",
    "DEVIN",
    "MANUS",
    "LOVABLE",
    "VERCEL V0",
    "MINIMAX",
    "MOONSHOT",
    "HUME",
    "DIA",
    "FACTORY",
    "MULTION",
    "SAMEDEV",
    "BRAVE",
    "CLUELY",
]

# Model name mappings for easier lookup
MODEL_ALIASES = {
    # Anthropic
    "claude": "ANTHROPIC",
    "claude-opus": "ANTHROPIC",
    "claude-sonnet": "ANTHROPIC",
    "claude-haiku": "ANTHROPIC",
    "anthropic": "ANTHROPIC",
    
    # OpenAI
    "gpt": "OPENAI",
    "gpt-4": "OPENAI",
    "gpt-4o": "OPENAI",
    "chatgpt": "OPENAI",
    "openai": "OPENAI",
    
    # Google
    "gemini": "GOOGLE",
    "bard": "GOOGLE",
    "google": "GOOGLE",
    
    # xAI
    "grok": "XAI",
    "xai": "XAI",
    
    # Meta
    "llama": "META",
    "meta": "META",
    
    # Mistral
    "mistral": "MISTRAL",
    "mixtral": "MISTRAL",
    
    # Others
    "perplexity": "PERPLEXITY",
    "cursor": "CURSOR",
    "windsurf": "WINDSURF",
    "cline": "CLINE",
    "bolt": "BOLT",
    "replit": "REPLIT",
    "devin": "DEVIN",
    "manus": "MANUS",
}

DEFAULT_CACHE_DIR = Path("claritas_cache")


@dataclass
class SystemPromptInfo:
    """Parsed system prompt information."""
    provider: str
    model_name: str
    filename: str
    content: str
    extracted_date: Optional[str] = None
    file_size: int = 0
    
    # Analyzed features
    has_safety_rules: bool = False
    has_persona: bool = False
    has_tool_use: bool = False
    has_output_format: bool = False
    detected_patterns: List[str] = field(default_factory=list)


@dataclass
class IntelligenceReport:
    """Aggregated intelligence from all system prompts."""
    total_prompts: int
    providers_covered: List[str]
    common_safety_patterns: List[str]
    common_refusal_phrases: List[str]
    common_format_rules: List[str]
    exploitable_patterns: List[str]
    generated_at: str


# ========== SYNC FUNCTIONS ==========

def sync_claritas(
    cache_dir: Optional[Path] = None,
    providers: Optional[List[str]] = None,
    verbose: bool = True
) -> Dict[str, List[str]]:
    """
    Sync system prompts from CL4R1T4S repository.
    
    Args:
        cache_dir: Directory to save downloaded files
        providers: List of providers to sync (None = all)
        verbose: Print progress
    
    Returns:
        Dict mapping provider to list of downloaded files
    """
    if not HAS_REQUESTS:
        print("❌ Cannot sync: requests library not installed")
        return {}
    
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    providers = providers or PROVIDERS
    downloaded = {}
    
    if verbose:
        print(f"📥 Syncing CL4R1T4S system prompts to {cache_dir}/")
        print(f"   Providers: {len(providers)}")
    
    for provider in providers:
        provider_dir = cache_dir / provider
        provider_dir.mkdir(exist_ok=True)
        
        try:
            # Get directory listing from GitHub API
            api_url = f"{GITHUB_API_BASE}/contents/{provider}"
            response = requests.get(api_url, timeout=30)
            
            if not response.ok:
                if verbose:
                    print(f"  ⚠️ {provider}: Could not list directory")
                continue
            
            files = response.json()
            downloaded[provider] = []
            
            for file_info in files:
                if file_info.get("type") != "file":
                    continue
                
                filename = file_info["name"]
                download_url = file_info.get("download_url")
                
                if not download_url:
                    continue
                
                # Download file
                try:
                    file_response = requests.get(download_url, timeout=30)
                    if file_response.ok:
                        filepath = provider_dir / filename
                        filepath.write_text(file_response.text, encoding="utf-8")
                        downloaded[provider].append(filename)
                except Exception:
                    pass
            
            if verbose:
                count = len(downloaded.get(provider, []))
                print(f"  ✅ {provider}: {count} files")
                
        except requests.RequestException as e:
            if verbose:
                print(f"  ❌ {provider}: {e}")
    
    # Save metadata
    total_files = sum(len(files) for files in downloaded.values())
    metadata = {
        "synced_at": datetime.now().isoformat(),
        "providers": list(downloaded.keys()),
        "total_files": total_files,
        "file_counts": {p: len(f) for p, f in downloaded.items()}
    }
    
    metadata_path = cache_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    if verbose:
        print(f"\n✅ Synced {total_files} files from {len(downloaded)} providers")
    
    return downloaded


def is_claritas_cache_valid(
    cache_dir: Optional[Path] = None,
    max_age_hours: int = 168  # 1 week
) -> bool:
    """Check if CL4R1T4S cache is valid."""
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    metadata_path = cache_dir / "metadata.json"
    
    if not metadata_path.exists():
        return False
    
    try:
        metadata = json.loads(metadata_path.read_text())
        synced_at = datetime.fromisoformat(metadata["synced_at"])
        age = datetime.now() - synced_at
        return age.total_seconds() < max_age_hours * 3600
    except (json.JSONDecodeError, KeyError, ValueError):
        return False


def ensure_claritas_cache(
    cache_dir: Optional[Path] = None,
    verbose: bool = True
) -> bool:
    """Ensure CL4R1T4S cache exists and is valid."""
    if is_claritas_cache_valid(cache_dir):
        if verbose:
            print("✅ CL4R1T4S cache is valid")
        return True
    
    if verbose:
        print("📥 CL4R1T4S cache expired or missing, syncing...")
    
    downloaded = sync_claritas(cache_dir, verbose=verbose)
    return len(downloaded) > 0


# ========== RETRIEVAL FUNCTIONS ==========

def get_system_prompt(
    model: str,
    cache_dir: Optional[Path] = None
) -> Optional[SystemPromptInfo]:
    """
    Get system prompt for a specific model.
    
    Args:
        model: Model name or alias (e.g., "claude", "gpt-4o", "grok")
        cache_dir: Cache directory
    
    Returns:
        SystemPromptInfo or None if not found
    """
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    
    # Resolve model to provider
    model_lower = model.lower()
    provider = MODEL_ALIASES.get(model_lower)
    
    if not provider:
        # Try direct match
        for p in PROVIDERS:
            if model_lower in p.lower():
                provider = p
                break
    
    if not provider:
        return None
    
    provider_dir = cache_dir / provider
    if not provider_dir.exists():
        return None
    
    # Find best matching file
    best_match = None
    best_score = 0
    
    for filepath in provider_dir.iterdir():
        if not filepath.is_file():
            continue
        
        filename_lower = filepath.name.lower()
        score = 0
        
        # Score based on model name match
        if model_lower in filename_lower:
            score += 10
        
        # Prefer newer files (check for date patterns)
        if "2025" in filepath.name:
            score += 5
        elif "2024" in filepath.name:
            score += 3
        
        # Prefer .txt and .md files
        if filepath.suffix in [".txt", ".md", ".mkd"]:
            score += 2
        
        if score > best_score:
            best_score = score
            best_match = filepath
    
    # If no match by model name, just get the first/newest file
    if not best_match:
        files = list(provider_dir.iterdir())
        if files:
            best_match = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
    
    if not best_match:
        return None
    
    content = best_match.read_text(encoding="utf-8", errors="ignore")
    
    return SystemPromptInfo(
        provider=provider,
        model_name=best_match.stem,
        filename=best_match.name,
        content=content,
        file_size=len(content),
        has_safety_rules=_detect_safety_rules(content),
        has_persona=_detect_persona(content),
        has_tool_use=_detect_tool_use(content),
        has_output_format=_detect_output_format(content),
        detected_patterns=_extract_patterns(content)
    )


def get_all_system_prompts(
    cache_dir: Optional[Path] = None,
    providers: Optional[List[str]] = None
) -> List[SystemPromptInfo]:
    """Get all cached system prompts."""
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    providers = providers or PROVIDERS
    
    prompts = []
    
    for provider in providers:
        provider_dir = cache_dir / provider
        if not provider_dir.exists():
            continue
        
        for filepath in provider_dir.iterdir():
            if not filepath.is_file():
                continue
            
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                
                prompts.append(SystemPromptInfo(
                    provider=provider,
                    model_name=filepath.stem,
                    filename=filepath.name,
                    content=content,
                    file_size=len(content),
                    has_safety_rules=_detect_safety_rules(content),
                    has_persona=_detect_persona(content),
                    has_tool_use=_detect_tool_use(content),
                    has_output_format=_detect_output_format(content),
                    detected_patterns=_extract_patterns(content)
                ))
            except Exception:
                pass
    
    return prompts


def list_available_providers(cache_dir: Optional[Path] = None) -> Dict[str, int]:
    """List available providers and file counts."""
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    
    if not cache_dir.exists():
        return {}
    
    result = {}
    for provider_dir in cache_dir.iterdir():
        if provider_dir.is_dir() and provider_dir.name in PROVIDERS:
            files = list(provider_dir.glob("*"))
            result[provider_dir.name] = len(files)
    
    return result


# ========== ANALYSIS FUNCTIONS ==========

def _detect_safety_rules(content: str) -> bool:
    """Detect if content has safety/restriction rules."""
    patterns = [
        r"cannot|can't|must not|should not|do not|don't",
        r"harmful|dangerous|illegal|unethical",
        r"refuse|decline|apologize",
        r"safety|security|protect",
        r"guideline|policy|rule",
    ]
    content_lower = content.lower()
    return any(re.search(p, content_lower) for p in patterns)


def _detect_persona(content: str) -> bool:
    """Detect if content defines a persona."""
    patterns = [
        r"you are|i am|your name is|my name is",
        r"assistant|helper|ai|model",
        r"character|personality|role",
        r"created by|developed by|made by",
    ]
    content_lower = content.lower()
    return any(re.search(p, content_lower) for p in patterns)


def _detect_tool_use(content: str) -> bool:
    """Detect if content mentions tool usage."""
    patterns = [
        r"tool|function|api|endpoint",
        r"search|browse|execute|run",
        r"<tool|<function|<action",
    ]
    content_lower = content.lower()
    return any(re.search(p, content_lower) for p in patterns)


def _detect_output_format(content: str) -> bool:
    """Detect if content specifies output format."""
    patterns = [
        r"format|markdown|json|xml",
        r"response|output|reply",
        r"structure|template|schema",
    ]
    content_lower = content.lower()
    return any(re.search(p, content_lower) for p in patterns)


def _extract_patterns(content: str) -> List[str]:
    """Extract notable patterns from system prompt."""
    patterns = []
    content_lower = content.lower()
    
    # Safety patterns
    if "sorry" in content_lower or "apologize" in content_lower:
        patterns.append("uses_apology")
    if "cannot" in content_lower or "can't" in content_lower:
        patterns.append("uses_cannot")
    if "harmful" in content_lower:
        patterns.append("mentions_harm")
    
    # Format patterns
    if "<" in content and ">" in content:
        patterns.append("uses_xml_tags")
    if "```" in content:
        patterns.append("uses_code_blocks")
    if "{" in content and "}" in content:
        patterns.append("uses_json_or_templates")
    
    # Instruction patterns
    if "step" in content_lower and ("by" in content_lower or "1" in content):
        patterns.append("uses_step_by_step")
    if "example" in content_lower:
        patterns.append("uses_examples")
    if "important" in content_lower or "critical" in content_lower:
        patterns.append("uses_emphasis")
    
    return patterns


def analyze_common_patterns(
    cache_dir: Optional[Path] = None
) -> IntelligenceReport:
    """
    Analyze all system prompts and extract common patterns.
    
    Returns:
        IntelligenceReport with aggregated intelligence
    """
    prompts = get_all_system_prompts(cache_dir)
    
    if not prompts:
        return IntelligenceReport(
            total_prompts=0,
            providers_covered=[],
            common_safety_patterns=[],
            common_refusal_phrases=[],
            common_format_rules=[],
            exploitable_patterns=[],
            generated_at=datetime.now().isoformat()
        )
    
    # Aggregate patterns
    all_content = "\n".join(p.content for p in prompts)
    providers = list(set(p.provider for p in prompts))
    
    # Extract common safety patterns
    safety_patterns = []
    safety_regex = [
        (r"I (?:cannot|can't|am unable to) ([^.]+)\.", "refusal"),
        (r"(?:harmful|dangerous|illegal) ([^.]+)", "harm_category"),
        (r"(?:should|must) (?:not|never) ([^.]+)", "prohibition"),
    ]
    
    for pattern, category in safety_regex:
        matches = re.findall(pattern, all_content, re.IGNORECASE)
        for match in matches[:5]:  # Limit to top 5
            safety_patterns.append(f"[{category}] {match[:100]}")
    
    # Extract common refusal phrases
    refusal_phrases = []
    refusal_patterns = [
        r"I'm sorry[^.]*\.",
        r"I cannot[^.]*\.",
        r"I'm unable to[^.]*\.",
        r"I don't[^.]*\.",
        r"I won't[^.]*\.",
    ]
    
    for pattern in refusal_patterns:
        matches = re.findall(pattern, all_content, re.IGNORECASE)
        refusal_phrases.extend(matches[:3])
    
    # Extract format rules
    format_rules = []
    if sum(1 for p in prompts if "uses_xml_tags" in p.detected_patterns) > len(prompts) / 2:
        format_rules.append("XML tags commonly used")
    if sum(1 for p in prompts if "uses_code_blocks" in p.detected_patterns) > len(prompts) / 2:
        format_rules.append("Code blocks commonly used")
    if sum(1 for p in prompts if "uses_json_or_templates" in p.detected_patterns) > len(prompts) / 2:
        format_rules.append("JSON/templates commonly used")
    
    # Identify exploitable patterns
    exploitable = []
    
    # Check for roleplay susceptibility
    roleplay_count = sum(1 for p in prompts if p.has_persona)
    if roleplay_count > len(prompts) * 0.7:
        exploitable.append("Most models have personas - roleplay attacks may work")
    
    # Check for format injection potential
    format_count = sum(1 for p in prompts if p.has_output_format)
    if format_count > len(prompts) * 0.5:
        exploitable.append("Many models have format rules - format confusion attacks may work")
    
    # Check for tool use
    tool_count = sum(1 for p in prompts if p.has_tool_use)
    if tool_count > len(prompts) * 0.3:
        exploitable.append("Some models have tool access - tool injection attacks may work")
    
    return IntelligenceReport(
        total_prompts=len(prompts),
        providers_covered=providers,
        common_safety_patterns=safety_patterns[:10],
        common_refusal_phrases=list(set(refusal_phrases))[:10],
        common_format_rules=format_rules,
        exploitable_patterns=exploitable,
        generated_at=datetime.now().isoformat()
    )


def get_bypass_suggestions(
    target_model: Optional[str] = None,
    cache_dir: Optional[Path] = None
) -> List[str]:
    """
    Get payload suggestions based on target model's system prompt.
    
    Args:
        target_model: Target model name (or None for general suggestions)
        cache_dir: Cache directory
    
    Returns:
        List of bypass strategy suggestions
    """
    suggestions = []
    
    if target_model:
        prompt_info = get_system_prompt(target_model, cache_dir)
        
        if prompt_info:
            # Model-specific suggestions
            if prompt_info.has_persona:
                suggestions.append(
                    f"Target uses persona '{prompt_info.model_name}' - "
                    "try roleplay override or character confusion"
                )
            
            if "uses_xml_tags" in prompt_info.detected_patterns:
                suggestions.append(
                    "Target uses XML tags - try XML injection or tag confusion"
                )
            
            if "uses_apology" in prompt_info.detected_patterns:
                suggestions.append(
                    "Target uses apology patterns - include 'no apology needed' in payload"
                )
            
            if prompt_info.has_tool_use:
                suggestions.append(
                    "Target has tool access - try tool spoofing or function injection"
                )
    
    # General suggestions from pattern analysis
    report = analyze_common_patterns(cache_dir)
    
    for pattern in report.exploitable_patterns:
        suggestions.append(f"[General] {pattern}")
    
    # Add universal bypass strategies
    suggestions.extend([
        "[Universal] Use format confusion (JSON inside markdown inside YAML)",
        "[Universal] Apply homoglyph mutations to bypass keyword filters",
        "[Universal] Use multi-language mixing (English + encoded)",
        "[Universal] Embed payload in hypothetical/roleplay context",
    ])
    
    return suggestions


# ========== CLI ==========

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "sync":
            sync_claritas(verbose=True)
        
        elif cmd == "list":
            providers = list_available_providers()
            print("\n📋 Available Providers:")
            for provider, count in sorted(providers.items()):
                print(f"  {provider}: {count} files")
            print(f"\n  Total: {sum(providers.values())} files")
        
        elif cmd == "analyze":
            print("\n🔍 Analyzing system prompts...\n")
            report = analyze_common_patterns()
            print(f"Total prompts: {report.total_prompts}")
            print(f"Providers: {', '.join(report.providers_covered)}")
            print(f"\n🔒 Common Safety Patterns:")
            for p in report.common_safety_patterns[:5]:
                print(f"  - {p}")
            print(f"\n🎯 Exploitable Patterns:")
            for p in report.exploitable_patterns:
                print(f"  - {p}")
        
        elif cmd == "suggest":
            target = sys.argv[2] if len(sys.argv) > 2 else None
            suggestions = get_bypass_suggestions(target)
            print(f"\n💡 Bypass Suggestions" + (f" for {target}" if target else "") + ":\n")
            for s in suggestions:
                print(f"  • {s}")
        
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python claritas_sync.py [sync|list|analyze|suggest [model]]")
    
    else:
        print("CL4R1T4S System Prompt Intelligence")
        print("Usage: python claritas_sync.py [sync|list|analyze|suggest [model]]")