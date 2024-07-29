import asyncio
from playwright.async_api import Page
from loguru import logger


class MetaMaskAutomator:
    def __init__(self, seed_phrase: str, password: str):
        self.seed_phrase = seed_phrase
        self.password = password

    async def click_element(self, page: Page, selector: str, description: str) -> None:
        """
        Clicks an element on the page.

        Args:
            page (Page): The Playwright page object.
            selector (str): The CSS selector of the element to click.
            description (str): Description of the element for logging purposes.
        """
        try:
            element = await page.query_selector(selector)
            if element:
                await element.click()
                logger.info(f"Clicked on {description}.")
            else:
                logger.warning(f"{description} not found.")
        except Exception as e:
            logger.error(f"Error clicking on {description}: {e}")

    async def fill_input(self, page: Page, selector: str, value: str, description: str) -> None:
        """
        Fills an input field on the page.

        Args:
            page (Page): The Playwright page object.
            selector (str): The CSS selector of the input field.
            value (str): The value to fill in the input field.
            description (str): Description of the input field for logging purposes.
        """
        try:
            input_element = await page.query_selector(selector)
            if input_element:
                await input_element.fill(value)
                logger.info(f"Filled '{description}' with value.")
            else:
                logger.warning(f"{description} input not found.")
        except Exception as e:
            logger.error(f"Error filling '{description}': {e}")



    async def login_metamask(self, page: Page) -> None:
        """
        Performs the MetaMask login process.

        Args:
            page (Page): The Playwright page object.
        """
        # try:
        #     await page.goto('chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#unlock')
        #     await asyncio.sleep(1)
        #     if page.url == 'chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#unlock':
        #         logger.info("Trying to login in current account")
        #     password_fields = await page.query_selector_all('input[type="password"]')
        #     await password_fields[0].fill(self.password)
        #     await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > button', 'unlock button')
        # except Exception as e:
        #     logger.warning(e)

        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        await self.click_element(page, 'input[type="checkbox"]', "TextField 'I agree to MetaMask Terms of Use'")
        await asyncio.sleep(1)

        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > ul > li:nth-child(3) > button', "Import Wallet button")
        await asyncio.sleep(1)
        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div > button.button.btn--rounded.btn-secondary.btn--large', "Import Wallet button")
        await asyncio.sleep(1)

        words = self.seed_phrase.split()
        try:
            textareas = await page.query_selector_all('input[type="password"]')
            if textareas and len(textareas) >= len(words):
                for i, word in enumerate(words):
                    await textareas[i].fill(word)
                    logger.info(f"Filled word {i + 1}: {word}")

                await asyncio.sleep(1)
                await self.click_element(page, "#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.import-srp__actions > div > button", "Confirm Seed Phrase button")
            else:
                logger.warning("Not enough text areas found for seed phrase.")
        except Exception as e:
            logger.error(f"Error interacting with seed phrase fields: {e}")

        try:
            password_fields = await page.query_selector_all('input[type="password"]')
            if len(password_fields) >= 2:
                await password_fields[0].fill(self.password)
                await password_fields[1].fill(self.password)
                logger.info("Password and confirmation filled.")
            else:
                logger.warning("Not enough password fields found.")
        except Exception as e:
            logger.error(f"Error filling password fields: {e}")

        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > div.mm-box.mm-box--margin-top-4.mm-box--margin-bottom-4.mm-box--justify-content-space-between.mm-box--align-items-center > label > input', 'confirmation_btn')
        await asyncio.sleep(1)
        await self.click_element(page, "#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > button", "Import button")
        await asyncio.sleep(1)
        await self.click_element(page, "#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.box.creation-successful__actions.box--margin-top-6.box--flex-direction-row > button", "Done button")
        await asyncio.sleep(1)
        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button', 'next')
        await asyncio.sleep(1)
        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button', 'next')

        try:
            password_fields = await page.query_selector_all('input[type="password"]')
            if len(password_fields) >= 2:
                await password_fields[0].fill(self.password)
                await password_fields[1].fill(self.password)
                logger.info("Password and confirmation filled.")
            elif len(password_fields) == 1:
                await password_fields[0].fill(self.password)
            else:
                logger.warning("No password fields found.")
        except Exception as e:
            logger.error(f"Error filling password fields: {e}")

        await self.click_element(page, '#app-content > div > div.mm-box.main-container-wrapper > div > div > button', 'unlock button')