"""
Constants for the CORE Engineer Training Portal.
"""

# Priority levels with descriptions
PRIORITIES = {
    "P0": "Highest priority problem which normally needs director's approval",
    "P1": "Serious problem that could block progress",
    "P2": "Has the potential to affect progress",
    "P3": "Minor problem or easily worked around (Default for product issues)",
    "P4": "Trivial problem with little or no impact on progress"
}

# Product list
PRODUCTS = [
    "Not Specified",
    "Trend Micro Security for Chrome (Standalone)",
    "TMMS",
    "iTMMS",
    "PWM",
    "Trend Micro Security for Edge (Standalone and co-exist)",
    "Maximum Security",
    "Internet Security",
    "Antivirus+ Security",
    "Antivirus for Mac",
    "HNS",
    "VPN Proxy One Pro",
    "My Account",
    "Security Report",
    "IDP",
    "Antivirus One",
    "Cleaner One Pro",
    "ID Protection",
    "ID Security"
]

# Fundamental Solution options
FUNDAMENTAL_SOLUTIONS = {
    "FS:None": "No fundamental solution",
    "FS:PRD": "Product Requirement/Request",
    "FS:HF": "Hotfix",
    "FS:BE": "Backend Fix",
    "FS:KB": "Knowledge Base Article"
}

# FS Details prompts
FS_DETAILS_PROMPTS = {
    "FS:PRD": {
        "fields": [
            "What was the product requirement/request?",
            "When will it be/was it published?"
        ]
    },
    "FS:HF": {
        "fields": [
            "Published/updated Hotfix KB",
            "Submitted/published date",
            "Will it be included in AU? If so, on what AU?"
        ]
    },
    "FS:BE": {
        "fields": [
            "What was fixed in the backend?"
        ]
    },
    "FS:KB": {
        "fields": [
            "Published/updated KB",
            "Submitted/published date"
        ]
    }
}

# Priority colors for UI
PRIORITY_COLORS = {
    "P0": "#D32F2F",  # Dark Red - Critical
    "P1": "#FF5722",  # Orange Red - High
    "P2": "#FF9800",  # Orange - Medium
    "P3": "#FFC107",  # Amber - Low
    "P4": "#4CAF50"   # Green - Trivial
}
