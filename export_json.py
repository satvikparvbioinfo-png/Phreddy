"""
Phreddy JSON Exporter
-----------------------
This file's ONLY job is saving results as a JSON file
(a format that other programs and websites can easily read).
"""
import json

def export_json(outfile, total, max_len, gc, n, overall, per_base):
    """Writes the summary and per-base stats into a JSON file."""
    data = {
        "summary": {
            "total_reads": total,
            "max_read_length": max_len,
            "gc_content": round(gc, 2),
            "n_content": round(n, 2),
            "overall_avg_quality": round(overall, 2)
        },
        "per_base": {}
    }

    for pos, (avg, min_s, max_s) in per_base.items():
        data["per_base"][str(pos)] = {
            "avg": round(avg, 2),
            "min": min_s,
            "max": max_s
        }

    with open(outfile, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"  📄 JSON report saved to {outfile}")