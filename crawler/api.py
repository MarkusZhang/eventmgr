from .models import Site
from .engine import CrawlerEngine

__all__=('scrape_info_from_all_sites',)

def scrape_info_from_all_sites():
    sites=Site.objects.filter(is_active=True)
    engine=CrawlerEngine(sites=sites)
    return engine.go_crawl()