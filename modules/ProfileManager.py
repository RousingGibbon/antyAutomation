from typing import List, Dict, Any, Optional
import aiohttp
from loguru import logger
import asyncio
class ProfileManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = aiohttp.ClientSession()

    async def get_browser_profiles(self, limit: int = 50, query: Optional[str] = None, tags: Optional[List[str]] = None, statuses: Optional[List[str]] = None, main_websites: Optional[List[str]] = None, users: Optional[List[str]] = None, page: int = 1) -> List[Dict[str, Any]]:
        """
        Retrieves browser profiles from the API.

        Args:
            limit (int): The number of profiles to retrieve. Default is 50.
            query (Optional[str]): Query string for filtering profiles.
            tags (Optional[List[str]]): List of tags for filtering profiles.
            statuses (Optional[List[str]]): List of statuses for filtering profiles.
            main_websites (Optional[List[str]]): List of main websites for filtering profiles.
            users (Optional[List[str]]): List of users for filtering profiles.
            page (int): Page number for pagination. Default is 1.

        Returns:
            List[Dict[str, Any]]: List of browser profiles.
        """
        url = "https://dolphin-anty-api.com/browser_profiles"
        params = {
            'limit': limit,
            'page': page
        }

        if query:
            params['query'] = query
        if tags:
            params['tags'] = tags
        if statuses:
            params['statuses'] = statuses
        if main_websites:
            params['mainWebsites'] = main_websites
        if users:
            params['users'] = users

        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

        async with self.session:
            try:
                async with self.session.get(url, headers=headers, params=params, ssl=False) as response:
                    response_data = await response.json()
                    if response.status == 200:
                        return response_data['data']
                    else:
                        logger.error(f"Failed to fetch profiles: {response_data}")
                        return []
            except aiohttp.ClientConnectorError as e:
                logger.error(f"Connection error: {e}")
                return []

    async def start_profile(self, profile_id: str, retries: int = 10) -> Optional[Dict[str, Any]]:
        """
        Starts a browser profile.

        Args:
            profile_id (str): The ID of the profile to start.
            retries (int): Retries counter.

        Returns:
            Optional[Dict[str, Any]]: Profile data if successful, otherwise None.
        """
        counter = 0
        url = f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1"
        async with self.session:
            try:
                while counter < retries:
                    async with self.session.post(url) as response:
                        data = await response.json()
                        logger.info(f"Response status: {response.status}")
                        logger.info(f"Response text: {data}")
                        if response.status == 200:
                            return data
                        else:
                            counter += 1
                            await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return None
