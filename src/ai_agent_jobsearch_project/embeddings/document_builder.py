

def build_document(row) -> str:
    """
    Creating a document string from first row in Yrkesbarometern. 
 
    """

    parts = [
        f"Yrke: {row['yb_yrke']}",
        f"Yrkesområde: {row['yrkesomrade']}",
        f"Län: {row['lan']}",
        f"SSYK: {row['ssyk']} ({row['ssyk_text']})",
        f"Jobbmöjligheter: {row.get('jobbmojligheter', '')}",
        f"Rekryteringssituation: {row.get('rekryteringssituation', '')}",
        f"Prognos: {row.get('prognos', '')}",
        row.get("text_jobbmojligheter", "") or "",
        row.get("text_rekryteringssituation", "") or "",
    ]
    
    return "\n".join([p for p in parts if str(p).strip()])