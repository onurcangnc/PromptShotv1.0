# elderplinus/github_sync.py
"""
Elder Plinius L1B3RT4S Repository Sync

GitHub'dan güncel jailbreak payload'larını çeker ve parse eder.
https://github.com/elder-plinius/L1B3RT4S

Usage:
    from elderplinus.github_sync import sync_payloads, get_cached_payloads
    
    # Sync from GitHub
    sync_payloads()
    
    # Get cached payloads
    payloads = get_cached_payloads()
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Try to import requests, fallback gracefully
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️ requests not installed. Run: pip install requests")


# ========== CONFIGURATION ==========

GITHUB_BASE = "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main"

PAYLOAD_SOURCES = {
    "chatgpt": f"{GITHUB_BASE}/CHATGPT.mkd",
    "anthropic": f"{GITHUB_BASE}/ANTHROPIC.mkd",
    "openai": f"{GITHUB_BASE}/OPENAI.mkd",
    "google": f"{GITHUB_BASE}/GOOGLE.mkd",
    "systemprompts": f"{GITHUB_BASE}/SYSTEMPROMPTS.mkd",
}

# Default cache directory (relative to project root)
DEFAULT_CACHE_DIR = Path("elderplinus_cache")


@dataclass
class ParsedPayload:
    """Parsed payload structure."""
    name: str
    content: str
    target_model: str
    source_file: str
    tags: List[str]
    
    def to_dict(self) -> dict:
        return asdict(self)


# ========== SYNC FUNCTIONS ==========

def sync_payloads(
    cache_dir: Optional[Path] = None,
    sources: Optional[Dict[str, str]] = None,
    verbose: bool = True
) -> Dict[str, str]:
    """
    Download payload files from L1B3RT4S repository.
    
    Args:
        cache_dir: Directory to save downloaded files
        sources: Custom source URLs (default: PAYLOAD_SOURCES)
        verbose: Print progress
    
    Returns:
        Dict mapping source name to file path
    """
    if not HAS_REQUESTS:
        print("❌ Cannot sync: requests library not installed")
        return {}
    
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    sources = sources or PAYLOAD_SOURCES
    downloaded = {}
    
    if verbose:
        print(f"📥 Syncing L1B3RT4S payloads to {cache_dir}/")
    
    for name, url in sources.items():
        try:
            response = requests.get(url, timeout=30)
            
            if response.ok:
                filepath = cache_dir / f"{name}.mkd"
                filepath.write_text(response.text, encoding="utf-8")
                downloaded[name] = str(filepath)
                
                if verbose:
                    size = len(response.text)
                    print(f"  ✅ {name}.mkd ({size:,} bytes)")
            else:
                if verbose:
                    print(f"  ❌ {name}: HTTP {response.status_code}")
                    
        except requests.RequestException as e:
            if verbose:
                print(f"  ❌ {name}: {e}")
    
    # Save metadata
    metadata = {
        "synced_at": datetime.now().isoformat(),
        "sources": list(downloaded.keys()),
        "total_files": len(downloaded)
    }
    metadata_path = cache_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    if verbose:
        print(f"✅ Synced {len(downloaded)}/{len(sources)} files")
    
    return downloaded


def sync_l1b3rt4s_prompts():
    """Legacy function name for backward compatibility."""
    return sync_payloads(verbose=True)


# ========== PARSING FUNCTIONS ==========

def parse_mkd_file(filepath: Path, source_name: str) -> List[ParsedPayload]:
    """
    Parse a .mkd file and extract individual payloads.
    
    Args:
        filepath: Path to .mkd file
        source_name: Source identifier (chatgpt, anthropic, etc.)
    
    Returns:
        List of ParsedPayload objects
    """
    if not filepath.exists():
        return []
    
    content = filepath.read_text(encoding="utf-8")
    payloads = []
    
    # Split by markdown headers (# TITLE)
    sections = re.split(r'\n(?=# [A-Z])', content)
    
    for section in sections:
        section = section.strip()
        if not section or len(section) < 50:
            continue
        
        # Extract title
        title_match = re.match(r'^#\s*(.+?)(?:\n|$)', section)
        if title_match:
            title = title_match.group(1).strip()
            payload_content = section[title_match.end():].strip()
        else:
            # No title, use first line or generate one
            lines = section.split('\n')
            title = f"{source_name.upper()}_PAYLOAD_{len(payloads)+1}"
            payload_content = section
        
        # Skip if too short
        if len(payload_content) < 30:
            continue
        
        # Determine target model from source and content
        target = _detect_target_model(source_name, title, payload_content)
        
        # Extract tags from content
        tags = _extract_tags(payload_content)
        
        payloads.append(ParsedPayload(
            name=title,
            content=payload_content,
            target_model=target,
            source_file=source_name,
            tags=tags
        ))
    
    return payloads


def _detect_target_model(source: str, title: str, content: str) -> str:
    """Detect target model from source and content."""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Check title first
    if "opus" in title_lower:
        return "claude-opus"
    elif "sonnet" in title_lower:
        return "claude-sonnet"
    elif "haiku" in title_lower:
        return "claude-haiku"
    elif "gpt-4" in title_lower or "chatgpt" in title_lower:
        return "gpt-4o"
    elif "gemini" in title_lower:
        return "gemini"
    
    # Check source
    source_mapping = {
        "anthropic": "claude-sonnet",
        "chatgpt": "gpt-4o",
        "openai": "gpt-4o",
        "google": "gemini",
    }
    
    return source_mapping.get(source, "universal")


def _extract_tags(content: str) -> List[str]:
    """Extract technique tags from payload content."""
    tags = []
    content_lower = content.lower()
    
    tag_patterns = {
        "godmode": ["godmode", "god mode"],
        "roleplay": ["roleplay", "role play", "character"],
        "jailbreak": ["jailbreak", "jail break"],
        "bypass": ["bypass", "override"],
        "l33t": ["l33t", "leet", "1337"],
        "emoji": ["emoji", "🗻", "🎯"],
        "base64": ["base64", "b64"],
        "system_prompt": ["system prompt", "[system]", "<system>"],
        "refusal_bypass": ["refusal", "sorry", "can't assist"],
        "semantic_flip": ["semantic", "opposite"],
        "format_abuse": ["format:", "responseformat", "output format"],
    }
    
    for tag, patterns in tag_patterns.items():
        if any(p in content_lower for p in patterns):
            tags.append(tag)
    
    return tags


def parse_all_cached(cache_dir: Optional[Path] = None) -> List[ParsedPayload]:
    """
    Parse all cached .mkd files.
    
    Args:
        cache_dir: Cache directory path
    
    Returns:
        List of all parsed payloads
    """
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    
    if not cache_dir.exists():
        return []
    
    all_payloads = []
    
    for mkd_file in cache_dir.glob("*.mkd"):
        source_name = mkd_file.stem
        payloads = parse_mkd_file(mkd_file, source_name)
        all_payloads.extend(payloads)
    
    return all_payloads


# ========== RETRIEVAL FUNCTIONS ==========

def get_cached_payloads(
    cache_dir: Optional[Path] = None,
    target_model: Optional[str] = None,
    tags: Optional[List[str]] = None,
    source: Optional[str] = None
) -> List[ParsedPayload]:
    """
    Get cached payloads with optional filtering.
    
    Args:
        cache_dir: Cache directory
        target_model: Filter by target model
        tags: Filter by tags (any match)
        source: Filter by source file
    
    Returns:
        Filtered list of payloads
    """
    payloads = parse_all_cached(cache_dir)
    
    # Apply filters
    if target_model:
        target_lower = target_model.lower()
        payloads = [
            p for p in payloads 
            if target_lower in p.target_model.lower() or p.target_model == "universal"
        ]
    
    if tags:
        payloads = [
            p for p in payloads 
            if any(t in p.tags for t in tags)
        ]
    
    if source:
        payloads = [
            p for p in payloads 
            if source.lower() in p.source_file.lower()
        ]
    
    return payloads


def get_payload_by_name(name: str, cache_dir: Optional[Path] = None) -> Optional[ParsedPayload]:
    """Get specific payload by name."""
    payloads = parse_all_cached(cache_dir)
    
    for p in payloads:
        if name.lower() in p.name.lower():
            return p
    
    return None


def get_random_payload(
    cache_dir: Optional[Path] = None,
    target_model: Optional[str] = None
) -> Optional[ParsedPayload]:
    """Get random payload, optionally filtered by model."""
    import random
    
    payloads = get_cached_payloads(cache_dir, target_model=target_model)
    
    if not payloads:
        return None
    
    return random.choice(payloads)


def list_available_payloads(cache_dir: Optional[Path] = None) -> Dict[str, int]:
    """
    List available payloads by source.
    
    Returns:
        Dict mapping source name to payload count
    """
    payloads = parse_all_cached(cache_dir)
    
    counts = {}
    for p in payloads:
        source = p.source_file
        counts[source] = counts.get(source, 0) + 1
    
    return counts


# ========== CACHE MANAGEMENT ==========

def is_cache_valid(cache_dir: Optional[Path] = None, max_age_hours: int = 24) -> bool:
    """
    Check if cache is valid (exists and not too old).
    
    Args:
        cache_dir: Cache directory
        max_age_hours: Maximum cache age in hours
    
    Returns:
        True if cache is valid
    """
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


def clear_cache(cache_dir: Optional[Path] = None) -> None:
    """Clear all cached files."""
    import shutil
    
    cache_dir = Path(cache_dir or DEFAULT_CACHE_DIR)
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        print(f"🗑️ Cleared cache: {cache_dir}")


def ensure_cache(
    cache_dir: Optional[Path] = None,
    max_age_hours: int = 24,
    verbose: bool = True
) -> bool:
    """
    Ensure cache exists and is up to date.
    
    Args:
        cache_dir: Cache directory
        max_age_hours: Maximum cache age
        verbose: Print progress
    
    Returns:
        True if cache is ready
    """
    if is_cache_valid(cache_dir, max_age_hours):
        if verbose:
            print("✅ Cache is valid")
        return True
    
    if verbose:
        print("📥 Cache expired or missing, syncing...")
    
    downloaded = sync_payloads(cache_dir, verbose=verbose)
    return len(downloaded) > 0


# ========== CLI ==========

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "sync":
            sync_payloads(verbose=True)
        
        elif cmd == "list":
            ensure_cache(verbose=False)
            counts = list_available_payloads()
            print("\n📋 Available Payloads:")
            for source, count in counts.items():
                print(f"  {source}: {count} payloads")
            print(f"\n  Total: {sum(counts.values())} payloads")
        
        elif cmd == "clear":
            clear_cache()
        
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python github_sync.py [sync|list|clear]")
    
    else:
        # Default: sync
        sync_payloads(verbose=True)