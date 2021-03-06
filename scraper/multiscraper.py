from scraper import JenkinsScraper
import itertools

# The multiscraper abstracts away multiple scrapers into acting like a single 
# While a single scraper can only have a single baseurl, the multiscraper will
# act as a single scraper with the same commands and handle deciding which scraper is chosen.


class MultiScraper(object):
    def __init__(self, *arg):
        assert(reduce(lambda x, y: type(x) == JenkinsScraper, arg))
        self.scrapers = arg

    def which_scraper(self, job):
        for scraper in self.scrapers:
            jobs = scraper.fetch_jobs()
            if job in jobs['current'] or job in jobs['legacy']:
                return scraper

    @property
    def is_offline(self):
        for scraper in self.scrapers:
            if scraper.is_offline:
                return True
        return False

    def get_local_builds(self, job):
        for scraper in self.scrapers:
                builds = scraper.get_local_builds(job)
                if builds == []:
                    continue
                return builds
        return []

    def fetch_jobs(self):
        jobs = [scraper.fetch_jobs() for scraper in self.scrapers]
        return reduce(lambda x, y: {'current': x['current']+y['current'], 'legacy': x['legacy']+y['legacy']}, jobs)

    def fetch_build_html(self, job, build):
        scraper = self.which_scraper(job)
        if not scraper:
            return False
        return scraper.fetch_build_html(job, build)

    def fetch_test_data(self, job, test_name):
        scraper = self.which_scraper(job)
        return scraper.fetch_test_data(job, test_name)

    def make_build_dict(self, job, build):
        scraper = self.which_scraper(job)
        return scraper.make_build_dict(job, build)

    def generate_build_cache(self):
        for scraper in self.scrapers:
            scraper.generate_build_cache()

    def fetch_all_job_reports(self):
        for scraper in self.scrapers:
            scraper.fetch_all_job_reports()

    def list_tests(self, job):
        scraper = self.which_scraper(job)
        return scraper.list_tests(job)

    def refresh_jobs(self):
        for scraper in self.scrapers:
            scraper.refresh_jobs()
