from aiohttp import web

from seo.database import transactional_session, db
from seo.models.meta_tags import MetaTags
from seo.controllers.base import BaseJsonApiController
from seo.logger import get_logger
import pandas as pd
import io
import json
import numpy as np

_logger = get_logger()


class MetaTagsApiController(BaseJsonApiController):
    """
    Example API Controller to demonstrate the out-of-the-box interaction between Aiohttp's request
    handlers and SQLAlchemy's declarative models, the async work is nicely wrapped in the database
    models functions using the `run_async` helper method which you can find at:
        `seo.background.run_async`
    """
    sep = ';'
    fields = ['slug', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = None

    async def create(self, request: web.Request) -> web.Response:
        post = await request.post()
        if not (file_csv := post.get("file_csv")):
            return self.write_error(400, "need file_csv")

        def to_dict(row):
            return json.dumps({f"{field}": getattr(row, field) for field in self.df.columns[3:]})

        self.df = pd.read_csv(io.BytesIO(file_csv.file.read()), sep=self.sep)

        # check required fields

        if list(self.df.columns[:3]) != self.fields:
            return self.write_error(400, f"need : {', '.join(self.fields)}")

        # check unique slug
        if not self.df.slug.is_unique:
            return self.write_error(400, f"field slug is not unique")

        # replace NaN on ""
        self.df.fillna('', inplace=True)
        self.df['data'] = self.df.apply(to_dict, axis=1)

        # drop all columns except *self.fields
        self.df.drop(self.df.columns[3:-1], axis=1, inplace=True)

        # check empty fields
        if is_null := [(row + 1, col) for row, col in zip(*np.where(self.df.applymap(lambda x: x == '')))]:
            return self.write_error(400, f"Set of data has empty fields : {is_null}")

        async with transactional_session() as session:
            await MetaTags.delete_all(session)
        self.df.to_sql(MetaTags.__tablename__, db.engine, method='multi', index_label="id", if_exists='append')
        return self.json_response(body={'status': 'success'}, status=201)

    async def get(self, request: web.Request) -> web.Response:
        """
        Return all entries of MetaTags in csv file
        """

        headers = {
            "Content-Disposition": f'attachment; filename="meta_tags.csv"'
        }
        async with transactional_session() as session:
            df = pd.read_sql_table(MetaTags.__tablename__, session.bind)

            if not df.empty:
                for key in df.at[0, 'data']:
                    df[key] = ''

                def to_self_field(row):
                    for key, value in row.data.items():
                        df.at[row.name, key] = value

                df.apply(to_self_field, axis=1)
                df.drop(['data', 'id'], axis=1, inplace=True)

                file_ = io.BytesIO()
                df.to_csv(file_, sep=self.sep, index=False)
                file_.seek(0)
                content = file_.getvalue()
            else:
                content = self.sep.join(self.fields)
            return web.Response(body=content, content_type="text/csv", charset="utf-8", headers=headers)

    async def get_by_slug(self, request: web.Request) -> web.Response:
        """
        Return a record of MetaTags by slug
        """

        slug = request.rel_url.query.get('slug')

        async with transactional_session() as session:
            record = await MetaTags.get_by_slug(slug, session)

            if not (record := record.first()):
                return self.write_error(404, "The requested example doesn't exist!")

            return self.json_response(body={})
