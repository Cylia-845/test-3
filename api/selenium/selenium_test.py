from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Options pour exécuter Chrome sans interface graphique
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    # Accéder à l'application (tu peux adapter l'URL si elle tourne ailleurs)
    driver.get("http://localhost:5000")

    time.sleep(1)

    # Remplir les champs avec des valeurs
    driver.find_element(By.ID, "a").send_keys("3")
    driver.find_element(By.ID, "b").send_keys("7")

    # Cliquer sur le bouton pour envoyer
    driver.find_element(By.ID, "add-button").click()

    # Attendre que le résultat soit affiché
    time.sleep(1)

    result = driver.find_element(By.ID, "result").text
    print("Résultat affiché :", result)

    assert "Résultat : 10" in result or "Résultat : 10.0" in result
    
except Exception as e:
    print("Test échoué :", str(e))

finally:
    driver.quit()
