# VULNRUIN - XSS Vulnerability Scanner & Exploiter

## Description
VULNRUIN is an automated tool designed to hunt for Cross-Site Scripting (XSS) vulnerabilities, including reflected, DOM-based, and even advanced injection techniques. It tests a target URL (or a list of URLs) by injecting a wide range of payloads—encoded in various ways—to identify exploitable weaknesses. While its primary goal is to **scan** for vulnerabilities, VULNRUIN also includes payloads that **auto exploit** certain weaknesses (e.g., triggering alerts, redirections, or page defacement) as a demonstration of the vulnerability.

## Features
- **Extensive Payload Library**: Contains over a hundred payloads covering standard XSS, event-based triggers, HTTP Parameter Pollution (HPP), WAF bypass techniques, server-destructive injections, and advanced injection tricks.
- **Multiple Encoding Techniques**: Automatically encodes payloads in hex, Base64, and URL encoding to bypass common input filters.
- **Reflected XSS Testing**: Injects payloads via URL parameters and checks responses for signs of vulnerabilities.
- **DOM-based XSS Testing**: Uses Selenium WebDriver in headless mode to simulate browser execution and detect DOM-based vulnerabilities.
- **Auto Exploitation Simulation**: Some payloads automatically demonstrate exploitation (e.g., triggering alerts, redirection, or defacement) when a vulnerability is found.
- **Website Crawling**: Crawls the target website to discover additional pages and scan them for vulnerabilities.
- **CSV Report Generation**: Saves a detailed scan report including URL, payload used, and vulnerability type.

## Installation
1. **Clone the Repository**:
   ```
   git clone https://github.com/your_username/vulnruin.git
   cd vulnruin```
2. **Install Requirements**:
   ```
   pip install requests beautifulsoup4 selenium colorama
   
   or
   
   pip install -r requirments.txt --break-system-packages```
3. **Execute VulnRuin**:
   ```
   python vulnruin.py```
   

