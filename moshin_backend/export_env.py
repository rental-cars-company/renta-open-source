import os
from datetime import datetime


def export_env_variables(output_file="/moshin_backend/dev.env", include=None, exclude=None):
    """
    :param output_file: Path to the .env file where environment variables will be written.
    :param include: List of variables to include (default: None, includes all).
    :param exclude: List of variables to exclude (default: None).
    """
    # Check if the file already exists
    if os.path.exists(output_file):
        print(f"The file '{output_file}' already exists. No changes were made.")
        return

    try:
        with open(output_file, "w") as f:
            # Add metadata as a comment
            f.write(f"# Environment variables exported on {datetime.now()}\n\n")

            for key, value in os.environ.items():
                if (include and key not in include) or (exclude and key in exclude):
                    continue

                # Escape special characters
                escaped_value = value.replace("\n", "\\n").replace('"', '\\"')
                f.write(f'{key}="{escaped_value}"\n')

        print(f"Environment variables exported to {output_file}")
    except Exception as e:
        print(f"An error occurred while exporting environment variables: {e}")


# Example usage
export_env_variables()
