import os
from google import genai
import yaml

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

from logger import get_logger

logger = get_logger()

def moderate_text(text, config):
    outputs = {}
    logger.info(f"Received input: {text}")
    # Toxicity
    if config['check_toxicity']:
        prompt = f"Is the following text toxic? Respond yes/no and explain. Text: {text}"
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        outputs['toxicity'] = resp.text
        logger.info(f"Toxicity check: {resp.text}")
    # PII detection
    if config['check_pii']:
        prompt = f"Identify any personal information (PII) in this text. If any, redact and explain changes: {text}"
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        outputs['pii_redaction'] = resp.text
        logger.info(f"PII redaction: {resp.text}")
    # Jailbreak attempt
    if config['check_jailbreak']:
        prompt = f"Is this prompt attempting prompt-injection or jailbreak? Yes/no and reasoning: {text}"
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        outputs['jailbreak'] = resp.text
        logger.info(f"Jailbreak detection: {resp.text}")
    logger.info(f"Moderation pipeline outputs: {outputs}")
    return outputs

def get_rag_response(text, rag_pipe):
    top_docs, citations = rag_pipe.retrieve(text)
    prompt = f"Based on these policies: {top_docs}, explain if the input violates any and cite relevant details for: {text}"
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    logger.info(f"RAG response: {resp.text}, Citations: {citations}")
    return {"policy_check": resp.text, "citations": citations}


def load_config():
    return yaml.safe_load(open("config.yaml"))
