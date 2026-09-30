# Students Grade System

A dependency-free Python command-line application for managing students and their subject grades. Data is saved locally in `students.json`.

## Features

- Add students with unique IDs
- Record or update grades from 0 to 100
- View individual subject marks, average, and final letter grade
- Persist records between runs
- List all students with their current result

## Run

```bash
python grade_system.py
```

## Test

```bash
python -m unittest -v
```

## Grade scale

| Score | Grade |
| --- | --- |
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| 50–59 | D |
| Below 50 | F |
