def field_match(field_name: str, answers: dict):
    if not field_name:
        return None

    field_name = field_name.lower()

    mapping = {
        "name": ["name", "fullname", "applicant"],
        "email": ["email", "mail"],
        "phone": ["phone", "mobile"],
        "linkedin": ["linkedin"],
        "github": ["github"],
        "resume": ["resume", "cv"],
    }

    for key in answers:
        for pat in mapping.get(key, []):
            if pat in field_name:
                return key

    return None
