import argparse
import sys
import os
from .orchestrator import StorytellerOrchestrator

def main():
    parser = argparse.ArgumentParser(
        description="Agentic Data Storyteller: Autonomous Multi-Agent BI & Executive Story Engine"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="data/sample_ecommerce_sales.csv",
        help="Path to input CSV dataset"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="artifacts",
        help="Directory to save generated dashboards, reports, and infographics"
    )
    parser.add_argument(
        "--repo-url",
        type=str,
        default="https://github.com/NiteshBen/agentic-data-storyteller",
        help="GitHub repository URL for attribution and links"
    )

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"Error: Dataset file not found at '{args.csv}'.")
        sys.exit(1)

    print("==================================================")
    print("   AGENTIC DATA STORYTELLER | MULTI-AGENT RUN     ")
    print("==================================================")
    print(f"[*] Input Data: {args.csv}")
    print(f"[*] Output Directory: {args.output_dir}")
    print("[*] Launching autonomous agents...")

    orchestrator = StorytellerOrchestrator(output_dir=args.output_dir)
    result = orchestrator.run_pipeline(args.csv, repo_url=args.repo_url)

    print("\n[+] Multi-Agent Pipeline Completed Successfully!")
    print(f"[+] Records Profiled: {result.key_metrics['records']:,}")
    print(f"[+] Dimensions Analyzed: {result.key_metrics['columns']}")
    print(f"[+] Interactive Dashboard: {result.html_dashboard_path}")
    print(f"[+] Infographic Vector Card: {result.infographic_svg_path}")
    print(f"[+] Executive Markdown Story: {os.path.join(args.output_dir, 'EXECUTIVE_STORY.md')}")
    print(f"[+] LinkedIn Announcement: {os.path.join(args.output_dir, 'LINKEDIN_POST.md')}")
    print("==================================================")

if __name__ == "__main__":
    main()
