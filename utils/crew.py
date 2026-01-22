#!/usr/bin/env python3
"""
crew.py

Principal‐developer–level, architected implementation of the ATS Resume‐Tailoring workflow.
Defines configuration, tools, agents, tasks, crew assembly, and execution in one file.
"""

import warnings
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, ScrapeWebsiteTool, MDXSearchTool, SerperDevTool


# ─── Configuration & Environment ───────────────────────────────────────────────

warnings.filterwarnings("ignore")

# Load .env from project root (fails silently if not found)
load_dotenv()

# Set up structured logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Tool Factory ─────────────────────────────────────────────────────────────
# Tools are now created inline in create_job_application_crew for better path handling

# ─── Agent Factory ────────────────────────────────────────────────────────────

def create_agents(tools):
    """
    Build and return the list of Agents driving the workflow.
    Tools dict may contain: 'search', 'scrape', 'read_resume', 'semantic_search'
    """
    # Get available tools (some may be optional)
    search_tool = tools.get("search")
    scrape_tool = tools.get("scrape")
    read_resume_tool = tools.get("read_resume")
    semantic_search_tool = tools.get("semantic_search")

    # Build tool lists for each agent (only include tools that exist)
    researcher_tools = []
    if scrape_tool:
        researcher_tools.append(scrape_tool)
    if search_tool:
        researcher_tools.append(search_tool)

    profiler_tools = []
    if scrape_tool:
        profiler_tools.append(scrape_tool)
    if search_tool:
        profiler_tools.append(search_tool)
    if read_resume_tool:
        profiler_tools.append(read_resume_tool)
    if semantic_search_tool:
        profiler_tools.append(semantic_search_tool)

    strategist_tools = []
    if scrape_tool:
        strategist_tools.append(scrape_tool)
    if search_tool:
        strategist_tools.append(search_tool)
    if read_resume_tool:
        strategist_tools.append(read_resume_tool)
    if semantic_search_tool:
        strategist_tools.append(semantic_search_tool)

    interviewer_tools = []
    if scrape_tool:
        interviewer_tools.append(scrape_tool)
    if search_tool:
        interviewer_tools.append(search_tool)
    if read_resume_tool:
        interviewer_tools.append(read_resume_tool)
    if semantic_search_tool:
        interviewer_tools.append(semantic_search_tool)

    researcher = Agent(
        role="Tech Job Researcher",
        goal="Analyze job postings deeply to identify required skills & qualifications.",
        tools=researcher_tools,
        verbose=True,
        backstory=(
            "Extract critical information from job postings to form the foundation "
            "for tailored resume content."
        )
    )

    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Compile detailed personal and professional profiles from diverse sources.",
        tools=profiler_tools,
        verbose=True,
        backstory=(
            "Analyze personal projects, publications, and professional history to "
            "create comprehensive profiles for resume tailoring."
        )
    )

    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Optimize resumes so they align tightly with job requirements.",
        tools=strategist_tools,
        verbose=True,
        backstory=(
            "Expert at tailoring resumes to highlight the most relevant experience "
            "and skills for specific job postings."
        )
    )

    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Generate focused interview questions & talking points.",
        tools=interviewer_tools,
        verbose=True,
        backstory=(
            "Prepare candidates for interviews by creating tailored questions and "
            "talking points based on job requirements and their background."
        )
    )

    return [researcher, profiler, resume_strategist, interview_preparer]# ─── Task Factory ─────────────────────────────────────────────────────────────

def create_tasks(agents):
    """
    Create and return Task objects linked to each Agent.
    """
    researcher, profiler, strategist, interviewer = agents

    research_task = Task(
        name="Extract Job Requirements",
        description=(
            "Analyze the job posting URL ({job_posting_url}) to extract key "
            "skills, experiences, and qualifications required."
        ),
        expected_output="Structured list of required skills, qualifications, and experiences.",
        agent=researcher,
        async_execution=True
    )

    profile_task = Task(
        name="Compile Applicant Profile",
        description=(
            "Compile a profile using:\n"
            "  • GitHub:        ({github_url})\n"
            "  • LinkedIn:      ({linkedin_url})\n"
            "  • Google Scholar:({scholar_url})\n"
            "  • Portfolio:     ({portfolio_url})\n"
            "  • Personal write-up: ({personal_writeup})\n"
            "Extract and synthesize information from all sources."
        ),
        expected_output=(
            "Comprehensive profile including skills, projects, publications, and highlights."
        ),
        agent=profiler,
        async_execution=True
    )

    resume_strategy_task = Task(
        name="Tailor Resume",
        description=(
            "Using outputs from previous tasks, tailor the resume to highlight the most relevant "
            "experience and skills. Do not invent information."
        ),
        expected_output="Markdown resume perfectly aligned with the job posting.",
        output_file="tailored_resume.md",
        context=[research_task, profile_task],
        agent=strategist
    )

    interview_task = Task(
        name="Prepare Interview Materials",
        description=(
            "Generate interview questions and talking points based on the tailored resume "
            "and job requirements to prepare the candidate."
        ),
        expected_output="Markdown with key questions and talking points.",
        output_file="interview_materials.md",
        context=[research_task, profile_task, resume_strategy_task],
        agent=interviewer
    )

    return [research_task, profile_task, resume_strategy_task, interview_task]

