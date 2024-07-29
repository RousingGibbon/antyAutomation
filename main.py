import asyncio
from playwright.async_api import async_playwright
from loguru import logger
from typing import Dict, Any, Optional
from api import api_key
from modules.SeedReader import SeedReader
from modules.ProfileManager import ProfileManager
from modules.MetamaskAutomator import MetaMaskAutomator

logger.add('debug.log', format='{time},{level},{message}', level='DEBUG')


async def unmain(profile: Dict[str, Any], seed: Optional[str], semaphore: asyncio.Semaphore) -> None:
    """
    Main function to perform tasks on a browser profile.

    Args:
        profile (Dict[str, Any]): The browser profile data.
        seed (Optional[str]): The seed phrase for the MetaMask account.
        semaphore (asyncio.Semaphore): The semaphore for controlling concurrency.
    """
    if not seed:
        logger.error("No seed phrase provided. Skipping...")
        return
    async with semaphore:
        automator = MetaMaskAutomator(seed, 'your_password')
        profile_manager = ProfileManager(api_key)

        async with async_playwright() as p:
            profile_id = profile.get('id')
            profile_data = await profile_manager.start_profile(profile_id)
            if not profile_data:
                logger.error(f"Failed to start profile {profile_id}. Skipping...")
                return
            automation = profile_data.get('automation')
            ws_endpoint = automation.get('wsEndpoint')
            port = automation.get('port')
            ws_endpoint = f"ws://127.0.0.1:{port}{ws_endpoint}"
            browser = await p.chromium.connect_over_cdp(ws_endpoint)
            context = browser.contexts[0]
            page = context.pages[0]
            await page.goto("chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#onboarding/welcome")
            await automator.login_metamask(page)



async def main() -> None:
    profile_manager = ProfileManager(api_key)
    profiles = await profile_manager.get_browser_profiles()
    seed_phrases = await SeedReader.read_seed_phrases('seed.txt')

    tasks = []
    semaphore = asyncio.Semaphore(6)
    for i, profile in enumerate(profiles):
        seed_phrase = seed_phrases[i] if i < len(seed_phrases) else None
        tasks.append(unmain(profile, seed_phrase, semaphore))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
