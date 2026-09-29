import csv
from pathlib import Path
from tkinter import filedialog, messagebox


def clear_tree(tree):
    tree.delete(*tree.get_children())


def sort_tree(tree, column, reverse=False):
    items = [(tree.set(item, column), item) for item in tree.get_children("")]
    try:
        items.sort(key=lambda x: float(x[0].replace(",", "")), reverse=reverse)
    except ValueError:
        items.sort(key=lambda x: x[0].casefold(), reverse=reverse)
    for index, (_, item) in enumerate(items):
        tree.move(item, "", index)
    tree.heading(column, command=lambda: sort_tree(tree, column, not reverse))


def export_rows_to_csv(parent, rows, headers, suggested_name):
    if not rows:
        messagebox.showinfo("Nothing to export", "There are no records to export.", parent=parent)
        return False
    path = filedialog.asksaveasfilename(
        parent=parent,
        title="Export CSV",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=suggested_name,
    )
    if not path:
        return False
    target = Path(path)
    if target.exists() and not messagebox.askyesno("Confirm overwrite", f"{target.name} already exists. Overwrite it?", parent=parent):
        return False
    try:
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Export complete", f"Saved {len(rows)} record(s) to:\n{target}", parent=parent)
        return True
    except OSError as exc:
        messagebox.showerror("Export failed", f"Could not save the CSV:\n{exc}", parent=parent)
        return False
