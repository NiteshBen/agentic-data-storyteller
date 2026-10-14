import os
import sys
import webbrowser
import urllib.parse

def main():
    post_file = os.path.join("artifacts", "LINKEDIN_POST.md")
    if not os.path.exists(post_file):
        post_file = "LINKEDIN_POST.md"

    if not os.path.exists(post_file):
        print("[-] Error: LINKEDIN_POST.md not found. Run the pipeline first:")
        print("    python -m agentic_data_storyteller.cli")
        sys.exit(1)

    with open(post_file, "r", encoding="utf-8") as f:
        content = f.read()

    print("================================================================")
    print("                LINKEDIN POST READY FOR SHARING                 ")
    print("================================================================\n")
    print(content)
    print("\n================================================================")
    print("[*] Infographic image available at: artifacts/executive_infographic.svg")
    print("[*] GitHub Repository: https://github.com/NiteshBen/agentic-data-storyteller")
    print("================================================================")
    
    # Generate direct LinkedIn share link
    repo_url = "https://github.com/NiteshBen/agentic-data-storyteller"
    share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(repo_url)}"
    
    print("\n[+] To share immediately on LinkedIn, open this link:")
    print(f"    {share_url}\n")
    
    # Try opening the share link in the default web browser
    try:
        if "--open" in sys.argv:
            print("[*] Opening LinkedIn sharing in your browser...")
            webbrowser.open(share_url)
    except Exception as e:
        print(f"[-] Could not open browser: {e}")

if __name__ == "__main__":
    main()
