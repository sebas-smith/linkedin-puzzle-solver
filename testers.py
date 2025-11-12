from playwright.sync_api import sync_playwright
import getpass

username = getpass.getuser()
p = sync_playwright().start()
browser = p.chromium.launch_persistent_context(
    user_data_dir=rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data",
    args=["--profile-directory=Default"],
    channel='chrome',
    headless=False
)
print("Success!")