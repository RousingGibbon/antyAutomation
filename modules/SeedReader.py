from typing import List
import aiofiles
from loguru import logger
class SeedReader:
    @staticmethod
    async def read_seed_phrases(file_path: str) -> List[str]:
        """
        Reads seed phrases from a file.

        Args:
            file_path (str): The path to the file containing seed phrases.

        Returns:
            List[str]: List of seed phrases.
        """
        async with aiofiles.open(file_path, 'r') as file:
            logger.info(f"Reading seeds.txt ...")
            lines = await file.readlines()
        return [phrase.strip() for phrase in lines]