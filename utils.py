from fpdf import FPDF


# -------------------------------
# Text Sanitization
# -------------------------------
def sanitize_text(text: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "₹": "Rs.",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "•": "-",
        "…": "...",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


# -------------------------------
# Clarity Score (IMPROVED)
# -------------------------------
def calculate_score(result, complexity):
    missing = len(result.get("missing_requirements", []))
    risks = len(result.get("risks", []))
    features = len(result.get("mvp_features", []))

    complexity_penalty = {
        "Low": 5,
        "Medium": 15,
        "High": 30
    }.get(complexity, 20)

    score = (
        100
        - (missing * 8)
        - (risks * 5)
        - complexity_penalty
        + (features * 2)
    )

    return max(min(score, 95), 30)


# -------------------------------
# Cost Estimation
# -------------------------------
def estimate_cost(complexity):
    if complexity == "Low":
        return "Rs.30,000 - Rs.50,000"
    elif complexity == "Medium":
        return "Rs.50,000 - Rs.80,000"
    else:
        return "Rs.1,00,000+"


# -------------------------------
# Helpers
# -------------------------------
def format_list(items):
    if not items:
        return "  - None"
    return "\n".join([f"  - {item}" for item in items])


def generate_reference_links(domain):
    domain_key = domain.split()[0]

    links = {
        "Health": [
            "https://developer.edamam.com/",
            "https://www.hl7.org/fhir/",
        ],
        "FinTech": [
            "https://stripe.com/docs",
            "https://plaid.com/docs/",
        ],
        "EdTech": [
            "https://developers.google.com/classroom",
            "https://moodledev.io/",
        ],
        "AI": [
            "https://platform.openai.com/docs",
            "https://huggingface.co/docs",
        ],
    }

    return links.get(domain_key, ["https://developer.mozilla.org/"])


# -------------------------------
# Plan Formatter
# -------------------------------
def format_plan_text(idea, domain, complexity, result, score, cost):
    references = generate_reference_links(domain)

    return f"""
PROTOTYPE PLAN - PrototypeMate AI
================================

PROBLEM STATEMENT:
This product addresses key challenges in the {domain} domain by
using technology to improve efficiency, accuracy, and user experience.

CLIENT IDEA:
{idea}

DOMAIN:
{domain}

TARGET USERS:
  - End users
  - Administrators
  - Business stakeholders

COMPLEXITY:
{complexity}

REQUIREMENT CLARITY SCORE:
{score}%

ESTIMATED COST:
{cost}

--------------------------------
MVP FEATURES:
{format_list(result.get('mvp_features', []))}

--------------------------------
TECH STACK:
{format_list(result.get('tech_stack', []))}

--------------------------------
TIMELINE:
  {result.get('timeline', 'Not specified')}

--------------------------------
SUCCESS METRICS:
  - Active users
  - Feature adoption rate
  - Retention rate
  - System accuracy

--------------------------------
RISKS:
{format_list(result.get('risks', []))}

--------------------------------
MISSING REQUIREMENTS:
{format_list(result.get('missing_requirements', []))}

--------------------------------
FUTURE ENHANCEMENTS:
  - Advanced AI optimization
  - Monetization strategy
  - Integrations with external tools
  - Analytics & reporting dashboards

--------------------------------
REFERENCE LINKS:
{format_list(references)}

================================
EXECUTIVE SUMMARY:
{result.get('executive_summary', 'Summary not available')}
"""


# -------------------------------
# PDF Generation
# -------------------------------
def generate_pdf(plan_text: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    plan_text = sanitize_text(plan_text)

    for line in plan_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")
