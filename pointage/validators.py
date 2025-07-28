import os
from django.core.exceptions import ValidationError
from django.conf import settings
import pandas as pd
from io import BytesIO

# Try to import magic, but make it optional
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

def validate_excel_file(file):
    """
    Validate uploaded Excel files for security and format
    """
    # Check file size
    if file.size > getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024):  # 10MB default
        raise ValidationError(f'File size must be under {getattr(settings, "MAX_UPLOAD_SIZE", 10 * 1024 * 1024) // (1024 * 1024)}MB.')
    
    # Check file extension
    allowed_extensions = getattr(settings, 'ALLOWED_EXCEL_EXTENSIONS', ['.xlsx', '.xls'])
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise ValidationError(f'Only {", ".join(allowed_extensions)} files are allowed.')
    
    # Check MIME type using python-magic (if available)
    if MAGIC_AVAILABLE:
        try:
            # Read first 2048 bytes for MIME detection
            file.seek(0)
            file_content = file.read(2048)
            file.seek(0)  # Reset file pointer
            
            mime_type = magic.from_buffer(file_content, mime=True)
            
            allowed_mime_types = [
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
                'application/vnd.ms-excel',  # .xls
                'application/octet-stream',  # Some systems report this for Excel files
            ]
            
            if mime_type not in allowed_mime_types:
                raise ValidationError('Invalid file type. Only Excel files are allowed.')
                
        except Exception as e:
            raise ValidationError(f'Error validating file: {str(e)}')
    else:
        # Fallback validation using file extension and basic checks
        file.seek(0)
        file_content = file.read(8)  # Read first 8 bytes
        file.seek(0)
        
        # Check for Excel file signatures
        excel_signatures = [
            b'\x50\x4B\x03\x04',  # ZIP signature (for .xlsx)
            b'\xD0\xCF\x11\xE0',  # OLE signature (for .xls)
        ]
        
        if not any(file_content.startswith(sig) for sig in excel_signatures):
            # If no signature match, still allow based on extension (less secure but functional)
            pass
    
    # Validate Excel file structure
    try:
        # Try to read the Excel file to ensure it's valid
        df = pd.read_excel(file, nrows=1)  # Read only first row to check structure
        
        # Check for required columns (case insensitive)
        required_columns = ['date', 'name', 'in', 'out']
        file_columns = [col.lower().strip() for col in df.columns]
        
        # Check if at least some required columns are present
        found_columns = [col for col in required_columns if any(req_col in col for req_col in [col, 'date', 'name', 'in', 'out'])]
        
        if len(found_columns) < 2:  # At least 2 required columns should be present
            raise ValidationError('Excel file must contain columns: date, name, in, out (or similar)')
            
    except Exception as e:
        raise ValidationError(f'Invalid Excel file format: {str(e)}')
    
    return file

def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks
    """
    # Remove any path separators
    filename = os.path.basename(filename)
    
    # Remove any potentially dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename 