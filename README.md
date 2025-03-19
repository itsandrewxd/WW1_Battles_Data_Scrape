# WW1_Battles_Data_Scrape
# Overview of the WWI Battles Data Cleaning Project

Below is a summary of the steps we’ve taken to scrape, clean, and partially standardize the WWI battles dataset from Wikipedia. It includes references to the relevant `.py` scripts and highlights areas where further refinements are still needed.

---

## 1. Initial Scrape

- **Script:** `ww1scrape.py`  
- **Goal:** Gather raw data from Wikipedia pages about WWI battles.
- **Outcome:**  
  - Produced an initial CSV with columns such as:
    - `BattleName`
    - `StartDate`
    - `EndDate`
    - `Location`
    - `Outcome`
    - `Belligerents_Right`
    - `Belligerents_Left`
    - `Strength_Right`
    - `Strength_Left`
    - `Casualties and losses_Right`
    - `Casualties and losses_Left`
  - The scraped data was messy, with:
    - Inconsistent formatting
    - References in square brackets (e.g. `[1]`)
    - Non-ASCII characters
    - Dates with partial or no year

---

## 2. Initial Cleaning

- **Script:** `WW1_Clean_V1.py`
- **Key Steps:**
  1. **Encoding & Reading**  
     - Ensured the CSV was read with `encoding='utf-8'` or `encoding='utf-8-sig'`.
     - Created backup DataFrames to avoid overwriting data during experimentation.
  2. **Battle Names**  
     - Removed non-ASCII or garbled characters from scraping.
     - Stripped bracket references.
     - Removed embedded years (e.g. “(1914)”).
  3. **Dates**  
     - Created functions to handle partial dates, bracketed text like `[O.S. 4 August]`.
     - Used logic such as:
       - If `StartDate` is just a day number but the `EndDate` has a month/year, infer the same or previous month.
       - Converted everything to a standardized date format (often `dd-mm-yyyy` or ISO‐8601).
     - Manual fixes for tough edge cases were done in a separate script (`By_Hand_Fix_Quick.py`).

---

## 3. Casualties & Losses Columns

- **Goal:** Extract meaningful structured data (like `killed`, `wounded`, `missing`, `captured`, or a simple `casualties` total).
- **Approach:**
  1. **Removed references** in square brackets to avoid merging numbers (e.g. `"1000[2]"` → `"1000"`).
  2. **Regexes** to capture patterns like:
     - `"X killed"`, `"Y wounded"`, `"Z missing"`, etc.
     - Ranges `"X–Y"`.
     - If only a single number is present, interpret it as total casualties.
  3. **Output:**  
     - New columns (`Casualties_dict_right`, `Casualties_dict_left`) containing dictionaries, e.g.:
       ```python
       {
         "killed": [509.0],
         "wounded": [4359.0],
         "missing": [1534.0],
         "total": [6402.0]
       }
       ```
     - Removed month names (e.g. `"august"`) if they accidentally got parsed as a key.
  4. **Remaining Issues:**  
     - **Accuracy**: Some rows have ambiguous or multi-sourced data.
     - **Different synonyms** (e.g. “POW,” “captured,” “taken prisoner”) might not be fully standardized.
     - **Complex multi-sentence cells** can still throw off our regex approach.

---

## 4. Strength Columns

- **Goal:** Parse `Strength_Right` and `Strength_Left` into structured numeric data with descriptors (`infantry`, `cavalry`, `troops`, etc.).
- **Approach:**  
  1. **Regex** capturing `(number or range) + descriptor`, for example `"10,000–12,000 men"`.  
  2. **If descriptor is `"men"` or `"in"`, rename it to `"troops"`.  
  3. **If it’s a single number only (including approximate “c.300”), interpret as `"troops"`.  
  4. **Look for `"Total: XXX"` or `"XXX total"` and store it under `"total"`.
- **Challenges:**  
  - Some rows have multiple stats jammed together without consistent separators (e.g. `"272,000 men, 750 machine guns, 3,058 guns"`).  
  - Regex isn’t always robust enough for complex formatting or missing commas.  
  - We replaced bracketed refs with spaces to avoid `"1000[2][c]750"` → `"1000750"` merges.

---

## 5. Manual Fixes & Future Work

- **Manual Fixes:**  
  - A few battles needed date corrections by hand (`By_Hand_Fix_Quick.py`).
  - Some casualties/strength rows required manual input due to extremely inconsistent data or conflicting sources.

- **Areas to Improve:**  
  1. **Validation of Parsed Data**  
     - Summaries of how many keys were created (e.g. “troops,” “infantry,” “machine guns”).  
     - Spot-check a sample of battles to confirm correctness.
  2. **Better Handling of Multi-Word Descriptors**  
     - “machine guns,” “light artillery,” etc. might need an updated regex if we want them recognized as a single descriptor.
  3. **De-duplicating Overlapping Info**  
     - If the same number is repeated under different labels (e.g. “including,” “total”), we can unify them.
  4. **Unified Collation**  
     - Possibly flatten the dictionaries into columns (e.g. `troops_right`, `cavalry_right`) if numeric analysis is needed.
  5. **Quality Checks**  
     - Some entries say “unknown” or “heavy losses.” We may store them as `NaN` or text but can’t do numeric analysis on them.

---

## Conclusion

**This dataset, while improved, still has complexities** due to messy historical data and variable Wikipedia formatting. We’ve used a combination of:

- _Regex-based extraction_  
- _Fallback logic for single numbers_  
- _Manual fixes for irreconcilable rows_

**Next steps** might involve deeper inspection of each battle’s row to ensure accuracy or a more sophisticated natural language processing approach. For quick analysis and visualizations, however, our current methods provide a decent structured foundation.

  
**Relevant Scripts:**
- **`ww1scrape.py`**: Initial scrape from Wikipedia.  
- **`WW1_Clean_V1.py`**: Main cleaning of names, dates, partial casualties logic.  
- **`By_Hand_Fix_Quick.py`**: Manual date corrections.  
- **Strength & Casualties** logic as seen in the notebook or integrated `.py` files containing functions like `parse_casualties_with_total`, `parse_strength`, etc.

