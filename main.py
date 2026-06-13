import os
from pypdf import PdfReader

# Load skills
with open("skills.txt", "r", encoding="utf-8") as f:
    required_skills = [line.strip().lower() for line in f if line.strip()]

resume_folder = "resume_folder"
results = []

# Read all PDF resumes
for file in os.listdir("resume_folder"):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(resume_folder, file)

        text = ""

        try:
            reader = PdfReader(pdf_path)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            text = text.lower()
            print("\n-------------------")
            print(file)
            print(text[:2000])
            print("-------------------")

            matched = []
            missing = []

            for skill in required_skills:
                if skill in text:
                    matched.append(skill)
                else:
                    missing.append(skill)

            percentage = round(
                (len(matched) / len(required_skills)) * 100,
                2
            )

            results.append({
                "resume": file,
                "score": percentage,
                "matched": matched,
                "missing": missing
            })

        except Exception as e:
            print(f"Error reading {file}: {e}")

# Sort by score
results.sort(key=lambda x: x["score"], reverse=True)

# Save result in TXT file
with open("result.txt", "w", encoding="utf-8") as report:

    report.write("===== ATS SKILL MATCH REPORT =====\n\n")

    for rank, candidate in enumerate(results, start=1):

        report.write(f"Rank #{rank}\n")
        report.write(f"Resume      : {candidate['resume']}\n")
        report.write(f"Match Score : {candidate['score']}%\n\n")

        report.write("Matched Skills:\n")
        report.write(
            ", ".join(candidate["matched"])
            if candidate["matched"] else "None"
        )

        report.write("\n\nMissing Skills:\n")
        report.write(
            ", ".join(candidate["missing"])
            if candidate["missing"] else "None"
        )

        report.write("\n")
        report.write("=" * 50)
        report.write("\n\n")

    if results:
        report.write("BEST CANDIDATE\n")
        report.write(f"Resume : {results[0]['resume']}\n")
        report.write(f"Score  : {results[0]['score']}%\n")

print("Result saved in result.txt")