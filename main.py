import re
from datetime import date
from functions import get_random_generator
# from schedule import weeks

book_sources = "../../queueing_book/book-sources"
EXAM, RESIT = 100, 101  # seeds for question selection
exam_date = date(2025, 1, 21)

if date.today() > exam_date:
    raise ValueError(
        "Replace EXAM seed for RESIT seed to prevent selecting the same questions."
    )

gen = get_random_generator(EXAM)

latex_header = r"""
\documentclass[a4paper,11pt]{article}
\usepackage{../../queueing_book/book-sources/preamble}
\usemintedstyle{bw}

\title{
\Large{Name: \hrulefill ~~Student id: \rule{3cm}{0.4pt}}
~\\
\vspace{1cm}
Exam Queueing Theory and Simulation \\
EBB074A05, 2023-2024.2A\\
Tue, April 2 2024
}

\author{dr. N.D. van Foreest c.s. \\
FEB, University of Groningen
}
\date{}

\begin{document}

\maketitle
"""

readme = r"""
\section*{README}

\begin{itemize}
\item Write your answer on the exam paper below the question. (If you need more room or scrap paper, just us
\item This is a closed book exam.
\item All questions have the same weight.
\item Queueing systems are assumed stable, unless explicitly stated.
\item You cannot ask questions. If you find a problem unclear, just write you comments on the exam, and I'll
\end{itemize}
\clearpage
"""

latex_footer = r"""
% footer

\begin{center}
\begin{Large}
Last page of the exam.
\end{Large}
\end{center}
\begin{center}
\begin{Large}
IS YOUR NAME AND STUDENT ID ON THE EXAM?
\end{Large}
\end{center}

\end{document}
"""

code = r"""
\begin{exercise}
In the next piece of code, underline the line with the error (1 point). Provide the code to repair it (1poi
(The text here is just a place holder. For the exam we'll replace it by a random selection of the code in th
\begin{python}
a = [0, 4, 8, 2, 11]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
a = [0, 4, 8, 2, 1]
\end{python}
\end{exercise}
"""

def extract_theorem(filename):
    theorems = []
    with open(book_sources + "/" + filename, "r") as fp:
        content = fp.read()

    pattern = r"\\begin{theorem}(.*?)\\end{theorem}"
    matches = re.findall(pattern, content, re.DOTALL)
    for text in matches:
        problem = "\\begin{theorem}"
        problem += text
        problem += "\\end{theorem}\n"
        theorems.append(problem)
    return theorems

def select_theorem(gen):
    files = [
        "ratestability.tex",
        "renewal_reward.tex",
        "little.tex",
        "pasta.tex",
        "levelcrossing.tex",
    ]
    theorems = []
    for fname in files:
        theorems += extract_theorem(fname)
    theorem = gen.choice(theorems, size=1)
    text = "\\begin{exercise}"
    text += "Prove this theorem.\n"
    text += theorem[0]
    text += "\\end{exercise}"
    text += "\n\\vfill\n"
    return text

def extract_exercises(filename):
    with open(book_sources + "/" + filename, "r") as fp:
        text = fp.read()

    text = re.sub(r'^%.*', '', text, flags=re.MULTILINE)
    pattern = r"\\begin{exercise}(.*?)\\end{exercise}"
    matches = re.findall(pattern, text, re.DOTALL)
    exercises = []
    for text in matches:
        pattern = r'\\begin{hint}.*?\\end{hint}'
        text = re.sub(pattern, '', text, flags=re.DOTALL)
        pattern = r'\\begin{solution}.*?\\end{solution}'
        text = re.sub(pattern, '', text, flags=re.DOTALL)
        problem = "\n\n\\begin{exercise}"
        problem += text.strip()
        problem += "\n\\end{exercise}"
        exercises.append(problem)
    return exercises

def select_exercises(gen, num_questions):
    files = [fname for week in weeks for fname in week]
    exercises = []
    for fname in files:
        exercises += extract_exercises(fname)
    chosen = gen.choice(exercises, size=num_questions, replace=False)
    text = ""
    for i, ex in enumerate(chosen, 1):
        text += ex
        text += "\n\\vfill\n"
        if i % 3 == 2:
            text += "\n\\clearpage\n"
    return text

text = ""
text += latex_header
text += readme
text += select_theorem(gen)
text += select_exercises(gen, num_questions=8)

text += code + "\n\\vfill\n"
text += code + "\n\\vfill\n\clearpage\n"
text += code + "\n\\vfill\n"

text += latex_footer

exam_name = "exam.tex"
if os.path.exists(exam_name):
    raise FileExistsError(f"{exam_name} already exists.")

with open(exam_name, "w") as fp:
    fp.write(text)
