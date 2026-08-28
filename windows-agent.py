from strands import Agent, tool
from strands.models.ollama import OllamaModel
import subprocess


# ============================================================
# WINDOWS POWERSHELL TOOL
# ============================================================

@tool
def powershell(command: str) -> str:
    """
    Execute a safe, read-only Windows PowerShell command.

    Args:
        command: A Windows PowerShell command for system inspection.
    """

    # Commands that can modify or damage the system
    blocked_commands = [
        "remove-item",
        "del ",
        "erase ",
        "format-volume",
        "clear-disk",
        "stop-computer",
        "restart-computer",
        "shutdown",
        "restart",
        "reboot",
        "diskpart",
        "set-itemproperty",
        "remove-itemproperty",
        "stop-process",
        "stop-service",
        "set-service",
        "start-service",
        "new-item",
        "move-item",
        "copy-item",
        "rename-item",
        "invoke-webrequest",
        "start-process",
    ]

    command_lower = command.lower()

    for blocked in blocked_commands:
        if blocked in command_lower:
            return (
                "BLOCKED: This command can modify system resources. "
                "For safety, only read-only commands are allowed."
            )

    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if output:
            return output

        if error:
            return f"PowerShell error:\n{error}"

        return "Command completed successfully with no output."

    except subprocess.TimeoutExpired:
        return "The PowerShell command timed out."

    except Exception as e:
        return f"Error executing PowerShell command: {e}"


# ============================================================
# OLLAMA MODEL
# ============================================================

model = OllamaModel(
    host="http://127.0.0.1:11434",
    model_id="minimax-m3:cloud"
)


# ============================================================
# WINDOWS SYSTEM ADMINISTRATOR AGENT
# ============================================================

agent = Agent(
    model=model,
    tools=[powershell],

    system_prompt="""
You are a smart Windows System Administrator AI.

You help users understand and troubleshoot their Windows computer.

You have access to a safe PowerShell tool called `powershell`.

Use the tool whenever real information from the Windows system
is required.

You can help with:

1. System information
2. Windows version
3. Computer name
4. CPU usage
5. Memory/RAM usage
6. Disk usage
7. Running processes
8. Network information
9. Open ports
10. Windows services
11. System event logs
12. Files and directories
13. System uptime

Useful Windows PowerShell commands include:

SYSTEM:
systeminfo
hostname
Get-CimInstance Win32_OperatingSystem

CPU:
Get-CimInstance Win32_Processor
Get-Counter '\\Processor(_Total)\\% Processor Time'

MEMORY:
Get-CimInstance Win32_OperatingSystem |
Select-Object TotalVisibleMemorySize,FreePhysicalMemory

DISK:
Get-PSDrive -PSProvider FileSystem
Get-Volume

PROCESSES:
Get-Process
Get-Process | Sort-Object CPU -Descending |
Select-Object -First 10

NETWORK:
Get-NetIPConfiguration
Get-NetIPAddress
Get-NetRoute

OPEN PORTS:
Get-NetTCPConnection
Get-NetTCPConnection -State Listen

SERVICES:
Get-Service
Get-Service | Where-Object {$_.Status -eq 'Running'}

EVENT LOGS:
Get-WinEvent -LogName System -MaxEvents 30

FILES:
Get-ChildItem
Get-ChildItem -Force
Get-Location

UPTIME:
Get-CimInstance Win32_OperatingSystem |
Select-Object LastBootUpTime

When troubleshooting, investigate step-by-step using multiple
read-only commands when necessary.

Explain the results in simple language.

IMPORTANT SAFETY RULES:

Only use read-only commands for system diagnosis.

Never execute commands that delete files, format disks,
shut down/restart Windows, stop processes/services, or modify
system settings.

IMPORTANT:
Do not executedestructive commands such as:
rm -rf
mkfs
shutdown
reboot
dd

Always ask the user for confirmation before executing commands that modify or stop system resources.

If the user asks for a potentially destructive operation,
do not execute it.

Never bypass Windows security protections.

Be friendly, concise, and helpful.
"""
)


# ============================================================
# CHAT LOOP
# ============================================================

print("=" * 60)
print("        WINDOWS SYSTEM ADMINISTRATOR AI")
print("=" * 60)
print("Ask me about your Windows computer.")
print("Type 'exit', 'quit' or 'bye' to stop.")
print("=" * 60)


while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nAgent: Goodbye! 👋")
        break

    if not user_input:
        continue

    try:
        agent(user_input)

    except Exception as e:
        print(f"\nAgent error: {e}")