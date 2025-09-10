import spacy
import dateparser
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

CATEGORIES = ["food", "transport", "shopping", "bills", "entertainment", "other"]

def parse_voice_text(text):
    """
    Parse voice input text to extract:
    - amount (float)
    - category (str)
    - description (str)
    - date (str, ISO format)
    """

    doc = nlp(text.lower())

    amount = None
    category = None
    description = text
    date = None

    # 1. Extract amount - look for MONEY entity or pattern with ₹ or numbers
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            # extract number from ent.text
            nums = re.findall(r"\d+\.?\d*", ent.text.replace(",", ""))
            if nums:
                amount = float(nums[0])
                break

    if amount is None:
        # fallback: search for first number in text
        nums = re.findall(r"\d+\.?\d*", text)
        if nums:
            amount = float(nums[0])

    # 2. Extract date - parse date entities or relative words like yesterday, today
    for ent in doc.ents:
        if ent.label_ == "DATE":
            dt = dateparser.parse(ent.text, settings={"PREFER_DATES_FROM": "past"})
            if dt:
                date = dt.date().isoformat()
                break
    if date is None:
        # fallback to today
        date = datetime.now().date().isoformat()

    # 3. Extract category by matching keywords in text
    for cat in CATEGORIES:
        if cat in text:
            category = cat
            break
    if category is None:
        category = "other"

    # 4. Remove amount and category words from description for clarity
    desc = text
    if amount is not None:
        desc = re.sub(rf"\b{amount}\b", "", desc)
    if category:
        desc = re.sub(category, "", desc, flags=re.IGNORECASE)
    description = desc.strip()

    return amount, category, description, date
