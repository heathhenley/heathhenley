# Scrape blog xml feed and update readme with latest
import os
import requests
import xml.etree.ElementTree as ET


def xml_to_url(xml_str: str, number_of_posts: int) -> dict[str, str]:
    url_title_map = {}
    for idx, post in enumerate(ET.fromstring(xml_str)[0].iter('item')):
        url_title_map[post.find('link').text] = post.find('title').text
        if idx + 1 == number_of_posts:
            break
    return url_title_map


def get_blog_feed_xml(blog_feed_url: str) -> str:
    res = requests.get(blog_feed_url, timeout=10)
    if res.status_code != 200:
        print('Failed to scrape blog feed')
        raise RuntimeError('Failed to scrape blog feed')
    return res.content


def add_to_readme(url_title_map: dict[str, str], readme_name: str):
    readme = ''
    with open(readme_name, 'r') as f:
        for line in f.readlines():
          if not line.startswith("BLOG_POST_LIST"):
            readme += line
            continue
          for url, title in url_title_map.items():
              readme += '- [{}]({})\n'.format(title, url)
    with open('README.md', 'w') as f:
        f.write(readme)
    return


def main():
    blog_feed_url = os.getenv('BLOG_FEED_URL', None)
    number_of_posts = os.getenv('NUMBER_OF_POSTS', 10)
    readme_name = os.getenv('README_TEMPLATE_NAME', 'README_template.md')
    if not blog_feed_url:
        print('Please set the BLOG_FEED_URL environment variable')
        return
    print('Scraping blog feed from: {}'.format(blog_feed_url))
    print('Number of posts: {}'.format(number_of_posts))
    url_title_map = xml_to_url(
        get_blog_feed_xml(blog_feed_url), number_of_posts)
    add_to_readme(url_title_map, readme_name)



if __name__ == '__main__':
    main()
