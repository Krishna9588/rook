# Most probably we will get this details in our .csv file.
# Keep this just for an exception.
# info is the main function

from urllib.parse import urlparse



def info(url):
    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # Get the home link (scheme + netloc)
    home_link = f"{parsed.scheme}://{parsed.netloc}"

    # Extract company name from domain (netloc)
    domain = parsed.netloc.lower().replace("www.", "")
    parts = domain.split(".")

    # Try to guess company name from domain
    company_name = parts[0].title()

    return company_name

