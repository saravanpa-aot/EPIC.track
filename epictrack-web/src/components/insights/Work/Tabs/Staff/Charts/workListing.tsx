import React, { useEffect } from "react";
import { MRT_ColumnDef } from "material-react-table";
import { showNotification } from "components/shared/notificationProvider";
import { useAppSelector } from "hooks";
import { hasPermission } from "components/shared/restricted";
import { ROLES } from "constants/application-constant";
import { Work } from "models/work";
import {
  getSelectFilterOptions,
  rowsPerPageOptions,
} from "components/shared/MasterTrackTable/utils";
import { ETGridTitle } from "components/shared";
import { searchFilter } from "components/shared/MasterTrackTable/filters";
import TableFilter from "components/shared/filterSelect/TableFilter";
import { ActiveChip, InactiveChip } from "components/shared/chip/ETChip";
import MasterTrackTable from "components/shared/MasterTrackTable";
import { useGetWorksQuery } from "services/rtkQuery/insights";

const WorkList = () => {
  const [workTypes, setWorkTypes] = React.useState<string[]>([]);
  const [leads, setLeads] = React.useState<string[]>([]);
  const [teams, setTeams] = React.useState<string[]>([]);
  const [officers, setOfficers] = React.useState<string[]>([]);
  const [pagination, setPagination] = React.useState({
    pageIndex: 0,
    pageSize: 10,
  });

  const { roles } = useAppSelector((state) => state.user.userDetail);
  const canEdit = hasPermission({ roles, allowed: [ROLES.EDIT] });

  const { data, error, isLoading } = useGetWorksQuery();

  const works = data || [];

  useEffect(() => {
    setPagination((prev) => ({
      ...prev,
      pageSize: works.length,
    }));
  }, [works]);

  const codeTypes: { [x: string]: any } = {
    work_type: setWorkTypes,
    eao_team: setTeams,
    work_lead: setLeads,
    responsible_epd: setOfficers,
  };

  React.useEffect(() => {
    Object.keys(codeTypes).forEach((key: string) => {
      let accessor = "name";
      if (key == "work_lead" || key == "responsible_epd") {
        accessor = "full_name";
      }
      const codes = works
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        .map((w) => (w[key] ? w[key][accessor] : null))
        .filter(
          (ele, index, arr) => arr.findIndex((t) => t === ele) === index && ele
        );
      codeTypes[key](codes);
    });
  }, [works]);

  useEffect(() => {
    if (error) {
      showNotification("Error fetching works", { type: "error" });
    }
  }, [error]);

  const columns = React.useMemo<MRT_ColumnDef<Work>[]>(
    () => [
      {
        accessorKey: "title",
        header: "Name",
        size: 300,
        Cell: canEdit
          ? ({ row, renderedCellValue }) => (
              <ETGridTitle
                to="#"
                onClick={() => {
                  //TODO: Implement this
                  return;
                }}
                titleText={row.original.title}
              >
                {renderedCellValue}
              </ETGridTitle>
            )
          : undefined,
        sortingFn: "sortFn",
        filterFn: searchFilter,
      },
      {
        accessorKey: "eao_team.name",
        header: "Team",
        size: 200,
        filterVariant: "multi-select",
        filterSelectOptions: teams,
        Filter: ({ header, column }) => {
          return (
            <TableFilter
              isMulti
              header={header}
              column={column}
              variant="inline"
              name="rolesFilter"
            />
          );
        },
        filterFn: (row, id, filterValue) => {
          if (
            !filterValue.length ||
            filterValue.length > teams.length // select all is selected
          ) {
            return true;
          }

          const value: string = row.getValue(id) || "";

          return filterValue.includes(value);
        },
      },
      {
        accessorKey: "work_lead.full_name",
        header: "Lead",
        filterVariant: "multi-select",
        filterSelectOptions: leads,
        Filter: ({ header, column }) => {
          return (
            <TableFilter
              isMulti
              header={header}
              column={column}
              variant="inline"
              name="rolesFilter"
            />
          );
        },
        filterFn: (row, id, filterValue) => {
          if (
            !filterValue.length ||
            filterValue.length > leads.length // select all is selected
          ) {
            return true;
          }

          const value: string = row.getValue(id) || "";

          return filterValue.includes(value);
        },
      },
      {
        accessorKey: "responsible_epd.full_name",
        header: "Officer/Analyst",
        filterVariant: "multi-select",
        filterSelectOptions: officers,
        Filter: ({ header, column }) => {
          return (
            <TableFilter
              isMulti
              header={header}
              column={column}
              variant="inline"
              name="rolesFilter"
            />
          );
        },
        filterFn: (row, id, filterValue) => {
          if (
            !filterValue.length ||
            filterValue.length > officers.length // select all is selected
          ) {
            return true;
          }

          const value: string = row.getValue(id) || "";

          return filterValue.includes(value);
        },
      },
    ],
    [leads, teams, officers, workTypes]
  );
  return (
    <MasterTrackTable
      columns={columns}
      data={works}
      initialState={{
        sorting: [
          {
            id: "title",
            desc: false,
          },
        ],
      }}
      state={{
        isLoading: isLoading,
        showGlobalFilter: true,
        pagination: pagination,
      }}
      enablePagination
      muiPaginationProps={{
        rowsPerPageOptions: rowsPerPageOptions(works.length),
      }}
      onPaginationChange={setPagination}
    />
  );
};

export default WorkList;
