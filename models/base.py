from pymysql import IntegrityError
from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound
from flask_sqlalchemy import BaseQuery as QueryClass

from miniapp.corelibs.stone import db


class BaseQuery(QueryClass):

    def __iter__(self):
        return QueryClass.__iter__(self._undeleted())

    def from_self(self, *ent):
        return QueryClass.from_self(self._undeleted(), *ent)

    def _undeleted(self):
        mzero = self._mapper_zero()
        if mzero is not None and hasattr(mzero.class_, 'deleted'):
            cri = (mzero.class_.deleted == False)    # noqa
            return self.enable_assertions(False).filter(cri)
        else:
            return self

    def count(self):
        mzero = self._mapper_zero()
        if mzero is not None and hasattr(mzero.class_, 'id'):
            q = self._clone()
            q._set_entities(func.count(mzero.class_.id))
            if q._criterion is not None:
                q = q.filter(q._criterion)
            try:
                return q.scalar()
            except MultipleResultsFound:
                pass
        return super(BaseQuery, self).count()


class Base(db.Model):

    __abstract__ = True
    query_class = BaseQuery

    @classmethod
    def create(cls, _commit=True, **kwargs):
        obj = cls(**kwargs)
        obj.save(_commit)
        return obj

    def update(self, _commit=True, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save(_commit)
        return self

    @classmethod
    def get(cls, id, exclude_deleted=True):
        query = db.session.query(cls)
        if hasattr(cls, 'deleted') and exclude_deleted:
            query = query.filter_by(deleted=False)
        return query.filter_by(id=id).first()

    @classmethod
    def paginate(cls, page, per_page, order=None):
        return cls.query.order_by(order).paginate(page, per_page)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_multi(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).all()

    def to_dict(self):
        keys = [c.key for c in self.__table__.columns]
        return {k: getattr(self, k) for k in keys}

    def __repr__(self):
        attrs = ', '.join('{0}={1}'.format(repr(k), repr(v))
                          for k, v in self.to_dict().items())
        return '{0}({1})'.format(self.__class__.__name__, attrs)

    def save(self, _commit=True):
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

        _hooks = ('_clean_cache', '_before_save_hook')
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()

    def delete(self, _hard=False, _commit=True):
        soft_delete = hasattr(self, 'deleted') and _hard is False
        if soft_delete:
            self.deleted = True
            db.session.add(self)
        else:
            db.session.delete(self)
        if _commit:
            db.session.commit()

        if hasattr(self, '_point_mongo'):
            if soft_delete:
                self.delete_props_item()
            else:
                self._destory_props()

        _hooks = ('_clean_cache', '_before_delete_hook')
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()
