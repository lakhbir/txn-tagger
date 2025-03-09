import pandas as pd
import os
from pathlib import Path
from typing import Union
import logging

logging.basicConfig(level=logging.INFO)

def write_to_file(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    file_format: str = "csv",
    mode: str = "w",
    **kwargs
) -> None:
    """
    Write DataFrame to a file in specified format.
    
    Args:
        df: Input DataFrame.
        output_path: Path to output file.
        file_format: File format (csv, json, parquet, excel, etc.).
        mode: Write mode ('w' for write, 'a' for append).
        **kwargs: Additional arguments for pandas IO methods.
    
    Example:
        write_to_file(df, "transactions.csv", file_format="csv")
    """
    try:
        output_path = Path(output_path)
        output_dir = output_path.parent
        
        # Create directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle different file formats
        if file_format.lower() == "csv":
            df.to_csv(
                output_path, 
                mode=mode, 
                header=not (mode == "a" and output_path.exists()), 
                index=False,
                **kwargs
            )
        elif file_format.lower() == "json":
            df.to_json(output_path, mode=mode, **kwargs)
        elif file_format.lower() == "parquet":
            df.to_parquet(output_path, **kwargs)
        elif file_format.lower() == "excel":
            if mode == "a" and output_path.exists():
                with pd.ExcelWriter(output_path, mode="a", engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name="Sheet1", index=False)
            else:
                df.to_excel(output_path, index=False, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
        
        logging.info(f"Successfully wrote data to {output_path}")
        
    except PermissionError:
        logging.error(f"Permission denied: {output_path}")
    except ImportError as e:
        logging.error(f"Missing dependency: {e}. Install with `pip install {e.name}`")
    except Exception as e:
        logging.error(f"Failed to write data: {str(e)}")