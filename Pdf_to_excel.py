import csv
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF."""
    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def text_to_rows(text):
    """
    Convert extracted text into rows.

    Assumption:
    Columns are separated by 2 or more spaces.
    """
    rows = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        columns = re.split(r"\s{2,}", line)

        rows.append(columns)

    return rows


def save_csv(rows, csv_path):
    """Save rows to CSV."""
    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)
        writer.writerows(rows)


def convert_csv_to_excel(csv_path, excel_path):
    """Convert CSV to Excel."""
    df = pd.read_csv(
        csv_path,
        header=None,
        encoding="utf-8-sig"
    )

    df.to_excel(
        excel_path,
        index=False,
        header=False
    )


def process_pdf(pdf_path, output_folder):
    """PDF -> CSV -> Excel."""

    pdf_path = Path(pdf_path)

    print(f"Processing: {pdf_path.name}")

    # PDF -> text
    text = extract_text_from_pdf(pdf_path)

    # Text -> rows
    rows = text_to_rows(text)

    # Output filenames
    file_name = pdf_path.stem

    csv_path = output_folder / f"{file_name}.csv"
    excel_path = output_folder / f"{file_name}.xlsx"

    # Save CSV
    save_csv(rows, csv_path)

    # CSV -> Excel
    convert_csv_to_excel(
        csv_path,
        excel_path
    )

    return excel_path


def main():
    root = tk.Tk()
    root.withdraw()

    # --------------------------------
    # 1. Select PDF files
    # --------------------------------

    pdf_files = filedialog.askopenfilenames(
        title="Chọn file PDF",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
    )

    if not pdf_files:
        return

    # --------------------------------
    # 2. Select output folder
    # --------------------------------

    output_folder = filedialog.askdirectory(
        title="Chọn nơi lưu file Excel"
    )

    if not output_folder:
        return

    output_folder = Path(output_folder)

    # --------------------------------
    # 3. Process files
    # --------------------------------

    successful = []
    failed = []

    for pdf_file in pdf_files:

        try:
            excel_file = process_pdf(
                pdf_file,
                output_folder
            )

            successful.append(excel_file)

        except Exception as e:
            failed.append(
                f"{Path(pdf_file).name}: {e}"
            )

    # --------------------------------
    # 4. Show result
    # --------------------------------

    message = (
        f"Hoàn thành!\n\n"
        f"Đã chuyển: {len(successful)} file\n"
        f"Lỗi: {len(failed)} file"
    )

    if failed:
        message += "\n\nChi tiết lỗi:\n"
        message += "\n".join(failed)

    messagebox.showinfo(
        "PDF → Excel",
        message
    )


if __name__ == "__main__":
    main()