import time

def safe_agent_invoke(agent, payload, retries=2):
    delay = 1
    for i in range(retries):
        try:
            return agent.invoke(payload)
        except Exception as e:
            print(f"Agent invocation failed on attempt {i + 1}/{retries}: {e}")
            if i == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2