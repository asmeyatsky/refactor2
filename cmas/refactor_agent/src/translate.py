import re
from cmas.shared.models import SourceFile, FileType, RefactoringResult
from cmas.framework.plugins import PluginManager

def translate_python(content: str, plugin_manager: PluginManager) -> str:
    """
    Translation using PluginManager.
    """
    translated_content = content
    imports_to_add = set()
    
    mappings = plugin_manager.get_all_python_mappings()

    for aws_snippet, (gcp_snippet, gcp_imports) in mappings.items():
        if aws_snippet in translated_content:
            translated_content = translated_content.replace(aws_snippet, gcp_snippet)
            for imp in gcp_imports:
                imports_to_add.add(imp)
            
    if imports_to_add:
        import_block = "\n".join(imports_to_add) + "\n"
        translated_content = import_block + translated_content

    return translated_content

def translate_terraform(content: str, plugin_manager: PluginManager) -> str:
    """
    Translation using PluginManager.
    """
    translated_content = content
    mappings = plugin_manager.get_all_terraform_mappings()
    
    for aws_resource, gcp_resource in mappings.items():
        if aws_resource in translated_content:
            translated_content = translated_content.replace(aws_resource, gcp_resource)
            translated_content = translated_content.replace(gcp_resource, f"{gcp_resource} # Refactored from {aws_resource}")
            
    return translated_content

def translate_file(source_file: SourceFile, plugin_manager: PluginManager) -> RefactoringResult:
    original_content = source_file.content
    refactored_content = original_content
    changes = []

    if source_file.file_type == FileType.PYTHON:
        refactored_content = translate_python(original_content, plugin_manager)
    elif source_file.file_type == FileType.TERRAFORM:
        refactored_content = translate_terraform(original_content, plugin_manager)
    
    if refactored_content != original_content:
        changes.append("Refactored content using plugins")

    return RefactoringResult(
        original_file=source_file,
        refactored_content=refactored_content,
        changes_made=changes,
        confidence_score=0.8 if changes else 1.0
    )
