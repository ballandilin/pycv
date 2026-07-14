import sys
import pymupdf4llm
from groq import Groq
import argparse
import os
from dotenv import load_dotenv
import glob
import shutil

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_PROMPT_USER = {
    "cv": "Réorganise et reformule uniquement le contenu du CV fourni, n'invente aucune expérience, compétence ou chiffre absent de l'original par rapport a la demande de poste suivante {job} et voici mon cv {cv}.",
    "letter": "Genere une lettre de motivation en accord avec le CV et la demande de poste, n'invente aucune expérience, compétence ou chiffre absent du CV que voici {cv}. Voici la demande de poste {job}",
}
GROQ_PROMPT_SYSTEM = {
    "cv": "Repond uniquement avec le document en markdown, sans preambule ni commentaire, en francais",
    "letter": "Repond uniquement avec le document en markdown, sans preambule ni commentaire. Format lettre classique sans aucun titre markdown, 250 a 300 mots maximum, francais irreprochable, ne pas lister les technologies, choisir deux ou trois experiences pertinentes pour l'offre et les developper, ton sobre, interdiction des formules creuses",
}


def extract_cv(file_path: str):
    if file_path.endswith(".pdf"):
        return pymupdf4llm.to_markdown(file_path)
    else:
        return extract_file_txt(file_path)


def extract_file_txt(file_path: str):
    with open(file_path, "r") as f:
        file_extract = f.read()
    return file_extract


def process_job(cv_text: str, job_path: str):
    job = extract_file_txt(job_path)
    cv_adapte = perform_doc_modification(job, "cv", cv_text)
    letter = perform_doc_modification(job, "letter", cv_adapte)
    save_outputs(job_path, cv_adapte, letter)


def process_bulk_job(cv_text: str, job_folder_path: str):
    for f in glob.glob(os.path.join(job_folder_path, "*.txt")):
        process_job(cv_text, f)


def perform_doc_modification(job: str, doc_type: str, cv: str | None = None):
    client = Groq(api_key=GROQ_API_KEY)
    if doc_type == "cv":
        print("Modification de votre cv")
    else:
        print("Modification de votre lettre de motivation")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": GROQ_PROMPT_SYSTEM[doc_type]},
            {
                "role": "user",
                "content": GROQ_PROMPT_USER[doc_type].format(
                    job=job,
                    cv=cv,
                ),
            },
        ],
        temperature=0.35,
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


def save_outputs(job_path: str, cv: str, letter: str):
    job_name = os.path.splitext(os.path.basename(job_path))[0]
    out_dir = os.path.join("results", job_name)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copy(job_path, os.path.join(out_dir, "offre.txt"))
    with open(os.path.join(out_dir, "cv.md"), "w") as f:
        f.write(cv)
    with open(os.path.join(out_dir, "lettre.md"), "w") as f:
        f.write(letter)


def main():
    if not GROQ_API_KEY:
        sys.exit("GROQ_API_KEY manquante")

    parser = argparse.ArgumentParser(
        prog="pycv",
        description="Ask an llm to optimise your cv and cover letter for a specific job",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("path_to_cv")
    group.add_argument("-f", "--file", help="specifie the job resume path")
    group.add_argument("-b", "--bulk", help="Process a bulk generation")

    args = parser.parse_args()

    if args.file and os.path.exists(args.file):
        process_job(extract_cv(args.path_to_cv), args.file)
    elif args.bulk and os.path.isdir(args.bulk):
        process_bulk_job(extract_cv(args.path_to_cv), args.bulk)
    else:
        print("Path does not exist")
        return


if __name__ == "__main__":
    main()
