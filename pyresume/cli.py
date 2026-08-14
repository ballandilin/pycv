import argparse
import glob
import os
import shutil
import sys
from typing import Callable

import pymupdf4llm
from dotenv import load_dotenv
from groq import Groq

from pyresume import config as config_loader

load_dotenv()


class CvGenerator:
    def __init__(
        self,
        api_key: str | None = None,
        prompts: dict | None = None,
        on_status: Callable[[str], None] | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY manquante")
        self.prompts = prompts or config_loader.load_config()
        self.client = Groq(api_key=self.api_key)
        self.on_status = on_status or (lambda msg: None)

    def build_groq_prompt(self, kind: str, cv: str, job: str) -> str:
        return self.prompts[kind]["user"].format(cv=cv, job=job)

    def extract_cv(self, file_path: str) -> str:
        if file_path.endswith(".pdf"):
            return pymupdf4llm.to_markdown(file_path)
        return self.extract_file_txt(file_path)

    @staticmethod
    def extract_file_txt(file_path: str) -> str:
        with open(file_path, "r") as f:
            return f.read()

    def perform_doc_modification(self, job: str, doc_type: str, cv: str) -> str:
        if doc_type == "cv":
            self.on_status("Modification de votre cv")
        else:
            self.on_status("Modification de votre lettre de motivation")
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.prompts[doc_type]["system"]},
                {
                    "role": "user",
                    "content": self.build_groq_prompt(doc_type, cv, job),
                },
            ],
            temperature=self.prompts[doc_type]["temperature"],
            model=self.prompts["model"]["name"],
            max_tokens=self.prompts["model"]["max_tokens"],
        )
        return chat_completion.choices[0].message.content

    def process_job(self, cv_text: str, job_path: str) -> str:
        job = self.extract_file_txt(job_path)
        cv_adapte = self.perform_doc_modification(job, "cv", cv_text)
        letter = self.perform_doc_modification(job, "letter", cv_adapte)
        return self.save_outputs(job_path, cv_adapte, letter)

    def process_bulk_job(self, cv_text: str, job_folder_path: str) -> list[str]:
        return [
            self.process_job(cv_text, f)
            for f in glob.glob(os.path.join(job_folder_path, "*.txt"))
        ]

    @staticmethod
    def save_outputs(job_path: str, cv: str, letter: str) -> str:
        job_name = os.path.splitext(os.path.basename(job_path))[0]
        out_dir = os.path.join("results", job_name)
        os.makedirs(out_dir, exist_ok=True)
        shutil.copy(job_path, os.path.join(out_dir, "offre.txt"))
        with open(os.path.join(out_dir, "cv.md"), "w") as f:
            f.write(cv)
        with open(os.path.join(out_dir, "lettre.md"), "w") as f:
            f.write(letter)
        return out_dir


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        prog="pyresume",
        description="Ask an llm to optimise your cv and cover letter for a specific job",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("path_to_cv")
    group.add_argument("-f", "--file", help="specifie the job resume path")
    group.add_argument("-b", "--bulk", help="Process a bulk generation")

    args = parser.parse_args(argv)

    try:
        generator = CvGenerator(on_status=print)
    except RuntimeError as exc:
        sys.exit(str(exc))

    if args.file and os.path.exists(args.file):
        generator.process_job(generator.extract_cv(args.path_to_cv), args.file)
    elif args.bulk and os.path.isdir(args.bulk):
        generator.process_bulk_job(generator.extract_cv(args.path_to_cv), args.bulk)
    else:
        print("Path does not exist")


if __name__ == "__main__":
    main()
