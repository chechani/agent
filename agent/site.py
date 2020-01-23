from agent.base import Base
from agent.job import step
import os
import json


class Site(Base):
    def __init__(self, name, bench):
        self.name = name
        self.bench = bench
        self.directory = os.path.join(self.bench.sites_directory, name)
        self.config_file = os.path.join(self.directory, "site_config.json")
        if not (
            os.path.isdir(self.directory) and os.path.exists(self.config_file)
        ):
            raise Exception

    def bench_execute(self, command):
        return self.bench.execute(f"bench --site {self.name} {command}")

    @step("Install Apps")
    def install_apps(self, apps):
        for app in apps:
            if app != "frappe":
                self.bench_execute(f"install-app {app}")

    @step("Site Update Configuration")
    def update_config(self, value):
        new_config = self.config
        new_config.update(value)
        self.setconfig(new_config)

    def setconfig(self, value):
        with open(self.config_file, "w") as f:
            json.dump(value, f, indent=1, sort_keys=True)

    @property
    def job_record(self):
        return self.bench.server.job_record

    @property
    def step_record(self):
        return self.bench.server.step_record