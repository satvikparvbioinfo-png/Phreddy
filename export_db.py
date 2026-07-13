"""
Phreddy SQLite Exporter
--------------------------
This file's ONLY job is saving results into a small database file
that can be searched using SQL later.
"""
import sqlite3

def export_sqlite(db_name, total, max_len, gc, n, overall, per_base):
    """Saves the summary and per-base stats into an SQLite database."""
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS stats
                     (metric TEXT PRIMARY KEY, value REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS per_base
                     (position INTEGER PRIMARY KEY, avg REAL, min INTEGER, max INTEGER)''')

        c.execute('DELETE FROM stats')
        c.execute('DELETE FROM per_base')

        metrics = [
            ('total_reads', total),
            ('max_read_length', max_len),
            ('gc_content', round(gc, 2)),
            ('n_content', round(n, 2)),
            ('overall_avg_quality', round(overall, 2))
        ]
        c.executemany('INSERT INTO stats VALUES (?, ?)', metrics)

        for pos, (avg, min_s, max_s) in per_base.items():
            c.execute('INSERT INTO per_base VALUES (?, ?, ?, ?)',
                      (pos, round(avg, 2), min_s, max_s))

    print(f"  🗄️  SQLite database saved to {db_name}")