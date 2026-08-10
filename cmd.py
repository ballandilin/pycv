import sys
import pymupdf4llm
from groq import Groq
import argparse
import os
from dotenv import load_dotenv
import glob
import shutil
import config as config_loader

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROMPTS = config_loader.load_config()

GROQ_PROMPT_SYSTEM = PROMPTS["cv"]["system"]
GROQ_PROMPT_USER = PROMPTS["cv"]["user"]
GROQ_PROMPT_SYSTEM_LETTER = PROMPTS["letter"]["system"]
GROQ_PROMPT_USER_LETTER = PROMPTS["letter"]["user"]


def build_groq_prompt(kind: str, cv: str, job: str) -> str:
    if kind == "cv":
        return GROQ_PROMPT_USER.format(cv=cv, job=job)
    else:
        return GROQ_PROMPT_USER_LETTER.format(cv=cv, job=job)


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
            {"role": "system", "content": PROMPTS[doc_type]["system"]},
            {
                "role": "user",
                "content": build_groq_prompt(doc_type, cv, job),
            },
        ],
        temperature=PROMPTS[doc_type]["temperature"],
        model=PROMPTS["model"]["name"],
        max_tokens=PROMPTS["model"]["max_tokens"],
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
