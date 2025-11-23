from cmas.validation_agent.src.execute import ExecutionResult

def compare_results(aws_result: ExecutionResult, gcp_result: ExecutionResult) -> bool:
    """
    Compares the execution results of AWS and GCP tests.
    Returns True if they are equivalent, False otherwise.
    """
    print("Comparing results...")
    
    # 1. Functional Match (Status Code)
    if aws_result.status_code != gcp_result.status_code:
        print(f"FAILURE: Status code mismatch. AWS: {aws_result.status_code}, GCP: {gcp_result.status_code}")
        return False
    
    # 2. Functional Match (Output)
    # In a real scenario, we might need fuzzy matching for timestamps/IDs
    if aws_result.output.strip() != gcp_result.output.strip():
        print(f"FAILURE: Output mismatch.\nAWS:\n{aws_result.output}\nGCP:\n{gcp_result.output}")
        return False
        
    # 3. Latency Check
    # P95 is hard with single run, so we just check if GCP is not > 15% slower than AWS
    # Allow some buffer for very fast tests where variance is high
    if aws_result.latency_ms > 100: 
        threshold = aws_result.latency_ms * 1.15
        if gcp_result.latency_ms > threshold:
            print(f"FAILURE: Latency regression. AWS: {aws_result.latency_ms}ms, GCP: {gcp_result.latency_ms}ms")
            return False

    print("SUCCESS: Validation passed. Workloads are equivalent.")
    return True
