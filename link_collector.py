import argparse
import requests
import re
import os
import sys


def collect_links(url, pattern):
    # Retrieve the web page content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return []

    # Extract the protocol and host from the main URL
    parsed_url = re.match(r"(https?://[^/]+)", url)
    if not parsed_url:
        print("Invalid URL format.")
        return []

    main_url = parsed_url.group(1)

    # Find all value matching in the '' or ""
    all_links = re.findall('\"(.*?)\"', response.text)
    all_links.append( re.findall("\'(.*?)\'", response.text) )    

    # Find all links matching the regex pattern
    correct_links = []
    for link in all_links:
      link = re.findall(pattern, str(link))
      if (len(link) >= 1):
        correct_links.extend(link)
        print(correct_links)
        print()

    print(correct_links)
    sys.exit()
    # flattened_arr = []
    # for sublist in arr1:
    #     flattened_arr.extend(sublist)

    # Append the main URL to links that don't have the protocol
    links = [main_url + link if not link.startswith(("http://", "https://")) else link for link in links]

    return links


def save_links_to_file(links):
    with open("links.txt", "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Website Link Collector")

    # Add the command line arguments
    parser.add_argument("-u", "--url", help="Main Website URL", required=True)
    parser.add_argument("-p", "--pattern", help="Regex Pattern", required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Collect links
    print("Collecting links from the main website...")
    links = collect_links(args.url, args.pattern)
    sys.exit()

    # Display the results
    if links:
        print(f"Found {len(links)} link(s) matching the regex pattern.")
        save_links_to_file(links)
        print("Saving the links to links.txt file.")
    else:
        print("No links found matching the regex pattern.")
        if os.path.exists("links.txt"):
            os.remove("links.txt")


if __name__ == "__main__":
    main()
