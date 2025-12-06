from typing import Any, Callable, Dict, Type, Optional

PREPROCESSOR_REGISTRY: Dict[str, Any] = {}
"""
A registry to map preprocessor names to their corresponding classes or instances.
Key: str - The name of the preprocessor.
Value: Any - The preprocessor class or instance.
"""

def register_preprocessor(name: str, preprocessor: Any):
    """
    Registry a new preprocessor class
    Args:
        name (str): The name of the preprocessor to register.
        preprocessor (Any): The preprocessor object to register.
    """
    PREPROCESSOR_REGISTRY[name] = preprocessor

def preprocessor_decorator(name: str) -> Callable[[Type], Type]:
    """
    Decorator to register a new preprocessor.
    Args:
        name (str): The name of the preprocessor to register.
    Returns:
        Callable[[Type], Type]: The decorator function.
    """
    def decorator(cls: Type) -> Type:
        register_preprocessor(name, cls)
        return cls
    return decorator


def get_preprocessor(name: str, **kwargs: Any) -> Any:
    """
    factory method to fetch the registered preprocessor by name.
    Args:
        name (str): The name of the preprocessor to retrieve.
        **kwargs: Additional keyword arguments to pass to the preprocessor constructor.
    Returns:
        Any: The registered preprocessor object.
    """
    if name not in PREPROCESSOR_REGISTRY:
        raise ValueError(f"preprocessor '{name}' is not registered")
    obj = PREPROCESSOR_REGISTRY[name]
    
    # detect obj is a class or an instance
    if isinstance(obj, type):
        # if it's a class, instantiate it with kwargs
        return obj(**kwargs)
    else:
        # if it's an instance, return it directly
        return obj
    


