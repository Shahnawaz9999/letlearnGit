import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape articles
    articles = soup.find_all("article")
    article_data = [article.get_text() for article in articles]

    # Scrape links
    links = soup.find_all("a")
    link_data = [link["href"] for link in links]

    # Scrape products and prices (example)
    products = soup.find_all("div", class_="product")
    product_data = []
    for product in products:
        name = product.find("h2").text.strip()
        price = product.find("span", class_="price").text.strip()
        product_data.append({"name": name, "price": price})

    # Return scraped data
    return {
        "articles": article_data,
        "links": link_data,
        "products": product_data
    }

@app.route("/", methods=["GET", "POST"])
def scrape_web_app():
    if request.method == "POST":
        url = request.form["url"]
        scraped_data = scrape_website(url)

        # Save data to a file
        with open("scraped_data.txt", "w") as file:
            file.write(str(scraped_data))

        return "Scraping completed. Data saved to scraped_data.txt file."

    # Render the HTML form for entering the URL
    return """
        <form method="POST">
            <label for="url">Enter URL:</label>
            <input type="text" id="url" name="url">
            <input type="submit" value="Scrape">
        </form>
    """

if __name__ == "__main__":
    app.run()