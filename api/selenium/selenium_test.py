from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Options pour Chrome headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium"  # chemin vers Chromium

# Créer le WebDriver avec le chemin vers chromedriver
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

try:
    driver.get("http://tp3_api_container:5000")

    time.sleep(1)

    driver.find_element(By.ID, "a").send_keys("3")
    driver.find_element(By.ID, "b").send_keys("7")
    driver.find_element(By.ID, "add-button").click()

    time.sleep(1)
    result = driver.find_element(By.ID, "result").text
    print("Résultat affiché :", result)

    assert "Résultat : 10" in result or "Résultat : 10.0" in result

except Exception as e:
    print("Test échoué :", str(e))

finally:
    driver.quit()
