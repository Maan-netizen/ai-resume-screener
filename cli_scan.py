"""
cli_scan.py
A standalone Python script version — run this directly to test the
matching logic without spinning up the full stack. Good for a quick
recruiter-facing demo or a terminal recording for your portfolio.

Usage:
    python cli_scan.py resume.pdf job_description.txt
"""

import sys
sys.path.append("backend")

from matcher import extract_text, compute_match_score


def main():
    if len(sys.argv) != 3:
        print("Usage: python cli_scan.py <resume_file> <job_description_file>")
        sys.exit(1)

    resume_path, jd_path = sys.argv[1], sys.argv[2]

    with open(resume_path, "rb") as f:
        resume_bytes = f.read()
    resume_text = extract_text(resume_path, resume_bytes)

    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    result = compute_match_score(resume_text, jd_text)

    print(f"\nMatch Score: {result['score']}%")
    print(f"Matched Skills: {', '.join(result['matched_skills']) or 'None'}")
    print(f"Missing Skills: {', '.join(result['missing_skills']) or 'None'}")


if __name__ == "__main__":
    main()
