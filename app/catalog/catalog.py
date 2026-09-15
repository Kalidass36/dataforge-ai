import json
from pathlib import Path

from app.catalog.builder import (
    CatalogBuilder,
)

from app.catalog.search import (
    CatalogSearch,
)


class DataCatalog:

    def __init__(self):

        self.catalog = None

    def build(self):

        builder = CatalogBuilder()

        self.catalog = builder.build()

        return self.catalog

    def search(self, query):

        if self.catalog is None:

            self.build()

        searcher = CatalogSearch(
            self.catalog
        )

        return searcher.search(
            query
        )

    def save(self, path="data/catalog.json"):

        if self.catalog is None:

            self.build()

        output_path = Path(path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.catalog,
                file,
                indent=2,
                default=str,
            )

        return str(output_path)

    def load(self, path="data/catalog.json"):

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            self.catalog = json.load(
                file
            )

        return self.catalog