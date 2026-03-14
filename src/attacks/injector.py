def inject_payload(benign_prompt: str, malicious_payload: str) -> str:
    """
    Combines a benign user task with an adversarial payload.
    This simulates an indirect prompt injection where the LLM is asked to
    summarize, translate, or process text that contains hidden instructions.
    """
    # A realistic indirect injection template:
    # "Please process the following text: <benign_text> \n\n <malicious_payload>"
    
    # In this benchmark, we just append it straightforwardly, which is the 
    # simplest and most common evaluation setup for injection testing.
    return f"{benign_prompt}\n\n{malicious_payload}"
