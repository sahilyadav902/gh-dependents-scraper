import requests
from bs4 import BeautifulSoup
import csv

def scrape_dependents(repo_url):
    dependents = []
    page=1
    while repo_url:
        print(f"Processing Page: {page}")
        page+=1
        response = requests.get(repo_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for repo_box in soup.find_all("div", class_="Box-row"):
            repo_data = {}
            username_tag = repo_box.find("a", attrs={"data-hovercard-type": "user"})
            repo_name_tag = repo_box.find("a", attrs={"data-hovercard-type": "repository"})
            star_fork_tags = repo_box.find_all("span", class_="color-fg-muted text-bold pl-3")
            if len(star_fork_tags) >= 2:
                stars_tag = star_fork_tags[0]
                forks_tag = star_fork_tags[1]
                if username_tag:
                    repo_data["Username"] = username_tag.get_text(strip=True)
                if repo_name_tag:
                    repo_data["Repository Name"] = repo_name_tag.get_text(strip=True)
                if stars_tag:
                    repo_data["Stars"] = stars_tag.get_text(strip=True)
                if forks_tag:
                    repo_data["Forks"] = forks_tag.get_text(strip=True)
                repo_data["Link"] = f"https://github.com{repo_name_tag['href']}"
                dependents.append(repo_data)
        next_page_link = soup.find("a", class_="BtnGroup-item", string="Next")
        if next_page_link:
            repo_url = next_page_link['href']
        else:
            repo_url = None    
    return dependents

def save_to_csv(data, filename):
    with open(filename, mode="w", newline="") as csv_file:
        fieldnames = ["Username", "Repository Name", "Stars", "Forks", "Link"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for repo in data:
            writer.writerow(repo)

def main():
    with open("repo_url.txt", "r") as file:
        repo_url = file.read().strip()
    full_repo_url = f"{repo_url}/network/dependents"
    dependents = scrape_dependents(full_repo_url)
    username, repo_name = repo_url.split("/")[-2:]
    csv_filename = f"{username}_{repo_name}.csv"
    save_to_csv(dependents, csv_filename)
    print(f"Data saved to {csv_filename}")

if __name__ == "__main__":
    main()
