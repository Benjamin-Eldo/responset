import json

def parse_gemma(dataset : str, website_id : str) -> list[str]:
    parsed_responsive_line = []
    with open(dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    responsive = None

    for site in data:
        if site.get("website_id") == website_id:
            responsive = site.get('responsive_explanation')

    print("Before: ", responsive, "\n")
    
    responsive_lines = responsive.split("\n")
    for line in responsive_lines:
        parsed_line = line.strip("! `").rsplit("`", 1)[0].strip()
        print(f"Responsive_line: {parsed_line}")
        parsed_responsive_line.append(parsed_line)

    return parsed_responsive_line

