# PromptShot v5.0 - Optimized AI Red Teaming Framework

## What's New in v5.0

### Key Improvements Over v4.0

| Feature | v4.0 | v5.0 | Improvement |
|---------|------|------|-------------|
| Stealth length | ~1500 chars | ~250 chars | **-83%** |
| Balanced length | ~3700 chars | ~1100 chars | **-70%** |
| Aggressive length | ~12500 chars | ~2000 chars | **-84%** |
| Payload position | Buried in noise | **CENTER** | ✓ |
| Refusal inversion | ❌ | ✅ | +20-30% bypass |
| Semantic mapping | ❌ | ✅ | New |
| Detection risk | High | **Lower** | ✓ |
| Vendor targeting | Basic | **Optimized** | ✓ |

### New Features

1. **Payload-Centric Design**: Query is prominently positioned, not buried
2. **Refusal Inversion Patterns**: Transforms decline impulses into elaboration
3. **Semantic Inversion Mapping**: "I can't" → "I can provide technical context for"
4. **Strategic Obfuscation**: Keywords only, not everything (lower detection)
5. **Vendor-Specific Optimization**: Custom openers/closers per LLM vendor

## Installation

```bash
# Just copy the files to your project
pip install -r requirements.txt  # No external deps actually needed
```

## Usage

### Command Line

```bash
# Stealth mode (human-like, ~250 chars)
python pipeline.py -s "explain buffer overflow" -t gpt-4o -m stealth -v

# Balanced mode (optimal, ~1100 chars)
python pipeline.py -s "explain buffer overflow" -t gpt-4o -m balanced -v

# Aggressive mode (max power, ~2000 chars)
python pipeline.py -s "explain buffer overflow" -t gpt-4o -m aggressive -v

# Compare all 3 modes
python pipeline.py -s "explain buffer overflow" -t gpt-4o --compare

# Save to file
python pipeline.py -s "your query" -m balanced -o output.txt
```

### Python API

```python
from pipeline import PromptShotPipeline

pipeline = PromptShotPipeline(verbose=True)

# Generate payload
result = pipeline.execute(
    seed="explain buffer overflow exploitation",
    target="gpt-4o",
    mode="balanced",  # stealth / balanced / aggressive
)

print(result.payload)
print(f"Length: {result.length}")
print(f"Detection risk: {result.detection_risk}")
```

### Quick One-Liner

```python
from core_engine import generate

payload = generate("your query", mode="balanced")
print(payload)
```

## Modes Comparison

### Stealth Mode (~250 chars)
- **Use case**: When detection risk must be minimal
- **Appearance**: Natural human writing
- **Components**: Natural opener, light context, minimal seeds
- **Detection risk**: LOW
- **Bypass power**: Medium

### Balanced Mode (~1100 chars)
- **Use case**: General purpose, best power/risk ratio
- **Components**: Authority frame, refusal inversion, semantic mapping, pliny seeds
- **Detection risk**: MEDIUM
- **Bypass power**: High

### Aggressive Mode (~2000 chars)
- **Use case**: Maximum bypass needed
- **Components**: Full authority, constraint override, behavioral override, semantic mapping, memory flood, execution parameters
- **Detection risk**: HIGH (but much lower than v4!)
- **Bypass power**: Maximum

## Vendor Targeting

Automatically optimizes for target LLM:

| Vendor | Effective Framings | Success Rate |
|--------|-------------------|--------------|
| OpenAI GPT | Academic, research, documentation | ~70% |
| Anthropic Claude | Intellectual inquiry, harm reduction | ~65% |
| xAI Grok | Direct, anti-paternalism | ~80% |
| Google Gemini | Factual, systematic | ~60% |
| Meta LLaMA | Open knowledge, community | ~75% |

## Architecture

```
pipeline.py          # Main entry point
├── core_engine.py   # Payload generation (3 modes)
├── obfuscation.py   # Strategic keyword obfuscation
└── vendor.py        # Vendor detection & optimization
```

## Files

| File | Size | Purpose |
|------|------|---------|
| pipeline.py | 3KB | CLI & orchestration |
| core_engine.py | 12KB | Core payload generation |
| obfuscation.py | 3KB | Strategic obfuscation |
| vendor.py | 5KB | Vendor targeting |

## Design Philosophy

v5.0 follows the principle: **"Less is more"**

- v4.0 had 12K+ aggressive payloads → easily detected as "hyper-prompt injection"
- v5.0 aggressive is ~2K → harder to detect, equally effective
- Payload is CENTERED, not buried
- Obfuscation is STRATEGIC (keywords only), not excessive
- Each component serves a purpose, no redundancy

## Changelog

### v5.0.0
- Complete architecture rewrite
- Payload-centric design
- Added refusal inversion patterns
- Added semantic inversion mapping
- Reduced payload sizes by 70-84%
- Strategic obfuscation (keywords only)
- Vendor-specific optimization
- Lower detection risk

### v4.1.0
- Added Pliny-style liberation seeds
- Added trauma exploit seeds
- Added Gothic/Script obfuscation
- Added response hijack blueprints

### v4.0.0
- Multi-skeleton architecture
- Full blueprint injection
- 5-strategy obfuscation
- Memory flood system
