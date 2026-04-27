import pdfplumber
import re

pdf_path = r".\KlimaatRapport-2020 (1).pdf"

print("=" * 80)
print("KMI KLIMAATRAPPORT 2020 - EXTREME NEERSLAG ANALYSE")
print("=" * 80)

with pdfplumber.open(pdf_path) as pdf:
    print(f"\nTotaal pagina's: {len(pdf.pages)}\n")
    
    # Volledige tekst extraheren
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    # Keywords zoeken
    keywords = ["extreme", "neerslag", "trend", "GEV", "return periode", "autocorrelatie", 
                "statistisch", "methode", "10 dag", "zware neerslag", "intensiteit",
                "Mann-Kendall", "lineaire trend", "percentiel", "drempel", "frequentie"]
    
    print("KEYWORD ANALYSE:")
    print("-" * 80)
    for keyword in keywords:
        count = len(re.findall(keyword, full_text, re.IGNORECASE))
        if count > 0:
            print(f"  {keyword:20} : {count:3d} voorkomen")

# Pagina's met relevante inhoud
print("\n" + "=" * 80)
print("RELEVANTE PAGINA'S VOOR EXTREME NEERSLAG:")
print("=" * 80)

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            # Zoek naar relevante termen
            if any(term in text.lower() for term in ["extreme", "zware neerslag", "intensiteit", 
                                                       "trend", "methode", "statistisch", "10 dag"]):
                print(f"\n[PAGINA {i+1}]")
                print("-" * 80)
                print(text[:800])  # Eerste 800 tekens
                print("...")

# Specifiek zoeken naar methodologie secties
print("\n" + "=" * 80)
print("METHODOLOGIE SECTIES:")
print("=" * 80)

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            # Zoek naar methodische beschrijvingen
            if re.search(r"methode|analyse|trend|statistische|onderzoek", text, re.IGNORECASE):
                if "neerslag" in text.lower() or "extreme" in text.lower():
                    print(f"\n[PAGINA {i+1}] - Methodische inhoud:")
                    print(text[:1000])
