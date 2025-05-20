import os
from dotenv import load_dotenv
import google.generativeai as genai
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)  # auto reset colors after each print

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(Fore.RED + "❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Convert natural language to Windows shell command with enhanced prompt
def get_command(natural_language):
    prompt = f"""
You are a helpful assistant that converts natural language into Windows command line instructions.

Task: Convert the following sentence into a valid Windows command.
Do not provide explanations or commentary.
Only return a single-line command, without quotes, markdown, or formatting.

Natural Language: {natural_language}
"""
    response = model.generate_content(prompt)
    return response.text.strip("` \n")

# Main loop
def main():
    print(Fore.CYAN + "🔮 AI Shell – Powered by Gemini (Windows)\n")
    while True:
        nl_input = input(Fore.YELLOW + "Enter command (or type 'exit'): " + Style.RESET_ALL)
        if nl_input.strip().lower() == 'exit':
            print(Fore.MAGENTA + "👋 Exiting AI Shell.")
            break
        try:
            bash_cmd = get_command(nl_input)
            print(Fore.GREEN + f"\n🧠 Interpreted command:\n{bash_cmd}\n")
            
            confirm = input(Fore.YELLOW + "⚠️ Run this command? (y/n): " + Style.RESET_ALL).strip().lower()
            if confirm != 'y':
                print(Fore.MAGENTA + "❎ Skipped.\n")
                continue

            result = subprocess.run(bash_cmd, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() or result.stderr.strip()
            print(Fore.WHITE + f"📄 Output:\n{output}\n")
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
