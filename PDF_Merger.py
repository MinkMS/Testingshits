import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfMerger

"""
Notes:
- Requires PyPDF2 installed: pip install PyPDF2
- Running this script will show GUI dialogs (no main window displayed)
- Consider adding validation for overwriting existing files or choosing output path
- For large PDFs or many files, consider using streaming/temporary files to reduce memory usage
"""

def merge_pdfs():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(
        title="Select files to merge: ",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_paths:
        messagebox.showinfo("Notification", "No file selected!")
        return

    file_paths = sorted(file_paths)

    output_file = simpledialog.askstring("Output file name", "File name(No .pdf needed):")
    if not output_file:
        messagebox.showinfo("Notification", "No name!")
        return

    output_file += ".pdf"

    merger = PdfMerger()
    for pdf in file_paths:
        merger.append(pdf)

    try:
        merger.write(output_file)
        merger.close()
        messagebox.showinfo("Success", f"Merge completed! File saved at: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Couldn't save the file: {e}")

if __name__ == "__main__":
    merge_pdfs()