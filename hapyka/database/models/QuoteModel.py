from sqlalchemy import Column, Integer, DateTime, TEXT

from hapyka.database.db import Base
from hapyka.dictionaries.generic import QUOTE_TMPL


class QuoteModel(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    when_written = Column(DateTime, nullable=False)
    when_quoted = Column(DateTime, nullable=False)
    quoted_by_id = Column(Integer, nullable=False)
    quoted_by_text = Column(TEXT, nullable=False)
    written_by = Column(Integer, nullable=False)
    quote = Column(TEXT, nullable=False)

    def __repr__(self):
        return QUOTE_TMPL.format(self.when_written.strftime("%d.%m.%Y"), self.quote, self.quoted_by_text)
