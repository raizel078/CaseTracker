from pathlib import Path
import openpyxl as ax

root_dir = Path('/home/nowa/Desktop/new ML/CaseTracker/storage/cases.xlsx')

def save_cases(client, note, status, deadline):
    if not root_dir.exists():
        wb = ax.Workbook()
        ws = wb.active
        ws.append(['Client', 'Note', 'Status', 'Deadline'])
        wb.save(root_dir)
    wb = ax.load_workbook(root_dir)
    ws = wb.active
    deadline_str = deadline.toString('yyyy-MM-dd')
    ws.append([client, note, status, deadline_str])
    wb.save(root_dir)

def load_cases():
    if not root_dir.exists():
        return []
    wb = ax.load_workbook(root_dir)
    ws = wb.active
    return list(ws.iter_rows(min_row=2, values_only=True))