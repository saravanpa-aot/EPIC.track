"""change in master data

Revision ID: 213ca6b67dcc
Revises: eacb66ae668b
Create Date: 2023-11-20 22:13:05.217287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table, text

# revision identifiers, used by Alembic.
revision = '213ca6b67dcc'
down_revision = 'eacb66ae668b'
branch_labels = None
depends_on = None

old_project_state_options = (
    "UNDER_EAC_ASSESSMENT",
    "UNDER_EXEMPTION_REQUEST",
    "UNDER_AMENDMENT",
    "UNDER_DISPUTE_RESOLUTION",
    "PRE_CONSTRUCTION",
    "CONSTRUCTION",
    "OPERATION",
    "CARE_AND_MAINTENANCE",
    "DECOMMISSION",
    "UNKNOWN",
)
new_project_state_options = sorted(old_project_state_options + ("CLOSED", "UNDER_DESIGNATION"))

old_project_state = sa.Enum(*old_project_state_options, name='projectstateenum')
new_project_state = sa.Enum(*new_project_state_options, name='projectstateenum')
tmp_project_state = sa.Enum(*new_project_state_options, name='_projectstateenum')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Create a tempoary "_project_state" type, convert and drop the "old" type
    tmp_project_state.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE projects ALTER COLUMN project_state TYPE _projectstateenum'
               ' USING project_state::text::_projectstateenum')
    op.execute('DROP TYPE projectstateenum CASCADE')
    # Create and convert to the "new" project_state type
    new_project_state.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE projects ALTER COLUMN project_state TYPE projectstateenum'
               ' USING project_state::text::projectstateenum')
    tmp_project_state.drop(op.get_bind(), checkfirst=False)

    with op.batch_alter_table("indigenous_nations", schema=None) as batch_op:
        batch_op.add_column(sa.Column("bcigid", sa.String(), nullable=True))
        batch_op.alter_column(
            "pip_link",
            existing_type=sa.TEXT(),
            type_=sa.String(),
            existing_nullable=True,
        )

    with op.batch_alter_table("indigenous_nations_history", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("bcigid", sa.String(), autoincrement=False, nullable=True)
        )
        batch_op.alter_column(
            "pip_link",
            existing_type=sa.TEXT(),
            type_=sa.String(),
            existing_nullable=True,
            autoincrement=False,
        )

    positions_table = table(
        "positions",
        column("id", sa.Integer),
        column("name", sa.String),
        column("sort_order", sa.Integer),
    )
    types_table = table(
        "types",
        column("id", sa.Integer),
        column("name", sa.String),
        column("short_name", sa.String),
        column("sort_order", sa.Integer),
    )
    sub_types_table = table(
        "sub_types",
        column("id", sa.Integer),
        column("name", sa.String),
        column("short_name", sa.String),
        column("sort_order", sa.Integer),
        column("type_id", sa.Integer),
    )
    regions_table = table(
        "regions",
        column("id", sa.Integer),
        column("name", sa.String),
        column("entity", sa.String),
        column("sort_order", sa.Integer),
    )

    positions = [
        {"name": "Minister", "sort_order": 1},
        {"name": "Associate Deputy Minister", "sort_order": 2},
        {"name": "ADM, EA Operations", "sort_order": 3},
        {"name": "OpsDiv Executive", "sort_order": 4},
        {"name": "Executive Project Director", "sort_order": 5},
        {"name": "Project Assessment Director", "sort_order": 6},
        {"name": "Project Assessment Officer", "sort_order": 7},
        {"name": "Project Analyst", "sort_order": 8},
        {"name": "PA/AA", "sort_order": 9},
        {"name": "IPE", "sort_order": 10},
        {"name": "HR", "sort_order": 11},
        {"name": "Other", "sort_order": 12},
    ]
    types = [
        {"short_name": "Energy", "name": "Energy - Electricity", "sort_order": 1},
        {
            "short_name": "O&G",
            "name": "Energy - Petroleum & Natural Gas",
            "sort_order": 2,
        },
        {"short_name": "Industry", "name": "Industrial", "sort_order": 3},
        {"short_name": "Mines", "name": "Mines", "sort_order": 4},
        {
            "short_name": "Resorts",
            "name": "Tourist Destination Resort",
            "sort_order": 5,
        },
        {"short_name": "Transport", "name": "Transportation", "sort_order": 6},
        {"short_name": "Waste", "name": "Waste Disposal", "sort_order": 7},
        {"short_name": "Water", "name": "Water Management", "sort_order": 8},
        {"short_name": "Other", "name": "Other", "sort_order": 9},
    ]

    sub_types = [
        {
            "short_name": "Plant",
            "type_id": "Energy - Electricity",
            "name": "Power Plants",
            "sort_order": 1,
        },
        {
            "short_name": "Lines",
            "type_id": "Energy - Electricity",
            "name": "Transmission Lines",
            "sort_order": 2,
        },
        {
            "short_name": "Storage",
            "type_id": "Energy - Petroleum & Natural Gas",
            "name": "Energy Storage Facilities",
            "sort_order": 3,
        },
        {
            "short_name": "Proccesing",
            "type_id": "Energy - Petroleum & Natural Gas",
            "name": "Natural Gas Processing Plants",
            "sort_order": 4,
        },
        {
            "short_name": "Offshore",
            "type_id": "Energy - Petroleum & Natural Gas",
            "name": "Offshore Oil or Gas Facilities",
            "sort_order": 5,
        },
        {
            "short_name": "Refinery",
            "type_id": "Energy - Petroleum & Natural Gas",
            "name": "Oil Refineries",
            "sort_order": 6,
        },
        {
            "short_name": "Pipeline",
            "type_id": "Energy - Petroleum & Natural Gas",
            "name": "Transmission Pipelines",
            "sort_order": 7,
        },
        {
            "short_name": "Forest",
            "type_id": "Industrial",
            "name": "Forest Products",
            "sort_order": 8,
        },
        {
            "short_name": "Non-Metallic",
            "type_id": "Industrial",
            "name": "Non-metallic Mineral Products",
            "sort_order": 9,
        },
        {
            "short_name": "Chemicals",
            "type_id": "Industrial",
            "name": "Organic & Inorganic Chemical",
            "sort_order": 10,
        },
        {
            "short_name": "Other",
            "type_id": "Industrial",
            "name": "Other Industries",
            "sort_order": 11,
        },
        {
            "short_name": "Metals",
            "type_id": "Industrial",
            "name": "Primary Metals",
            "sort_order": 12,
        },
        {
            "short_name": "Coal",
            "type_id": "Mines",
            "name": "Coal Mines",
            "sort_order": 13,
        },
        {
            "short_name": "Stone",
            "type_id": "Mines",
            "name": "Construction Stone & Industrial Mineral Quarries",
            "sort_order": 14,
        },
        {
            "short_name": "Mineral",
            "type_id": "Mines",
            "name": "Mineral Mines",
            "sort_order": 15,
        },
        {
            "short_name": "Offshore",
            "type_id": "Mines",
            "name": "Offshore Mines",
            "sort_order": 16,
        },
        {
            "short_name": "Placer",
            "type_id": "Mines",
            "name": "Placer Mineral Mines",
            "sort_order": 17,
        },
        {
            "short_name": "Gravel",
            "type_id": "Mines",
            "name": "Sand and Gravel Pits",
            "sort_order": 18,
        },
        {
            "short_name": "Golf",
            "type_id": "Tourist Destination Resort",
            "name": "Golf Resorts",
            "sort_order": 19,
        },
        {
            "short_name": "Marina",
            "type_id": "Tourist Destination Resort",
            "name": "Marina Resorts",
            "sort_order": 20,
        },
        {
            "short_name": "Resort",
            "type_id": "Tourist Destination Resort",
            "name": "Resort Developments",
            "sort_order": 21,
        },
        {
            "short_name": "Ski",
            "type_id": "Tourist Destination Resort",
            "name": "Ski Resorts",
            "sort_order": 22,
        },
        {
            "short_name": "Airport",
            "type_id": "Transportation",
            "name": "Airports",
            "sort_order": 23,
        },
        {
            "short_name": "Ferry",
            "type_id": "Transportation",
            "name": "Ferry Terminals",
            "sort_order": 24,
        },
        {
            "short_name": "Port",
            "type_id": "Transportation",
            "name": "Marine Ports",
            "sort_order": 25,
        },
        {
            "short_name": "Highway",
            "type_id": "Transportation",
            "name": "Public Highways",
            "sort_order": 26,
        },
        {
            "short_name": "Railway",
            "type_id": "Transportation",
            "name": "Railways",
            "sort_order": 27,
        },
        {
            "short_name": "Hazardous",
            "type_id": "Waste Disposal",
            "name": "Hazardous Waste Facilities",
            "sort_order": 28,
        },
        {
            "short_name": "Liquid",
            "type_id": "Waste Disposal",
            "name": "Local Government Liquid Waste Management Facilities",
            "sort_order": 29,
        },
        {
            "short_name": "Solid",
            "type_id": "Waste Disposal",
            "name": "Solid Waste Management Facilities",
            "sort_order": 30,
        },
        {
            "short_name": "Dams",
            "type_id": "Water Management",
            "name": "Dams",
            "sort_order": 31,
        },
        {
            "short_name": "Dikes",
            "type_id": "Water Management",
            "name": "Dikes",
            "sort_order": 32,
        },
        {
            "short_name": "Groundwater",
            "type_id": "Water Management",
            "name": "Groundwater Extraction",
            "sort_order": 33,
        },
        {
            "short_name": "Shoreline",
            "type_id": "Water Management",
            "name": "Shoreline Modification",
            "sort_order": 34,
        },
        {
            "short_name": "Diversion",
            "type_id": "Water Management",
            "name": "Water Diversion",
            "sort_order": 35,
        },
        {"short_name": "Other", "type_id": "Other", "name": "Other", "sort_order": 36},
    ]
    env_regions = [
        {"name": "Cariboo", "entity": "ENV", "sort_order": 1},
        {"name": "Kootenay", "entity": "ENV", "sort_order": 2},
        {"name": "Lower Mainland", "entity": "ENV", "sort_order": 3},
        {"name": "Okanagan", "entity": "ENV", "sort_order": 4},
        {"name": "Omineca", "entity": "ENV", "sort_order": 5},
        {"name": "Peace", "entity": "ENV", "sort_order": 6},
        {"name": "Skeena", "entity": "ENV", "sort_order": 7},
        {"name": "Thompson", "entity": "ENV", "sort_order": 8},
        {"name": "Vancouver Island", "entity": "ENV", "sort_order": 9},
    ]
    flnro_regions = [
        {"name": "Cariboo", "entity": "FLNR", "sort_order": 1},
        {"name": "Kootenay-Boundary", "entity": "FLNR", "sort_order": 2},
        {"name": "Northeast", "entity": "FLNR", "sort_order": 3},
        {"name": "Omineca", "entity": "FLNR", "sort_order": 4},
        {"name": "Skeena", "entity": "FLNR", "sort_order": 5},
        {"name": "South Coast", "entity": "FLNR", "sort_order": 6},
        {"name": "Thompson-Okanagan", "entity": "FLNR", "sort_order": 7},
        {"name": "West Coast", "entity": "FLNR", "sort_order": 8},
    ]
    conn = op.get_bind()

    for position in positions:
        position_sort_order = position.pop("sort_order")
        conditions = (
            f"WHERE {' AND '.join(map(lambda x: f'{x} = :{x}', position.keys()))} "
        )
        query = text(f"SELECT id from positions {conditions}")
        position_obj = conn.execute(query, position).fetchone()

        # moving this here because with old data may differ.
        position["sort_order"] = position_sort_order

        if position_obj is None:
            position_obj = conn.execute(
                positions_table.insert()
                .values(**position)
                .returning((positions_table.c.id).label("position_id"))
            )
        else:
            conn.execute(
                positions_table.update()
                .where(positions_table.c.id == position_obj.id)
                .values(**position)
            )
    for type_data in types:
        type_sort_order = type_data.pop("sort_order")
        conditions = (
            f"WHERE {' AND '.join(map(lambda x: f'{x} = :{x}', type_data.keys()))} "
        )
        query = text(f"SELECT id from types {conditions}")
        type_obj = conn.execute(query, type_data).fetchone()

        # moving this here because with old data may differ.
        type_data["sort_order"] = type_sort_order

        if type_obj is None:
            type_obj = conn.execute(
                types_table.insert()
                .values(**type_data)
                .returning((types_table.c.id).label("type_id"))
            )
        else:
            conn.execute(
                types_table.update()
                .where(types_table.c.id == type_obj.id)
                .values(**type_data)
            )
        for sub_type_data in sub_types:
            sub_type_sort_order = sub_type_data.pop("sort_order")
            sub_type_data.pop("type_id")
            conditions = f"WHERE {' AND '.join(map(lambda x: f'{x} = :{x}', sub_type_data.keys()))} "
            query = text(f"SELECT id from sub_types {conditions}")
            sub_type_obj = conn.execute(query, sub_type_data).fetchone()

            # moving this here because with old data may differ.
            sub_type_data["sort_order"] = sub_type_sort_order
            sub_type_data["type_id"] = type_obj.id

            if sub_type_obj is None:
                sub_type_obj = conn.execute(
                    sub_types_table.insert()
                    .values(**sub_type_data)
                    .returning((sub_types_table.c.id).label("sub_type_id"))
                )
            else:
                conn.execute(
                    sub_types_table.update()
                    .where(sub_types_table.c.id == sub_type_obj.id)
                    .values(**sub_type_data)
                )

    regions = env_regions + flnro_regions
    for region in regions:
        region_sort_order = region.pop("sort_order")
        conditions = (
            f"WHERE {' AND '.join(map(lambda x: f'{x} = :{x}', region.keys()))} "
        )
        query = text(f"SELECT id from regions {conditions}")
        region_obj = conn.execute(query, region).fetchone()

        # moving this here because with old data may differ.
        region["sort_order"] = region_sort_order

        if region_obj is None:
            region_obj = conn.execute(
                regions_table.insert()
                .values(**region)
                .returning((regions_table.c.id).label("region_id"))
            )
        else:
            conn.execute(
                regions_table.update()
                .where(regions_table.c.id == region_obj.id)
                .values(**region)
            )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    table = sa.sql.table('projects',
                   sa.Column('project_state', new_project_state, nullable=True))
    op.execute(table.update().where(table.c.project_state.in_(("CLOSED", "UNDER_DESIGNATION")))
               .values(project_state=None))
     # Create a tempoary "_project_state" type, convert and drop the "new" type
    tmp_project_state.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE projects ALTER COLUMN project_state TYPE _projectstateenum'
               ' USING project_state::text::_projectstateenum')
    op.execute('DROP TYPE projectstateenum CASCADE')
    # Create and convert to the "old" project_state type
    old_project_state.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE projects ALTER COLUMN project_state TYPE projectstateenum'
               ' USING project_state::text::projectstateenum')
    tmp_project_state.drop(op.get_bind(), checkfirst=False)
    with op.batch_alter_table("indigenous_nations_history", schema=None) as batch_op:
        batch_op.alter_column(
            "pip_link",
            existing_type=sa.String(),
            type_=sa.TEXT(),
            existing_nullable=True,
            autoincrement=False,
        )
        batch_op.drop_column("bcigid")

    with op.batch_alter_table("indigenous_nations", schema=None) as batch_op:
        batch_op.alter_column(
            "pip_link",
            existing_type=sa.String(),
            type_=sa.TEXT(),
            existing_nullable=True,
        )
        batch_op.drop_column("bcigid")
    # ### end Alembic commands ###