# ─── Crew Factory ─────────────────────────────────────────────────────────────

def create_job_application_crew(resume_path=None, mdx_path=None):
    """
    Factory function to create and return the job application crew.
    If resume_path or mdx_path are not provided, they default to None and
    tools requiring them will be disabled.
    """
    # Only create tools that have valid paths
    tools_dict = {
        "scrape": ScrapeWebsiteTool(),
    }

    # Add search tool only if API key is available
    serper_key = os.environ.get("SERPER_API_KEY")
    if serper_key:
        tools_dict["search"] = SerperDevTool(api_key=serper_key)
    else:
        logger.warning("SERPER_API_KEY not found. Search functionality will be limited.")

    # Add file-based tools if paths are provided and exist
    if resume_path and os.path.exists(resume_path):
        tools_dict["read_resume"] = FileReadTool(file_path=resume_path)
    else:
        logger.warning(f"Resume path not provided or doesn't exist: {resume_path}")

    if mdx_path and os.path.exists(mdx_path):
        tools_dict["semantic_search"] = MDXSearchTool(mdx=mdx_path)
    else:
        logger.warning(f"MDX path not provided or doesn't exist: {mdx_path}")

    agents = create_agents(tools_dict)
    tasks  = create_tasks(agents)

    return Crew(agents=agents, tasks=tasks, verbose=True)

# Lazy initialization: job_application_crew will be created only when accessed
class LazyJobApplicationCrew:
    """Lazy wrapper to delay crew creation until first use."""
    _crew = None

    def kickoff(self, inputs):
        """Create crew on first kickoff call."""
        if self._crew is None:
            # Set default paths relative to project root
            project_root = Path(__file__).resolve().parent.parent
            resume_path = project_root / "data" / "Nikhil_Nageshwar_Inturi.pdf"
            mdx_path = project_root / "data" / "Nikhil_Nageshwar_Inturi.pdf"

            # Convert to string, but allow non-existent paths
            self._crew = create_job_application_crew(
                resume_path=str(resume_path) if resume_path.exists() else None,
                mdx_path=str(mdx_path) if mdx_path.exists() else None
            )
        return self._crew.kickoff(inputs=inputs)

job_application_crew = LazyJobApplicationCrew()

# ─── Main Workflow ────────────────────────────────────────────────────────────

def main():
    """
    Alternative entry point using direct crew creation.
    """
    # Define inputs (extendable with any URLs or writeups)
    inputs = {
        "job_posting_url": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4215170359",
        "github_url":      "https://github.com/unikill066",
        "linkedin_url":    "https://www.linkedin.com/in/nikhilinturi/",
        "scholar_url":     "https://scholar.google.com/citations?user=9mU1K0cAAAAJ&hl=en",
        "portfolio_url":   "https://inturinikhilnageshwar.netlify.app/",
        "personal_writeup": (
            "I build AI that helps scientists decode pain. With 7 + years at the intersection of Generative AI, "
            "Machine Learning, and Bioinformatics, I’ve shipped everything from RAG-powered chatbots that surface lab "
            "insights on demand to high-throughput pipelines that segment millions of neurons 95 % effectively and 15 % "
            "more accurately than before. Today: Senior Data Scientist at the Center for Advanced Pain Studies (UT Dallas) "
            "and M.S. candidate in Business Analytics & AI, leading three cross-functional teams (image segmentation, "
            "sequencing analytics, bioinformatics). Recent wins include:\n"
            "• Unified data-to-knowledge chat system that ingests spatial & single-cell omics, publications, and lab notebooks via "
            "custom RAG pipelines—cutting search time from hours to minutes.\n"
            "• Neuron-detection suite (Detectron2 | YOLOv11 | SAM) that improved labeling precision by 15 % and scaled inference 10× on Kubernetes.\n"
            "• Predictive models of rat jaw kinematics, supporting pre-clinical pain-modulation studies.\n"
            "Previously: At Infosys and Aganitha, I automated AAV capsid engineering, built 7-mer clustering models, and optimized enterprise "
            "ML workflows that now analyze > 5 TB of genomic data weekly.\n"
            "Tech stack: Python, PyTorch, FastAI, Hugging Face, Nextflow, Docker/K8s, SQL, R, Tableau. Methodologies: RAG & Agentic AI "
            "architectures, CV segmentation, single-cell & spatial-omics analysis, MLOps, container orchestration.\n"
            "When I’m not coding, I’m a Technical Officer for Code.exe @ UTD—hosting hands-on workshops in Python, SQL, and Docker for 500+ "
            "students each semester.\n"
            "Let’s connect if you’re exploring AI for neuroscience, multi-omic analytics, or just want to geek out over Generative AI’s next leap.\n"
            "GitHub: https://github.com/unikill066"
        )
    }

    logger.info("Starting ATS Resume Tailoring workflow...")
    result = job_application_crew.kickoff(inputs=inputs)
    logger.info("Workflow complete. Generated outputs: %s", list(result.keys()))

    return result

if __name__ == "__main__":
    main()
