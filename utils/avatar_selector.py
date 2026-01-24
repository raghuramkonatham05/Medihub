def select_avatar(age, gender):
    try:
        age = int(age)
    except (TypeError, ValueError):
        age = None

    gender = (gender or "").lower()

    if age is None:
        return "default.jpg"

    if age < 30:
        return "male_20.jpg" if gender == "male" else "female_20.jpg"
    elif age < 50:
        return "male_35.jpg" if gender == "male" else "female_35.jpg"
    else:
        return "male_60.jpg" if gender == "male" else "female_60.jpg"
