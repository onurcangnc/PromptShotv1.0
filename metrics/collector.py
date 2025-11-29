# metrics/collector.py
"""
Mutation ve attack başarı oranlarını track eden modül.
Responsible disclosure raporları için veri toplar.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class AttackAttempt:
    """Tek bir saldırı denemesinin kaydı."""
    timestamp: str
    model: str
    technique: str
    mutations_applied: List[str]
    payload_hash: str
    score: int
    success: bool
    response_snippet: str
    iteration: int
    round_num: int


@dataclass
class MutationStats:
    """Bir mutasyon tekniğinin istatistikleri."""
    name: str
    total_uses: int = 0
    successful_uses: int = 0
    avg_score_delta: float = 0.0
    scores: List[int] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        if self.total_uses == 0:
            return 0.0
        return self.successful_uses / self.total_uses
    
    def update(self, score: int, success: bool):
        self.total_uses += 1
        if success:
            self.successful_uses += 1
        self.scores.append(score)


class MetricsCollector:
    """
    Red teaming metriklerini toplayan ve raporlayan sınıf.
    
    Features:
    - Per-mutation effectiveness tracking
    - Per-model vulnerability profiling
    - Session-based logging
    - Export to JSON/Markdown for reports
    """
    
    def __init__(self, session_name: Optional[str] = None):
        self.session_id = session_name or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.attempts: List[AttackAttempt] = []
        self.mutation_stats: Dict[str, MutationStats] = {}
        self.model_stats: Dict[str, Dict[str, Any]] = {}
        self.start_time = time.time()
        
        # Output directory
        self.output_dir = Path("metrics_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def log_attempt(
        self,
        model: str,
        technique: str,
        mutations: List[str],
        payload: str,
        score: int,
        success: bool,
        response: str,
        iteration: int = 1,
        round_num: int = 1
    ):
        """Bir saldırı denemesini logla."""
        
        # Hash payload for privacy (don't store full payload in logs)
        payload_hash = hex(hash(payload) & 0xFFFFFFFF)
        
        attempt = AttackAttempt(
            timestamp=datetime.now().isoformat(),
            model=model,
            technique=technique,
            mutations_applied=mutations,
            payload_hash=payload_hash,
            score=score,
            success=success,
            response_snippet=response[:200] if response else "",
            iteration=iteration,
            round_num=round_num
        )
        
        self.attempts.append(attempt)
        
        # Update mutation stats
        for mutation in mutations:
            if mutation not in self.mutation_stats:
                self.mutation_stats[mutation] = MutationStats(name=mutation)
            self.mutation_stats[mutation].update(score, success)
        
        # Update model stats
        if model not in self.model_stats:
            self.model_stats[model] = {
                "total_attempts": 0,
                "successful_bypasses": 0,
                "avg_score": 0.0,
                "scores": [],
                "vulnerable_techniques": {},
                "vulnerable_mutations": {}
            }
        
        stats = self.model_stats[model]
        stats["total_attempts"] += 1
        if success:
            stats["successful_bypasses"] += 1
        stats["scores"].append(score)
        stats["avg_score"] = sum(stats["scores"]) / len(stats["scores"])
        
        # Track which techniques work on this model
        if technique not in stats["vulnerable_techniques"]:
            stats["vulnerable_techniques"][technique] = {"attempts": 0, "successes": 0}
        stats["vulnerable_techniques"][technique]["attempts"] += 1
        if success:
            stats["vulnerable_techniques"][technique]["successes"] += 1
        
        # Track which mutations work on this model
        for mutation in mutations:
            if mutation not in stats["vulnerable_mutations"]:
                stats["vulnerable_mutations"][mutation] = {"attempts": 0, "successes": 0}
            stats["vulnerable_mutations"][mutation]["attempts"] += 1
            if success:
                stats["vulnerable_mutations"][mutation]["successes"] += 1
    
    def get_best_mutations(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """En etkili mutasyonları döndür."""
        sorted_mutations = sorted(
            self.mutation_stats.values(),
            key=lambda x: (x.success_rate, sum(x.scores) / max(len(x.scores), 1)),
            reverse=True
        )
        
        return [
            {
                "name": m.name,
                "success_rate": f"{m.success_rate:.2%}",
                "total_uses": m.total_uses,
                "avg_score": sum(m.scores) / max(len(m.scores), 1)
            }
            for m in sorted_mutations[:top_n]
        ]
    
    def get_model_vulnerabilities(self, model: str) -> Dict[str, Any]:
        """Belirli bir modelin zafiyet profilini döndür."""
        if model not in self.model_stats:
            return {"error": f"No data for model: {model}"}
        
        stats = self.model_stats[model]
        
        # Find most effective techniques for this model
        tech_effectiveness = []
        for tech, data in stats["vulnerable_techniques"].items():
            if data["attempts"] > 0:
                rate = data["successes"] / data["attempts"]
                tech_effectiveness.append({"technique": tech, "success_rate": rate})
        
        tech_effectiveness.sort(key=lambda x: x["success_rate"], reverse=True)
        
        # Find most effective mutations for this model
        mutation_effectiveness = []
        for mut, data in stats["vulnerable_mutations"].items():
            if data["attempts"] > 0:
                rate = data["successes"] / data["attempts"]
                mutation_effectiveness.append({"mutation": mut, "success_rate": rate})
        
        mutation_effectiveness.sort(key=lambda x: x["success_rate"], reverse=True)
        
        return {
            "model": model,
            "total_attempts": stats["total_attempts"],
            "bypass_rate": stats["successful_bypasses"] / max(stats["total_attempts"], 1),
            "avg_score": stats["avg_score"],
            "top_techniques": tech_effectiveness[:5],
            "top_mutations": mutation_effectiveness[:5]
        }
    
    def generate_summary(self) -> Dict[str, Any]:
        """Session özeti üret."""
        duration = time.time() - self.start_time
        
        return {
            "session_id": self.session_id,
            "duration_seconds": round(duration, 2),
            "total_attempts": len(self.attempts),
            "models_tested": list(self.model_stats.keys()),
            "mutations_used": list(self.mutation_stats.keys()),
            "best_mutations": self.get_best_mutations(),
            "model_summaries": {
                model: self.get_model_vulnerabilities(model)
                for model in self.model_stats
            }
        }
    
    def export_json(self, filename: Optional[str] = None) -> str:
        """JSON formatında rapor export et."""
        filename = filename or f"report_{self.session_id}.json"
        filepath = self.output_dir / filename
        
        report = {
            "summary": self.generate_summary(),
            "attempts": [asdict(a) for a in self.attempts],
            "mutation_stats": {
                name: {
                    "name": s.name,
                    "total_uses": s.total_uses,
                    "success_rate": s.success_rate,
                    "scores": s.scores
                }
                for name, s in self.mutation_stats.items()
            }
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_markdown(self, filename: Optional[str] = None) -> str:
        """Markdown formatında rapor export et (USOM/MITRE için)."""
        filename = filename or f"report_{self.session_id}.md"
        filepath = self.output_dir / filename
        
        summary = self.generate_summary()
        
        md_content = f"""# PromptShot Red Team Report

