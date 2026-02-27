# IP Tracker - First Semester Project
# A simple tool to look up IP address location info

import tkinter as tk
from tkinter import messagebox
import requests

# -- Colours --
BG     = "#1a1a2e"   # deep navy
PANEL  = "#16213e"   # darker navy panel
ACCENT = "#e2b96f"   # warm amber/gold
TEXT   = "#eaeaea"   # soft white
SOFT   = "#fcfcfc"   # muted blue-grey
BTN2   = "#c0392b"   # clear button red

def get_ip_info():
    ip = entry.get().strip()
    if not ip:
        messagebox.showwarning("Wait", "Enter an IP address!")
        return
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if data["status"] == "fail":
            messagebox.showerror("Not Found", f"No data for: {ip}")
            return
        values = [
            data.get("query", "N/A"),
            data.get("city", "N/A"),
            data.get("regionName", "N/A"),
            data.get("country", "N/A"),
            data.get("isp", "N/A"),
            f"{data.get('lat', 'N/A')},  {data.get('lon', 'N/A')}",
            data.get("timezone", "N/A"),
        ]
        for lbl, val in zip(value_labels, values):
            lbl.config(text=val)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "No internet connection.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_all():
    entry.delete(0, tk.END)
    for lbl in value_labels:
        lbl.config(text="—")

def hover(btn, color_on, color_off):
    btn.bind("<Enter>", lambda e: btn.config(bg=color_on))
    btn.bind("<Leave>", lambda e: btn.config(bg=color_off))

# -- Window --
root = tk.Tk()
root.title("IP Tracker")
root.geometry("440x460")
root.resizable(False, False)
root.config(bg=BG)

# -- Title --
tk.Label(root, text="IP Address Tracker", font=("Georgia", 16, "bold"),
         bg=BG, fg=ACCENT).pack(pady=(20, 2))
tk.Label(root, text="geolocation lookup tool",
         font=("Georgia", 9, "italic"), bg=BG, fg=SOFT).pack()
tk.Frame(root, bg=ACCENT, height=1).pack(fill="x", padx=30, pady=10)

# -- Input --
tk.Label(root, text="Enter IP Address:", font=("Georgia", 10),
         bg=BG, fg=SOFT).pack()

entry = tk.Entry(root, width=26, font=("Courier", 12),
                 bg=PANEL, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", highlightthickness=1,
                 highlightbackground=SOFT, highlightcolor=ACCENT)
entry.pack(ipady=5, pady=6)

# -- Buttons --
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=4)

btn_track = tk.Button(btn_frame, text="Track", command=get_ip_info,
                      bg=ACCENT, fg="#1a1a2e", font=("Georgia", 10, "bold"),
                      relief="flat", width=10, cursor="hand2")
btn_track.grid(row=0, column=0, padx=8, ipady=4)
hover(btn_track, "#f0c97a", ACCENT)

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_all,
                      bg=PANEL, fg=SOFT, font=("Georgia", 10),
                      relief="flat", width=10, cursor="hand2",
                      highlightthickness=1, highlightbackground=SOFT)
btn_clear.grid(row=0, column=1, padx=8, ipady=4)
hover(btn_clear, BTN2, PANEL)

tk.Frame(root, bg=ACCENT, height=1).pack(fill="x", padx=30, pady=10)

# -- Results --
results_frame = tk.Frame(root, bg=PANEL)
results_frame.pack(padx=30, fill="both")

fields = ["IP", "City", "Region", "Country", "ISP", "Coordinates", "Timezone"]
value_labels = []

for i, field in enumerate(fields):
    row_bg = PANEL if i % 2 == 0 else "#1e2a40"

    tk.Label(results_frame, text=field, font=("Georgia", 9, "bold"),
             bg=row_bg, fg=ACCENT, anchor="w", width=12,
             padx=8).grid(row=i, column=0, sticky="nsew", pady=2)

    val = tk.Label(results_frame, text="—", font=("Courier", 9),
                   bg=row_bg, fg=TEXT, anchor="w", width=26, padx=6)
    val.grid(row=i, column=1, sticky="nsew", pady=2)
    value_labels.append(val)
root.mainloop()