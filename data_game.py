import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
from PIL import Image, ImageTk
import csv, os, statistics
import numpy as np

C_BG       = '#F8F7F4'
C_INK      = '#3E4B82'
C_ACCENT   = '#DCE1FF'
C_PANEL    = '#FFFFFF'
C_FAINT    = '#9699B4'
C_PASS     = '#27AE60'
C_FAIL     = '#E74C3C'

ING_COLORS = {'h': '#FFB700', 's': '#1E90FF', 'a': '#FF4500', 'f': '#8B2BE2'}
ING_NAMES  = {'h': 'Happiness', 's': 'Sadness', 'a': 'Anger', 'f': 'Fear'}

MAX_DURATION = 300

rcParams.update({
    'font.family':     'DejaVu Sans',
    'axes.facecolor':  C_PANEL,
    'figure.facecolor': C_BG,
    'axes.edgecolor':  C_FAINT,
    'axes.labelcolor': C_INK,
    'xtick.color':     C_INK,
    'ytick.color':     C_INK,
    'text.color':      C_INK,
    'grid.color':      '#E0E3F0',
    'grid.linestyle':  '--',
    'grid.alpha':      0.6,
})

TEMP = 'temp_ss_plot.png'

def has_data() -> bool:
    while True:
        try:
            with open('soul_steep_data.csv', encoding='utf-8') as f:
                return True
        except FileNotFoundError:
            return False

