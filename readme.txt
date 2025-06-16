## Folder Structure

- `THEORY/`  
  Place all **input attainment sheets** here. Each file should correspond to a test or assignment.

- `OUTPUT/`  
  The **generated output** files will be saved here after processing.

Instructions to Run:

1. In `marksplit.py`, go to the end of the file.
   - Set the `for` loop index to match the file index from THEORY.
     Example: for i in [0, 1]
     Run each file seperately

2. From `extract.py`, go to line 10.
   - Ensure that `total_co`, `total_serial_tests`, and `total_assignments` are set correctly and match the structure in your attainment sheet.
   
3. In `question_paper.py`, go to line 31.
   - Set the `question_splitUp` based on the question paper pattern.
     Example: For a 50-mark paper → 2-mark × 9, 10-mark × 2, 12-mark × 1
     adjust as needed

4. To run the program:
   - Execute: `python marksplit.py`
   - Ensure the for-loop index is correctly set.

Common Error:

If you get an exception like:
Exception(f"obtained_mark not matched {student.name} {'serial_test' if serial_test else 'assignment'}{num} co{co.num}")

→ Go to `marksplit.py` line ~170  
→ Reduce the randomness in:
   `min(obtained_percentage + random.randint(0, 2), 100)`
   (Lower the 2 if needed)

Output:

- Generated files will be saved in the `OUTPUT/` folder.



