import uuid

import sqlalchemy as sa
from sqlalchemy.orm import aliased

from src.app.common.repository import BaseRepository
from src.app.lca import models, schemas as sch, enum


class LCAComponentRepository(BaseRepository[models.LCAComponent, sch.LCAComponentCreateSch, sch.LCAComponentUpdateSch]):
    model = models.LCAComponent

    async def get_all_stmt(self):
        stmt = sa.select(self.model).where(self.model.parent_id.is_(None))
        return stmt.order_by(self.model.name.asc())

    async def get_all_hierarchy(self, lca_id: uuid.UUID, id: uuid.UUID = None, phase_id: int = None, level: int | str = None):
        filters = [self.model.lca_id == lca_id]
        if id is not None:
            filters.append(self.model.id == id)
        else:
            filters.append(self.model.parent_id.is_(None))
        if phase_id is not None:
            filters.append(self.model.phase_id == phase_id)
        hierarchy = sa.select(self.model, sa.literal(0).label("level")).filter(*filters).cte(name="hierarchy", recursive=True)
        parent = aliased(hierarchy, name="p")
        children = aliased(self.model, name="c")
        hierarchy = hierarchy.union_all(
            sa.select(children, (parent.c.level + 1).label("level")).filter(children.parent_id == parent.c.id)
        )
        stmt = sa.select(self.model, hierarchy.c.level).join(hierarchy, self.model.id == hierarchy.c.id)
        stmt = stmt.order_by(self.model.name.asc())
        query = await self.async_session.execute(stmt)
        items = query.unique().fetchall()

        def build_hierarchy(items: list):
            items_by_id = {item.id: item.__dict__ for item, level in items}
            root_items = []
            for item, level in items:
                if item.parent_id is None or item.id == id:
                    root_items.append(items_by_id[item.id])
                else:
                    parent = items_by_id.get(item.parent_id)
                    if parent:
                        if parent.get("components") is None:
                            parent["components"] = []
                        parent["components"].append(items_by_id[item.id])
            return root_items

        return build_hierarchy(items)

    async def create(self, *, obj_in: sch.LCAComponentCreateSch, lca_id: uuid.UUID) -> model:
        obj_in_dict = obj_in.model_dump()
        components = obj_in_dict.pop("components", [])
        obj_db = self.model(**obj_in_dict, lca_id=lca_id)
        self.async_session.add(obj_db)
        await self.async_session.flush()
        for component in obj_in.components:
            await self.create_child(
                obj_in=component, lca_id=lca_id, parent_id=obj_db.id, phase_id=obj_in.phase_id, unit=obj_in.unit
            )
        await self.async_session.commit()
        await self.async_session.refresh(obj_db)
        obj_db = await self.get_all_hierarchy(lca_id=obj_db.lca_id, id=obj_db.id)
        return obj_db[0]

    async def create_child(
        self,
        *,
        obj_in: sch.LCAComponentChildCreateSch,
        lca_id: uuid.UUID,
        parent_id: uuid.UUID,
        phase_id: int,
        unit: enum.UnitEnum,
    ) -> model:
        obj_in_dict = obj_in.model_dump()
        obj_in_dict["lca_id"] = lca_id
        obj_in_dict["parent_id"] = parent_id
        obj_in_dict["phase_id"] = phase_id
        obj_in_dict["unit"] = unit
        components = obj_in_dict.pop("components", [])
        obj_db = self.model(**obj_in_dict)
        self.async_session.add(obj_db)
        await self.async_session.flush()
        for component in obj_in.components:
            await self.create_child(obj_in=component, lca_id=lca_id, parent_id=obj_db.id, phase_id=obj_db.phase_id, unit=unit)
        return obj_db
