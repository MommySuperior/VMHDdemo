from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
import time
import random
import json

results = ["https://www.reddit.com/r/Denver/comments/kmwr0i/mental_health_help/", 
           "https://www.reddit.com/r/mentalhealth/comments/1ak3pod/what_is_mental_health/",
           "https://www.reddit.com/r/AskNYC/comments/1spp0na/inpatient_mental_health_facility_recommendations/",
           "https://www.reddit.com/r/neurodiversity/comments/ynbyol/what_is_mental_health_anyway/",
           "https://www.reddit.com/r/mentalhealth/comments/1jzxeqx/10_signs_of_good_mental_health/",
           "https://www.reddit.com/r/AskReddit/comments/102yppe/what_are_major_ways_to_improve_your_overall/",
           "https://www.reddit.com/r/Dallas/comments/1df8emh/free_mental_health_services/",
           "https://www.reddit.com/r/Austin/comments/1ad52bf/austin_mental_health_resources_that_are_free_or/",
           "https://www.reddit.com/r/mentalhealth/comments/175bv92/do_people_without_any_mental_health_issues/",
           "https://www.reddit.com/r/mentalhealth/comments/1gjetix/whats_something_you_wish_people_understood_more/",
           "https://www.reddit.com/r/explainlikeimfive/comments/1rhdq8p/eli5_why_do_mental_health_problems_usually_appear/",
           "https://www.reddit.com/r/SaltLakeCity/comments/1kffi1x/mental_health_clinics_i_can_check_myself_into/",
           "https://www.reddit.com/r/AskAnAmerican/comments/1s7tec8/how_is_mental_health_treated_in_your_area/",
           "https://www.reddit.com/r/AskLosAngeles/comments/1i4sy9f/where_can_i_get_immediate_mental_health_care/",
           "https://www.reddit.com/r/mentalhealth/comments/1oj4vg2/do_you_think_mental_health_can_be_fully_cured_not/",
           "https://www.reddit.com/r/sandiego/comments/1hbkcpx/i_need_helpresources_for_mental_health/",
           "https://www.reddit.com/r/mentalhealth/comments/1fgrrzl/what_has_helped_with_your_mental_health_the_most/",
           "https://www.reddit.com/r/mentalhealth/comments/160ljh2/what_is_the_difference_between_mental_illness_and/",
           "https://www.reddit.com/r/FortCollins/comments/1mhp3w2/mental_health_crisis_recommendations/",
           "https://www.reddit.com/r/mentalhealth/comments/1c1ua6p/its_all_mental_health_matters_until/"]

print(len(results), "URLs stored")

def scrape_web_content(results):

    d = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        )

        page = context.new_page()

        for url in results:
            try:
                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                d[url] = page.content()
                print(f"SUCCESS: {url}")
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"ERROR: {url}")
                print(e)

        browser.close()

    return d

scraped_results = scrape_web_content(results)

print("\nNumber of pages scraped:", len(scraped_results))

print("\nFirst URL:")
print(list(scraped_results.keys())[0])

print("\nFirst 1000 characters of HTML:")
print(scraped_results[list(scraped_results.keys())[0]][:1000])

def parse_reddit_content (results):
    for i, (url, content) in enumerate(results.items()):
        soup = BeautifulSoup(content, 'html.parser')
        header = soup.find("h1")
        post_container = soup.find("shreddit-post-text-body")
        post = None
        if post_container:
            post = post_container.find("div", {"slot": "text-body"})
        if not post:
            continue
        reddit_data = {
            "url" : url,
            "title" : header.get_text(strip=True) if header else None,
            "post" : post.get_text("\n", strip=True) if post else None
        }
    
        file_name = f"reddit_post_{i}"
        out = Path(__file__).parent.parent / "data" / "reddit_json_demo" / f"{file_name}.json"

        with open(out, "w", encoding="utf-8") as f:
            json.dump(reddit_data, f, ensure_ascii=False, indent=4)

parsed_results = parse_reddit_content(scraped_results)

# right now, "read more" is added after every post text. remove that.