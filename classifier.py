def classify_idea(text):
    text = text.lower()

    if "ai" in text or "machine learning" in text:
        domain = "AI"
    elif "app" in text or "mobile" in text:
        domain = "Mobile"
    elif "website" in text or "web" in text:
        domain = "Web"
    else:
        domain = "General"

    length = len(text.split())

    if length < 30:
        complexity = "Low"
    elif length < 60:
        complexity = "Medium"
    else:
        complexity = "High"

    return domain, complexity
