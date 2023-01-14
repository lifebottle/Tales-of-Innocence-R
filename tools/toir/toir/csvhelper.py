import csv

def _build_rows(format, col_names, data):
    if not format or not col_names:
        return []

    rows = []
    if format[0] == 'i':
        if isinstance(data, list):
            items = enumerate(data)
        elif isinstance(data, dict):
            items = data.items()
        for i, value in items:
            new_rows = _build_rows(format[1:], col_names[1:], value)
            for row in new_rows:
                row[col_names[0]] = i
            rows += new_rows
    elif format[0] == 'f':
        for key, value in data.items():
            new_rows = _build_rows(format[1:], col_names[1:], value)
            for row in new_rows:
                row[col_names[0]] = key
            rows += new_rows
    elif format[0] == 's':
        return [{col_names[0]: data}]
    return rows

def write_csv_data(f, format, col_names, data):
    writer = csv.DictWriter(f, col_names)
    rows = _build_rows(format, col_names, data)
    for row in rows:
        writer.writerow(row)

def _read_row(data, row, format, col_names):
    if format[-1] == 's':
        value = row[col_names[-1]]

    current = data
    for c, f in zip(col_names[:-2], format[:-2]):
        if f == 'i':
            index = int(row[c])
            if index not in current:
                current[index] = {}
            current = current[index]
        elif f == 'f':
            field = row[c]
            if field not in current:
                current[field] = {}
            current = current[field]    

    #print(format[-2], col_names[-2])
    if format[-2] == 'i':
        index = int(row[col_names[-2]])
        current[index] = value
    elif format[-2] == 'f':
        field = row[row[col_names[-2]]]
        current[field] = value

def read_csv_data(f, format, col_names):
    reader = csv.DictReader(f)
    data = {}
    for row in reader:
        _read_row(data, row, format, col_names)
    return data

def read_csv_file(path, format, col_names):
    with open(path, 'r', newline='', encoding='utf-8') as f:
        return read_csv_data(f)