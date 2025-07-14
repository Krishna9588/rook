import google.generativeai as genai
import json
# import random
from itertools import cycle
# Gemini API KEYs ----------------------------------------------
API_KEYS = ["AIzaSyAJiD4iD9TcLeFfRwDILNn_TC6B59kcgYE",
            "AIzaSyDWc4srzdUPHMsyPUstpYoS80hEKGaHoxw",
            "AIzaSyBt7Kwemd4STbnid3sQ_eRBbCONJ0ls0rc",
            "AIzaSyC1xocoL8eurJRMwMOu44v-vXg3uwCBs0s"
            ]

# "AIzaSyCqUfR7V9V0Q1wysfRFRuv3ox2N188ZOnM",
# "AIzaSyBpCPUhxoxGauQX33x0nfpcMLFz0uZjUAI",
# ""
# "AIzaSyDkYWbO0kj2oIikqcuYyafT4CKZBKJ2cB8",
# "AIzaSyCfpQp453XtoB9aU4FRNb17Uyn7Lw3HKaU"
# -----------------------------------------------------------


# Old target list
# target = [
#     "use", "using", "used", "adopted", "deployed", "running on",
#     "built with", "powered by", "partner", "integration", "migrated to"
# ]
# New target list
target = [
    # Technology usage
    "use", "using", "used", "adopted", "deployed", "implemented",
    "powered by", "enabled by", "built with", "runs on", "based on",
    "leveraged", "utilized", "developed with", "hosted on", "migrated to",

    # Partnerships and integrations
    "partner", "partnership", "strategic partner", "collaborated with",
    "integrated with", "alliance", "reseller", "technology partner",
    "solution partner", "OEM", "channel partner", "vendor",

    # Hiring indicators
    "hiring", "job posting", "career opportunity", "recruiting",
    "skills required", "experience with", "desired skills", "looking for",
    "join our team", "open roles", "vacancy", "apply", "certified in",

    # Spending and investment
    "investment", "budget", "procurement", "IT spend", "contract with",
    "financial commitment", "spending", "cost", "deal", "payment to", "funding"
]

key_cycler = cycle(API_KEYS)

def explain(chunk_text: str, keyword_tech: str, company_name: str, usage_indicators: list = None) -> dict:
    if usage_indicators is None:
        usage_indicators = target
    # this will kep my code to work with older and new main function together.
    indicators_str = ", ".join([f"'{ind}'" for ind in usage_indicators])
    # print(indicators_str)


    prompt = f"""
    Analyze the following text about {company_name} (company name might not be well structured) to determine if it indicates that {company_name} uses, supports, develops, deploys, partners with, or is actively involved with the technology or concept of '{keyword_tech}'.
    Note: If the technology is mentioned in Job description by that company means they use that technology.
    Note: The company name might not always be explicitly mentioned, could be misspelled, have irregular spacing, or be mixed with unrelated tokens or unknown words. Focus on contextual clues to assess technology usage.
    **Important Guidance:**
    To help you assess company involvement accurately, compare the text against the following key phrases. These are indicators of meaningful involvement with "{keyword_tech}":
    Indications of usage often include words or phrases like: {indicators_str}.
    Do not assume involvement unless there is a clear match or a strong semantic equivalent to one of these phrases.
    However, also consider semantic equivalents and contextual implications beyond just these specific words as exceptions are possible and we can't include each indicator separately.
    
    If the text (chunk) discusses another company (e.g., mentions companies like Wipro, IBM, Infosys, etc.) using or developing the technology, and there is no clear evidence that the company "{company_name}" is directly involved in those activities, then the answer should be **false**.
    Even if "{company_name}" is the host of the content (such as a blog, case study, or article), do **not** assume it is using or endorsing the technology unless explicitly stated.
    Always cross-check if the **actions are attributed directly to {company_name}** and not a third-party company.

    ---
    Text about {company_name}:
    {chunk_text}
    ---

    Provide your answer in a JSON format with two keys:
    1.  "uses_tech": a boolean (true/false) indicating if '{keyword_tech}' is used or involved by the company based on the text and the above guidance.
    2.  "explanation": a brief reason for your answer, quoting relevant parts of the text if possible.
    """

    try:

        # Key Rotation logic
        # current_key = random.choice(API_KEYS)
        # current_key = ""
        current_key = next(key_cycler)
        print(f"--> Using API Key ending in: ...{current_key[-4:]}")
        # Call Gemini API
        genai.configure(api_key=current_key)

        # model = genai.GenerativeModel('gemini-1.5-flash')
        model = genai.GenerativeModel('gemini-2.0-flash-lite-001')

        # response = model.generate_content(prompt)
        response = model.generate_content(
            prompt,
            request_options={"timeout": 300}
        )
        # Clean and parse JSON response
        cleaned_text = response.text.strip().replace("```json\n", "").replace("\n```", "")
        parsed_response = json.loads(cleaned_text)
        return {
            "uses_tech": parsed_response.get("uses_tech", False),
            "explanation": parsed_response.get("explanation", "No explanation from LLM.")
        }
    except Exception as e:
        print(f"Error calling Gemini API or parsing response for keyword '{keyword_tech}': {e}")
        return {"uses_tech": False, "explanation": f"API or parsing error: {e}"}

# Test -------------------
# """
# chunk = "This is just an sample test case"
# keyword = "case"
# company = "test"
# x = explain(chunk,keyword,company)
# print(x)
# """