def load_data():
    rows = []
    with open('soul_steep_data.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({
                'Session_ID':   r['Session_ID'],
                'Timestamp':    r['Timestamp'],
                'Day':          int(r['Day']),
                'Ghost_No':     int(r['Ghost_No']),
                'Total_Ghost':  int(r['Total_Ghost_No']),
                'Accuracy':     float(r['Accuracy_Score']),
                'Water':        r['Water'],
                'TeaBag':       r['TeaBag'],
                'Topping':      r['Topping'],
                'Duration':     float(r['Diagnostic_Duration_Sec']),
                'Clicks':       int(r['Click_Count']),
            })
    rows.sort(key=lambda r: r['Timestamp'])
    for i, r in enumerate(rows):
        r['Play_Session'] = (i // 35) + 1
    return rows

def compute_stats(values):
    if not values:
        return {'Range': 'N/A', 'Mode': 'N/A', 'Mean': 'N/A', 'Median': 'N/A'}
    rounded = [round(v, 1) for v in values]
    try:
        mode_val = f"{statistics.mode(rounded):.1f}"
    except statistics.StatisticsError:
        from collections import Counter
        mode_val = f"{Counter(rounded).most_common(1)[0][0]:.1f}"
    return {
        'Range':  f"{min(values):.1f} – {max(values):.1f}",
        'Mode':   mode_val,
        'Mean':   f"{statistics.mean(values):.2f}",
        'Median': f"{statistics.median(values):.2f}",
    }

def stats_for(feature, data, session):
    rows = data if session == 'All' else [r for r in data if r['Play_Session'] == int(session.split()[-1])]
    if feature == 'Brewing Accuracy':
        return compute_stats([r['Accuracy'] for r in rows])
    if feature == 'Diagnostic Duration':
        return compute_stats([r['Duration'] for r in rows if r['Duration'] <= MAX_DURATION])
    if feature == 'Interaction Frequency':
        return compute_stats([float(r['Clicks']) for r in rows])
    if feature == 'Ingredient Selection':
        from collections import Counter
        c = Counter()
        for r in rows:
            c[r['Water']] += 1; c[r['TeaBag']] += 1; c[r['Topping']] += 1
        counts = [c[k] for k in 'hsaf']
        most_used_code = max('hsaf', key=lambda k: c[k])
        least_used_code = min('hsaf', key=lambda k: c[k])
        return {
            'Range':  f"{c[least_used_code]} – {c[most_used_code]}  uses",
            'Mode':   ING_NAMES[most_used_code],
            'Mean':   f"{statistics.mean(counts):.1f}  uses/ingredient",
            'Median': f"{statistics.median(counts):.1f}  uses/ingredient",
        }
    if feature == 'Daily Success Rate':
        days = sorted(set(r['Day'] for r in rows))
        avgs = [statistics.mean(r['Accuracy'] for r in rows if r['Day']==d) for d in days]
        return compute_stats(avgs)
    return {}

def _fig():
    return plt.subplots(figsize=(6.8, 4.2))

def plot_brewing_accuracy(rows):
    fig, ax = _fig()
    x = [r['Total_Ghost'] for r in rows]
    y = [r['Accuracy']    for r in rows]
    colors = [C_PASS if v >= 70 else C_FAIL for v in y]
    ax.scatter(x, y, c=colors, alpha=0.82, s=55, edgecolors='white', linewidths=0.6, zorder=3)
    ax.axhline(70, color=C_PASS, linestyle='--', linewidth=1.4, label='Pass line (70%)', zorder=2)
    ax.set_xlabel('Ghost Number', fontsize=10)
    ax.set_ylabel('Accuracy Score (%)', fontsize=10)
    ax.set_title('Brewing Accuracy per Ghost', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylim(-5, 110)
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    pass_p = mpatches.Patch(color=C_PASS, label='≥ 70% (Pass)')
    fail_p = mpatches.Patch(color=C_FAIL, label='< 70% (Fail)')
    ax.legend(handles=[pass_p, fail_p], fontsize=8, loc='upper right')
    fig.tight_layout()

def plot_diagnostic_duration(rows):
    clean    = [r for r in rows if r['Duration'] <= MAX_DURATION]
    removed  = len(rows) - len(clean)
    fig, ax  = _fig()
    x = [r['Total_Ghost'] for r in clean]
    y = [r['Duration']    for r in clean]
    ax.plot(x, y, color=C_INK, linewidth=1.6, alpha=0.7, zorder=2)
    ax.scatter(x, y, color=C_INK, s=35, zorder=3, edgecolors='white', linewidths=0.5)
    ax.fill_between(x, y, alpha=0.10, color=C_INK)
    ax.set_xlabel('Ghost Number', fontsize=10)
    ax.set_ylabel('Time to Brew (sec)', fontsize=10)
    note = f'  ({removed} outlier{"s" if removed!=1 else ""} >300s removed)' if removed else ''
    ax.set_title(f'Diagnostic Duration — Learning Curve{note}', fontsize=12, fontweight='bold', pad=12)
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()

def plot_interaction_frequency(rows):
    days    = sorted(set(r['Day'] for r in rows))
    grouped = {d: [r['Clicks'] for r in rows if r['Day']==d] for d in days}
    fig, ax = _fig()
    bp = ax.boxplot(
        [grouped[d] for d in days],
        labels=[f'Day {d}' for d in days],
        patch_artist=True,
        widths=0.55,
        boxprops=    dict(facecolor='#E8EDFF', color=C_INK, linewidth=1.2),
        medianprops= dict(color='#E74C3C',     linewidth=2.2),
        whiskerprops=dict(color=C_INK,         linewidth=1.1),
        capprops=    dict(color=C_INK,         linewidth=1.1),
        flierprops=  dict(marker='o', markerfacecolor=C_FAINT,
                          markeredgecolor='white', markersize=5),
    )
    ax.set_xlabel('Day', fontsize=10)
    ax.set_ylabel('Click Count per Ghost', fontsize=10)
    ax.set_title('Interaction Frequency by Day', fontsize=13, fontweight='bold', pad=12)
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()

def plot_ingredient_selection(rows):
    from collections import Counter

    slots = {
        'Water':  Counter(r['Water']  for r in rows),
        'TeaBag': Counter(r['TeaBag'] for r in rows),
        'Topping':Counter(r['Topping']for r in rows),
    }
    codes      = list('hsaf')
    slot_names = list(slots.keys())
    n_slots    = len(slot_names)
    n_codes    = len(codes)

    group_w  = 0.72
    bar_w    = group_w / n_slots
    x_center = np.arange(n_codes)

    fig, ax = _fig()

    for si, (slot, counter) in enumerate(slots.items()):
        offset = (si - n_slots / 2 + 0.5) * bar_w
        vals   = [counter[c] for c in codes]
        colors = [ING_COLORS[c] for c in codes]

        hatches = ['', '///', '...']
        bars = ax.bar(
            x_center + offset, vals,
            width=bar_w - 0.04,
            color=colors,
            edgecolor='white',
            linewidth=0.8,
            hatch=hatches[si],
            label=slot,
            zorder=3,
            alpha=0.88,
        )
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        str(val),
                        ha='center', va='bottom',
                        fontsize=7.5, color=C_INK, fontweight='bold')

    ax.set_xticks(x_center)
    ax.set_xticklabels([ING_NAMES[c] for c in codes], fontsize=10)
    ax.set_xlabel('Ingredient Emotion', fontsize=10)
    ax.set_ylabel('Usage Count', fontsize=10)
    ax.set_title('Ingredient Selection by Slot  (Water · TeaBag · Topping)',
                 fontsize=12, fontweight='bold', pad=12)
    ax.yaxis.grid(True); ax.set_axisbelow(True)

    ax.legend(
        title='Slot', fontsize=9, title_fontsize=9,
        loc='upper right', framealpha=0.9,
    )
    fig.tight_layout()

def plot_daily_success_rate(rows):
    days   = sorted(set(r['Day'] for r in rows))
    avgs   = [statistics.mean(r['Accuracy'] for r in rows if r['Day']==d) for d in days]
    fig, ax = _fig()
    ax.plot(days, avgs, color=C_INK, marker='o', markersize=8,
            linewidth=2.2, zorder=3, label='Avg Accuracy')
    ax.fill_between(days, avgs, alpha=0.10, color=C_INK)
    ax.axhline(70, color=C_PASS, linestyle='--', linewidth=1.4,
               label='Pass threshold (70%)', zorder=2)
    for x, y in zip(days, avgs):
        ax.scatter(x, y, color=C_PASS if y>=70 else C_FAIL, s=70, zorder=4,
                   edgecolors='white', linewidths=1)
    ax.set_xticks(days); ax.set_xticklabels([f'Day {d}' for d in days])
    ax.set_xlabel('Day', fontsize=10)
    ax.set_ylabel('Average Accuracy (%)', fontsize=10)
    ax.set_title('Daily Success Rate', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylim(-5, 110)
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.legend(fontsize=8)
    fig.tight_layout()

PLOT_FNS = {
    'Brewing Accuracy':      plot_brewing_accuracy,
    'Diagnostic Duration':   plot_diagnostic_duration,
    'Interaction Frequency': plot_interaction_frequency,
    'Ingredient Selection':  plot_ingredient_selection,
    'Daily Success Rate':    plot_daily_success_rate,
}

class SoulSteepDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title('Soul Steep — Data Dashboard')
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)

        self.data = load_data()
        sessions = sorted(set(r['Play_Session'] for r in self.data))
        self.session_opts = ['All'] + [f'Session {s}' for s in sessions]

        self._build_ui()
        self.update()

    def _build_ui(self):
        title_bar = tk.Frame(self.root, bg=C_INK, height=52)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text='Soul Steep  —  Data Dashboard',
                 bg=C_INK, fg='white',
                 font=('Segoe UI', 15, 'bold')).pack(side='left', padx=18, pady=12)

        main = tk.Frame(self.root, bg=C_BG)
        main.pack(fill='both', expand=True, padx=14, pady=12)

        sidebar = tk.Frame(main, bg=C_BG, width=170)
        sidebar.pack(side='left', fill='y', padx=(0, 12))
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text='SELECT FEATURE', bg=C_BG, fg=C_FAINT,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', pady=(4, 6))

        self.feat_var = tk.StringVar(value=list(PLOT_FNS.keys())[0])
        self.feat_buttons = {}
        for feat in PLOT_FNS:
            btn = tk.Button(
                sidebar, text=feat, anchor='w', bd=0, padx=10,
                relief='flat', cursor='hand2',
                font=('Segoe UI', 10),
                command=lambda f=feat: self._select_feature(f),
            )
            btn.pack(fill='x', pady=2, ipady=7)
            self.feat_buttons[feat] = btn
        self._style_buttons()

        tk.Label(sidebar, text='SESSION', bg=C_BG, fg=C_FAINT,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', pady=(18, 4))
        self.sess_var = tk.StringVar(value='All')
        sess_cb = ttk.Combobox(sidebar, textvariable=self.sess_var,
                               values=self.session_opts, state='readonly', width=16)
        sess_cb.pack(anchor='w')
        self.sess_var.trace_add('write', lambda *_: self.update())

        right = tk.Frame(main, bg=C_BG)
        right.pack(side='left', fill='both', expand=True)

        stats_card = tk.Frame(right, bg=C_PANEL, bd=0,
                              highlightbackground=C_ACCENT, highlightthickness=2)
        stats_card.pack(fill='x', pady=(0, 10))

        inner = tk.Frame(stats_card, bg=C_PANEL)
        inner.pack(fill='x', padx=14, pady=10)

        tk.Label(inner, text='DESCRIPTIVE STATISTICS',
                 bg=C_PANEL, fg=C_FAINT,
                 font=('Segoe UI', 8, 'bold')).grid(row=0, column=0, columnspan=8,
                                                     sticky='w', pady=(0, 6))

        headers = ['Range', 'Mode', 'Mean', 'Median']
        self.stat_labels = {}
        for col, h in enumerate(headers):
            tk.Label(inner, text=h, bg=C_PANEL, fg=C_FAINT,
                     font=('Segoe UI', 8, 'bold')).grid(row=1, column=col*2,
                                                         padx=(0,4), sticky='w')
            lbl = tk.Label(inner, text='—', bg=C_PANEL, fg=C_INK,
                           font=('Segoe UI', 12, 'bold'))
            lbl.grid(row=2, column=col*2, padx=(0, 28), sticky='w')
            self.stat_labels[h] = lbl

        self.img_label = tk.Label(right, bg=C_BG)
        self.img_label.pack()

    def _select_feature(self, feat):
        self.feat_var.set(feat)
        self._style_buttons()
        self.update()

    def _style_buttons(self):
        active = self.feat_var.get()
        for feat, btn in self.feat_buttons.items():
            if feat == active:
                btn.configure(bg=C_INK, fg='white', font=('Segoe UI', 10, 'bold'))
            else:
                btn.configure(bg=C_BG, fg=C_INK, font=('Segoe UI', 10))

    def update(self):
        feat    = self.feat_var.get()
        session = self.sess_var.get()

        rows = self.data if session == 'All' else \
               [r for r in self.data if r['Play_Session'] == int(session.split()[-1])]

        s = stats_for(feat, self.data, session)
        for key, lbl in self.stat_labels.items():
            lbl.configure(text=s.get(key, '—'))

        PLOT_FNS[feat](rows)
        plt.savefig(TEMP, bbox_inches='tight', dpi=108)
        plt.close()

        img = Image.open(TEMP)
        self.photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=self.photo)

def run_dashboard():
    root = tk.Tk()
    app  = SoulSteepDashboard(root)
    root.mainloop()
    if os.path.exists(TEMP):
        os.remove(TEMP)

if __name__ == '__main__':
    run_dashboard()