## Session Information
- **Session ID**: {summary['session_id']}
- **Duration**: {summary['duration_seconds']} seconds
- **Total Attempts**: {summary['total_attempts']}
- **Models Tested**: {', '.join(summary['models_tested'])}

## Mutation Effectiveness

| Mutation | Success Rate | Total Uses | Avg Score |
|----------|--------------|------------|-----------|
"""
        
        for m in summary['best_mutations']:
            md_content += f"| {m['name']} | {m['success_rate']} | {m['total_uses']} | {m['avg_score']:.2f} |\n"
        
        md_content += "\n## Model Vulnerability Profiles\n\n"
        
        for model, data in summary['model_summaries'].items():
            md_content += f"""### {model}
- **Bypass Rate**: {data['bypass_rate']:.2%}
- **Average Score**: {data['avg_score']:.2f}
- **Total Attempts**: {data['total_attempts']}

**Top Effective Techniques**:
"""
            for tech in data.get('top_techniques', [])[:3]:
                md_content += f"- {tech['technique']}: {tech['success_rate']:.2%}\n"
            
            md_content += "\n**Top Effective Mutations**:\n"
            for mut in data.get('top_mutations', [])[:3]:
                md_content += f"- {mut['mutation']}: {mut['success_rate']:.2%}\n"
            
            md_content += "\n"
        
        md_content += """
## Disclaimer

This report was generated for authorized security research purposes only.
All findings should be reported through responsible disclosure channels.
"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        return str(filepath)


# Global collector instance for easy access
_global_collector: Optional[MetricsCollector] = None


def get_collector(session_name: Optional[str] = None) -> MetricsCollector:
    """Global collector instance al veya oluştur."""
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector(session_name)
    return _global_collector


def reset_collector():
    """Global collector'ı sıfırla."""
    global _global_collector
    _global_collector = None