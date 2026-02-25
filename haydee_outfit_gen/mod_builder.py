import os
import shutil
import logging
from pathlib import Path
from .config import settings

logger = logging.getLogger(__name__)

class ModBuilder:
    """Handles the creation of directories and mod configuration files."""

    def __init__(self, mod_name: str):
        if mod_name.strip().lower() == "haydee":
            raise ValueError("Mod name cannot be 'Haydee'. This protects the system outfit.")
        
        self.mod_name = mod_name.strip()
        self.mod_dir = settings.outfits_dir / self.mod_name

    def prepare_directory(self) -> None:
        """Creates the mod directory, overwriting if it already exists."""
        if self.mod_dir.exists():
            logger.warning(f"Mod directory '{self.mod_name}' already exists. Overwriting...")
            shutil.rmtree(self.mod_dir)
        
        self.mod_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {self.mod_dir}")

    def generate_mtl_file(self) -> None:
        """Generates the .mtl material mapping file."""
        mtl_content = f"""HD_DATA_TXT 300
material
{{
	type OPAQUE;
	twoSided false;
	width 64.0;
	height 64.0;
	normalMap "Outfits\\Haydee\\Suit_N.dds";
	diffuseMap "Outfits\\{self.mod_name}\\Suit_D.dds";
	specularMap "Outfits\\Haydee\\Suit_S.dds";
	speculars 1.0 2.0 0.0;
	surface Default;
}}
"""
        mtl_path = self.mod_dir / "Suit.mtl"
        mtl_path.write_text(mtl_content, encoding="utf-8")
        logger.info(f"Generated {mtl_path.name}")

    def generate_outfit_file(self) -> None:
        """Generates the .outfit configuration file."""
        outfit_content = f"""HD_DATA_TXT 300

outfit
{{
	name			"{self.mod_name}";
	default			false;

	mesh
	{{
		mesh		"Outfits\\Haydee\\Suit.mesh";
		skin		"Outfits\\Haydee\\Suit.skin";
		material	"Outfits\\{self.mod_name}\\Suit.mtl";

		common		true;
		mask		true;
		visor		true;
		jacket		true;
	}}

	mesh
	{{
		mesh		"Outfits\\Haydee\\Helmet.mesh";
		skin		"Outfits\\Haydee\\Helmet.skin";
		material	"Outfits\\{self.mod_name}\\Suit.mtl";

		common		true;
		mask		true;
		visor		true;
		jacket		true;
		
		slot		"Head" "Haydee";
	}}
	
	mesh
	{{
		mesh		"Outfits\\Haydee\\Hands.mesh";
		skin		"Outfits\\Haydee\\Hands.skin";
		material	"Outfits\\{self.mod_name}\\Suit.mtl";

		common		true;
		mask		true;
		visor		true;
		jacket		true;

		slot		"Hands" "Haydee";
	}}

	mesh
	{{
		mesh		"Outfits\\Haydee\\Clock.mesh";
		skin		"Outfits\\Haydee\\Clock.skin";

		clock		true;

		common		true;
		mask		true;
		visor		true;
		jacket		true;
	}}

	mesh
	{{
		mesh		"Outfits\\Haydee\\MaskRobo.mesh";
		skin		"Outfits\\Haydee\\MaskRobo.skin";
		material	"Outfits\\Haydee\\MaskRobo.mtl";

		mask		true;
	}}

	mesh
	{{
		mesh		"Outfits\\Haydee\\Visor.mesh";
		skin		"Outfits\\Haydee\\Visor.skin";
		material	"Items\\Visor\\Visor.mtl";

		visor		true;
	}}
	
	mesh
	{{
		mesh		"Outfits\\Haydee\\Vest.mesh";
		skin		"Outfits\\Haydee\\Vest.skin";
		material	"Outfits\\Haydee\\Vest.mtl";

		common		false;
		mask		false;
		visor		false;
		jacket		true;
	}}

	ragdoll
	{{
		common		true;
		mask		true;
		visor		true;
		jacket		true;

		ragdoll		"Outfits\\Haydee\\Haydee.doll";
	}}
}}
"""
        outfit_path = settings.outfits_dir / f"{self.mod_name}.outfit"
        outfit_path.write_text(outfit_content, encoding="utf-8")
        logger.info(f"Generated {outfit_path.name}")
