# Template

## 1. Export selected products to excel

## 2. Get URL adresses of products

Shopetet doesn't allow me to export URL of products so I used python code [data-scraper-URLS.py](data-scraper-URLS.py), where I put there categories pages and code got URLS and titles of every product that was visible in those categories. Some products may be hidden. So add them manualy. I made the URLS in excel [template_generate_url](template_generate_url) (but not every URL is generated crrectly) so after that I used [check_url_status.py](check_url_status.py) to check if every URL is valid and replaced invalid manually.

## 3. Get URLs of images

From URLs I got in previous step I needed one image for reference. So I used [url_of_images.py](url_of_images.py) to load URLs from excel to get URL of main image of the product and write it to next column
