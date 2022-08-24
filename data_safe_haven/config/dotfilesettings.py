"""Load global and local settings from dotfiles"""
# Standard library imports
import pathlib
import re

# Third party imports
import yaml

# Local imports
from data_safe_haven import __version__
from data_safe_haven.exceptions import DataSafeHavenInputException


class DotFileSettings:
    """Load global and local settings from dotfiles with structure like the following

    azure:
      admin_group_id: 347c68cb-261f-4a3e-ac3e-6af860b5fec9
      location: uksouth
      subscription_name: Data Safe Haven Development
    shm:
      name: Turing Development
    """

    admin_group_id: str = None
    location: str = None
    name: str = None
    subscription_name: str = None
    config_file_name = ".dshconfig"

    def __init__(
        self, admin_group_id: str = None, location: str = None, name: str = None, subscription_name: str = None
    ):
        try:
            # Load local dotfile settings (if any)
            local_dotfile = pathlib.Path.cwd() / self.config_file_name
            if local_dotfile.exists():
                with open(pathlib.Path(local_dotfile), "r") as f_yaml:
                    settings = yaml.safe_load(f_yaml)
                    self.admin_group_id = settings.get("azure", {}).get(
                        "admin_group_id", self.admin_group_id
                    )
                    self.location = settings.get("azure", {}).get(
                        "location", self.location
                    )
                    self.name = settings.get("shm", {}).get("name", self.name)
                    self.subscription_name = settings.get("azure", {}).get(
                        "subscription_name", self.subscription_name
                    )
        except Exception as exc:
            raise DataSafeHavenInputException(
                f"Could not load settings from YAML file '{local_dotfile}'"
            ) from exc

        # Override with command-line settings (if any)
        if admin_group_id:
            self.admin_group_id = admin_group_id
        if location:
            self.location = location
        if name:
            self.name = name
        if subscription_name:
            self.subscription_name = subscription_name

        # Check that all variables exist
        if not all(
            [self.admin_group_id, self.location, self.name, self.subscription_name]
        ):
            raise DataSafeHavenInputException(
                f"Not enough information to initialise Data Safe Haven. Please provide subscription_name and location in one of the following ways\n"
                + "- in the current directory .dshconfig\n"
                + "- via command line arguments"
            )

    def write(self, directory: pathlib.Path) -> None:
        settings = {
            "shm": {
                "name": self.name,
            },
            "azure": {
                "admin_group_id": self.admin_group_id,
                "location": self.location,
                "subscription_name": self.subscription_name,
            }
        }
        filepath = (directory / self.config_file_name).resolve()
        with open(filepath, "w") as f_settings:
            yaml.dump(settings, f_settings, indent=2)
        return filepath
