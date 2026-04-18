"""
Agent Runtime Utilities
Helper functions for agent initialization, execution, and error handling
"""

from typing import Dict, Any, Callable, Optional
import functools
import time
import traceback


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"[Retry] Attempt {attempt + 1} failed: {str(e)}")
                        time.sleep(delay)
                    else:
                        print(f"[Retry] All {max_retries} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely execute a function and return standardized result
    
    Returns:
        Dict with success, data, and error fields
    """
    try:
        result = func(*args, **kwargs)
        return {
            "success": True,
            "data": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def validate_agent_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate agent configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        (is_valid, error_message)
    """
    required_fields = ["GEMINI_API_KEY"]
    
    for field in required_fields:
        if field not in config or not config[field]:
            return False, f"Missing required configuration: {field}"
    
    return True, None


def format_tool_result(tool_name: str, result: Dict[str, Any]) -> str:
    """
    Format tool execution result for logging
    
    Args:
        tool_name: Name of the tool
        result: Tool execution result
        
    Returns:
        Formatted string
    """
    if result.get("success"):
        return f"[Tool: {tool_name}] ✓ Success"
    else:
        return f"[Tool: {tool_name}] ✗ Error: {result.get('error', 'Unknown error')}"


def merge_score_data(*data_dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple score data dictionaries
    
    Args:
        *data_dicts: Variable number of dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    merged = {}
    for d in data_dicts:
        if d:
            merged.update(d)
    return merged


def extract_error_message(error: Exception) -> str:
    """
    Extract a user-friendly error message from an exception
    
    Args:
        error: Exception object
        
    Returns:
        User-friendly error message
    """
    error_str = str(error)
    
    # Common error patterns and their user-friendly versions
    error_mappings = {
        "API key": "Invalid or missing API key. Please check your Gemini API configuration.",
        "rate limit": "API rate limit exceeded. Please try again in a few moments.",
        "timeout": "Request timed out. Please try again.",
        "connection": "Connection error. Please check your internet connection.",
        "not found": "Requested resource not found.",
        "unauthorized": "Authentication failed. Please check your credentials.",
        "forbidden": "Access denied. You don't have permission for this operation.",
    }
    
    for pattern, friendly_msg in error_mappings.items():
        if pattern.lower() in error_str.lower():
            return friendly_msg
    
    return f"An error occurred: {error_str}"


def log_agent_activity(task_type: str, status: str, details: Optional[str] = None):
    """
    Log agent activity for monitoring
    
    Args:
        task_type: Type of task being executed
        status: Status (started, completed, failed)
        details: Optional additional details
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] Agent Task: {task_type} | Status: {status}"
    
    if details:
        log_msg += f" | Details: {details}"
    
    print(log_msg)


def create_agent_context(user_id: Optional[str] = None, admin_id: Optional[str] = None, 
                        session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a context object for agent execution
    
    Args:
        user_id: Optional user ID
        admin_id: Optional admin ID
        session_id: Optional session ID
        
    Returns:
        Context dictionary
    """
    return {
        "user_id": user_id,
        "admin_id": admin_id,
        "session_id": session_id,
        "timestamp": time.time()
    }


def sanitize_tool_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize tool arguments to prevent injection or invalid data
    
    Args:
        args: Tool arguments
        
    Returns:
        Sanitized arguments
    """
    sanitized = {}
    
    for key, value in args.items():
        # Remove None values
        if value is None:
            continue
        
        # Convert to appropriate types
        if isinstance(value, str):
            # Trim whitespace
            sanitized[key] = value.strip()
        elif isinstance(value, (int, float, bool)):
            sanitized[key] = value
        elif isinstance(value, (list, dict)):
            sanitized[key] = value
        else:
            # Convert to string for unknown types
            sanitized[key] = str(value)
    
    return sanitized


class AgentMetrics:
    """Track agent execution metrics"""
    
    def __init__(self):
        self.task_counts = {}
        self.task_durations = {}
        self.tool_calls = {}
        self.errors = []
    
    def record_task_start(self, task_type: str):
        """Record task start"""
        if task_type not in self.task_counts:
            self.task_counts[task_type] = 0
            self.task_durations[task_type] = []
        
        return time.time()
    
    def record_task_end(self, task_type: str, start_time: float, success: bool):
        """Record task completion"""
        duration = time.time() - start_time
        self.task_counts[task_type] += 1
        self.task_durations[task_type].append(duration)
        
        if not success:
            self.errors.append({
                "task": task_type,
                "timestamp": time.time(),
                "duration": duration
            })
    
    def record_tool_call(self, tool_name: str):
        """Record tool usage"""
        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = 0
        self.tool_calls[tool_name] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "total_tasks": sum(self.task_counts.values()),
            "task_counts": self.task_counts,
            "average_durations": {
                task: sum(durations) / len(durations) if durations else 0
                for task, durations in self.task_durations.items()
            },
            "tool_usage": self.tool_calls,
            "error_count": len(self.errors)
        }


# Global metrics instance
_metrics = AgentMetrics()


def get_metrics() -> AgentMetrics:
    """Get global metrics instance"""
    return _metrics
