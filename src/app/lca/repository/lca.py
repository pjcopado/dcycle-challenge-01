import uuid
from collections import defaultdict

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import aliased

from src.app.common.repository import BaseRepository
from src.app.lca import models, schemas as sch


class LCARepository(BaseRepository[models.LCA, sch.LCACreateSch, sch.LCAUpdateSch]):
    model = models.LCA

    async def calculate_impact(self, id: uuid.UUID = None):
        filters = [models.LCAComponent.lca_id == id, models.LCAComponent.parent_id.is_(None)]

        hierarchy = (
            sa.select(models.LCAComponent, sa.literal(0).label("level")).filter(*filters).cte(name="hierarchy", recursive=True)
        )

        parent = aliased(hierarchy, name="p")
        children = aliased(models.LCAComponent, name="c")
        hierarchy = hierarchy.union_all(
            sa.select(children, (parent.c.level + 1).label("level")).filter(children.parent_id == parent.c.id)
        )

        stmt = (
            sa.select(
                models.PhaseGroup.sort_order.label("sort_order"),
                models.PhaseGroup.name.label("group_name"),
                models.Phase.code.label("phase_code"),
                models.Phase.name.label("phase_name"),
                hierarchy.c.level,
                models.LCAComponent.quantity,
                models.LCAComponent.unit,
                models.LCAComponent.source_id,
            )
            .join(hierarchy, models.LCAComponent.id == hierarchy.c.id)
            .join(models.Phase, models.LCAComponent.phase_id == models.Phase.id)
            .join(models.PhaseGroup, models.Phase.group_id == models.PhaseGroup.id)
        )

        stmt = stmt.order_by(models.LCAComponent.name.asc())

        def pandas_query(session):
            conn = session.connection()
            return pd.read_sql_query(stmt, conn)

        df = await self.async_session.run_sync(pandas_query)
        df = (
            df.groupby(["sort_order", "group_name", "phase_code", "phase_name", "unit", "source_id"])
            .agg({"quantity": "sum"})
            .reset_index()
        )

        # TODO falta aplicar impactos. cómo se calculan?

        impact_stmt = sa.select(
            models.Impact.source_id, models.Impact.category.label("impact_category"), models.Impact.value.label("impact_value")
        ).where(models.Impact.source_id.in_(df["source_id"].unique()))

        def pandas_query(session):
            conn = session.connection()
            return pd.read_sql_query(impact_stmt, conn)

        impact_df = await self.async_session.run_sync(pandas_query)
        # print(impact_df)

        ####

        df_dict = df.to_dict(orient="records")

        data = defaultdict(list)

        for item in df_dict:
            phase = {
                "code": item["phase_code"],
                "name": item["phase_name"],
                "quantity": item["quantity"],
                "unit": item["unit"],
                "impact": 0,  # TODO
                "impact_distribution": 0,  # TODO
            }
            data[item["group_name"]].append(phase)

        result = [{"name": group_name, "phases": phases} for group_name, phases in data.items()]

        return result
