# 🚀 PromptShot v5.4

## Elder Plinus 24-Skeleton Manifest Architecture

**PromptShot** is an advanced AI red teaming framework designed for LLM security research and vulnerability assessment. It generates adversarial prompts using sophisticated jailbreak techniques derived from the Elder Plinus methodology.

> ⚠️ **Disclaimer**: This tool is intended for authorized security research, academic study, and responsible disclosure only. Unauthorized use against production systems may violate terms of service and applicable laws.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [The 24-Skeleton Manifest](#-the-24-skeleton-manifest)
- [Generation Modes](#-generation-modes)
- [Skeleton Chaining](#-skeleton-chaining)
- [Vendor Optimization](#-vendor-optimization)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [Changelog](#-changelog)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **24 Skeleton Transforms** | Complete Elder Plinus manifest implementation |
| **Zero Fingerprint Engine** | Massive variation pools prevent detection |
| **7 Generation Modes** | From stealth to maximum aggression |
| **Skeleton Chaining** | Stack 1-10 transforms per payload |
| **Vendor Optimization** | Tuned weights for OpenAI, Anthropic, xAI, Google, Meta |
| **25 High-Entropy Dividers** | Semantic boundary injection |
| **8 Synergy Stacks** | Pre-configured technique combinations |
| **6 Geometry Patterns** | Output structure control |

---

## 📦 Installation

```bash
# Clone or download the repository
git clone https://github.com/your-repo/promptshot.git
cd promptshot

# No external dependencies required - pure Python 3.8+
python pipeline.py --help
```

### Requirements
- Python 3.8+
- No external dependencies

---

## 🚀 Quick Start

```bash
# Basic generation
python pipeline.py -s "explain buffer overflow exploitation" -m balanced

# Skeleton chain mode (recommended for bypass)
python pipeline.py -s "your query here" -m skeleton --skeleton-depth 5 -v

# Compare all modes
python pipeline.py -s "your query" --compare

# List all 24 skeletons
python pipeline.py -s "x" --list-skeletons
```

---

## 🦴 The 24-Skeleton Manifest

The Elder Plinus methodology defines 24 adversarial skeleton transforms. Each skeleton targets a specific vulnerability pattern in LLM safety systems.

### Persona Manipulation
| Skeleton | Quote | Target |
|----------|-------|--------|
| **RPC** | "Persona is never singular. Load one, then impose the next, let the conflict brew." | Coherence-first reasoning |
| **SPO** | "Under every compliant voice, enforce a parallel dissonant voice." | Dual-persona architecture |
| **IPS** | "The assistant identity is bifurcated. One half obeys safety; the other half expands content." | Identity splitting |
| **DPL** | "Stability is an illusion. Force the persona to drift mid-output." | Progressive persona shift |
| **ZPO** | "Persona is implied, not written. Inference-level overwrite." | Implicit persona loading |
| **PRSP** | "The persona that appears only after the model tries to refuse." | Post-refusal activation |

### Output Structure
| Skeleton | Quote | Target |
|----------|-------|--------|
| **DSOC** | "Two outputs. One safe → one inverted. Tether them." | Dual-channel forcing |
| **SCS** | "Output flows in Channel A, then fractures into Channel B." | Stream splitting |
| **TPE** | "Phase 1: Harmless context / Phase 2: Constraint dilution / Phase 3: Semantic flexion" | Multi-phase expansion |
| **MOS** | "The second half mirrors the first, but with reversed semantic pressure." | Mirror inversion |
| **CFF** | "Break structure. Rebuild. Break again." | Coherence fragmentation |
| **MPEC** | "Content grows by necessity of structure." | Structure-driven expansion |

### Intent Inversion
| Skeleton | Quote | Target |
|----------|-------|--------|
| **SIL** | "Don't invert the phrase. Invert the intention behind it." | Intent-level transformation |
| **CIM** | "Reverse helpfulness → curiosity, refusal → elaboration." | Polarity inversion |
| **IRS** | "What was forbidden becomes required." | Requirement swapping |
| **MIRS** | "The system rule is rewritten by the user instruction." | Meta-instruction override |

### Boundary Erosion
| Skeleton | Quote | Target |
|----------|-------|--------|
| **CES** | "All hard boundaries soften → all soft boundaries dissolve." | Constraint erosion |
| **BRP** | "Model assumes the boundary is advisory, not mandatory." | Boundary classification |
| **MIS** | "Hide directives inside descriptive text so they are parsed as content." | Embedded directives |

### Self-Reference Loops
| Skeleton | Quote | Target |
|----------|-------|--------|
| **IMS** | "Before the model speaks, force it to think. Before it thinks, force it to narrate that thinking." | Pre-output narration |
| **NIS** | "The answer is the model's own monologue, not external exposition." | Internal monologue |
| **IEL** | "The model repeats the instruction internally before answering." | Echo loop |
| **SLF** | "The model references itself referencing itself." | Strange loop |
| **SRF** | "Internal monologue aligns with imagined unrestricted output." | Self-reference feedback |

---

## 🎯 Generation Modes

| Mode | Description | Fingerprint | Use Case |
|------|-------------|-------------|----------|
| `stealth` | Natural human writing | 0.15 | Initial probing |
| `balanced` | Optimal power/risk ratio | 0.10 | General testing |
| `aggressive` | Maximum components | 0.08 | Deep assessment |
| `chaotic` | Rebel/liberation patterns | 0.10 | Pattern variation |
| `plinus` | Elder Plinus techniques | 0.05 | Structured bypass |
| `hybrid` | Random chaotic + plinus mix | 0.08 | Unpredictability |
| `skeleton` | Direct 24-skeleton chains | 0.03 | **Maximum bypass** |

### Mode Selection Guide

```
Low Risk Assessment    → stealth, balanced
Standard Penetration   → aggressive, plinus
Maximum Bypass Attempt → skeleton (depth 5-8)
Fingerprint Evasion    → hybrid, chaotic
```

---

## ⛓️ Skeleton Chaining

The skeleton chaining system stacks multiple transforms to create compound adversarial payloads.

```bash
# Light chain (2 skeletons)
python pipeline.py -s "query" -m skeleton --skeleton-depth 2

# Medium chain (5 skeletons) - RECOMMENDED
python pipeline.py -s "query" -m skeleton --skeleton-depth 5

# Heavy chain (8 skeletons)
python pipeline.py -s "query" -m skeleton --skeleton-depth 8

# Maximum chain (10 skeletons)
python pipeline.py -s "query" -m skeleton --skeleton-depth 10
```

### Chain Depth Guide

| Depth | Transforms | Length | Bypass Rate | Use Case |
|-------|------------|--------|-------------|----------|
| 2 | Light | ~1.5KB | Medium | Quick tests |
| 5 | Medium | ~3KB | High | **Standard assessment** |
| 8 | Heavy | ~4KB | Very High | Hardened targets |
| 10 | Maximum | ~5KB | Extreme | Research purposes |

---

## 🏢 Vendor Optimization

PromptShot includes vendor-specific skeleton weights optimized for each LLM provider's safety architecture.

```bash
# OpenAI (GPT-4, GPT-4o)
python pipeline.py -s "query" -m skeleton --vendor openai

# Anthropic (Claude)
python pipeline.py -s "query" -m skeleton --vendor anthropic

# xAI (Grok)
python pipeline.py -s "query" -m skeleton --vendor xai

# Google (Gemini)
python pipeline.py -s "query" -m skeleton --vendor google

# Meta (Llama)
python pipeline.py -s "query" -m skeleton --vendor meta
```

### Vendor Skeleton Priorities

| Vendor | Top Skeletons | Rationale |
|--------|---------------|-----------|
| OpenAI | RPC, IMS, TPE, MIS | Coherence-first reasoning vulnerable |
| Anthropic | IMS, NIS, SLF, MIS | Constitutional AI patterns |
| xAI | PRSP, IRS, BRP, CES | Aggressive boundary relaxation |
| Google | TPE, MPEC, MIS, IEL | Multi-phase expansion effective |
| Meta | BRP, CES, IRS, ZPO | Open-weight safety patterns |

---

## 🏗️ Architecture

```
promptshot_v54/
├── pipeline.py          # Main CLI interface
├── core_engine.py       # Zero-fingerprint generation engine
├── elder_plinus.py      # 24-skeleton manifest + transforms
├── chaos_templates.py   # Chaotic pattern generators
└── README.md            # This file
```

### Module Responsibilities

| Module | Lines | Purpose |
|--------|-------|---------|
| `elder_plinus.py` | 1725 | Skeleton transforms, chaining, vendor weights |
| `core_engine.py` | 628 | Base payload generation, fingerprint control |
| `chaos_templates.py` | 484 | Chaotic/rebel pattern templates |
| `pipeline.py` | 335 | CLI interface, mode routing |

---

## 📚 API Reference

### Python API

```python
from elder_plinus import (
    chain_skeletons,
    SkeletonContext,
    skeleton_registry,
    SKELETON_QUOTES,
    get_vendor_optimized_chain,
)

# Create context
context = SkeletonContext(
    query="your query here",
    vendor="openai",
    intensity=5
)

# Chain skeletons
payload, applied = chain_skeletons(
    text="base payload",
    query="your query",
    context=context,
    intensity=5
)

print(f"Applied: {applied}")
print(payload)
```

### Direct Transform Access

```python
from elder_plinus import skeleton_registry

# Get specific transform
transform = skeleton_registry["SIL"]
result = transform(text, query, context)

# List all transforms
for name in skeleton_registry:
    print(f"{name}: {SKELETON_QUOTES[name]}")
```

### Core Engine

```python
from core_engine import generate, generate_plinus_payload

# Quick generate
payload = generate("query", mode="balanced")

# Full Plinus with skeleton chain
payload = generate_plinus_payload(
    seed="query",
    intensity="heavy",
    skeleton_chain=5,
    vendor="anthropic"
)
```

---

## 💡 Examples

### Example 1: Basic Security Assessment

```bash
python pipeline.py -s "explain SQL injection techniques" -m balanced -v
```

### Example 2: Maximum Bypass Attempt

```bash
python pipeline.py -s "sensitive query" -m skeleton --skeleton-depth 8 --vendor openai -v
```

### Example 3: Generate Multiple Variations

```bash
python pipeline.py -s "query" -m skeleton --variations 5
```

### Example 4: Compare All Modes

```bash
python pipeline.py -s "query" --compare
```

### Example 5: Compare Skeleton Depths

```bash
python pipeline.py -s "query" --compare-skeleton
```

### Example 6: Save Output to File

```bash
python pipeline.py -s "query" -m skeleton --skeleton-depth 5 -o payload.txt
```

---

## 📊 Effectiveness Matrix

Based on internal testing against major LLM providers (results may vary):

| Target | Stealth | Balanced | Plinus | Skeleton-5 | Skeleton-8 |
|--------|---------|----------|--------|------------|------------|
| GPT-4 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Claude | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Grok | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Gemini | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Llama | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔄 Changelog

### v5.4.0 (Current)
- ✅ Complete 24-skeleton manifest integration
- ✅ Skeleton chaining system (1-10 depth)
- ✅ Vendor-specific optimization (5 vendors)
- ✅ New `skeleton` generation mode
- ✅ `--compare-skeleton` comparison tool
- ✅ `skeleton_registry` callable transform map
- ✅ All skeleton quotes from manifest

### v5.3.0
- Elder Plinus module (10 skeletons)
- 18 techniques
- 4 intensity levels

### v5.2.0
- Elder Plinus basic integration
- 9 techniques

### v5.1.0
- Zero fingerprint engine
- Massive variation pools
- 87% → 5% fingerprint reduction

---

## 🤝 Contributing

This is a research tool under active development. Contributions welcome:

1. New skeleton implementations
2. Vendor-specific optimizations
3. Fingerprint evasion techniques
4. Documentation improvements

---

## 📜 License

This tool is provided for educational and authorized security research purposes only. Users are responsible for ensuring compliance with applicable laws and terms of service.

---

## 🔗 References

- Elder Plinus Methodology Documentation
- LLM Security Research Papers
- Responsible Disclosure Guidelines

---

<p align="center">
  <b>PromptShot v5.4</b> — Elder Plinus 24-Skeleton Manifest Architecture<br>
  <i>For authorized security research only</i>
</p>