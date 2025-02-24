import React from "react";
import { MRT_ColumnDef } from "material-react-table";
import { Box, Button, Grid } from "@mui/material";
import StaffForm from "./StaffForm";
import { Staff } from "../../models/staff";
import MasterTrackTable from "../shared/MasterTrackTable";
import { ETGridTitle, ETPageContainer } from "../shared";
import { MasterContext } from "../shared/MasterContext";
import staffService from "../../services/staffService/staffService";
import { ActiveChip, InactiveChip } from "../shared/chip/ETChip";
import TableFilter from "../shared/filterSelect/TableFilter";
import { getSelectFilterOptions } from "../shared/MasterTrackTable/utils";
import { Restricted, hasPermission } from "../shared/restricted";
import { ROLES } from "../../constants/application-constant";
import { searchFilter } from "../shared/MasterTrackTable/filters";
import { useAppSelector } from "../../hooks";

const StaffList = () => {
  const [staffId, setStaffId] = React.useState<number>();
  const [positions, setPositions] = React.useState<string[]>([]);
  const { roles } = useAppSelector((state) => state.user.userDetail);
  const ctx = React.useContext(MasterContext);

  React.useEffect(() => {
    ctx.setForm(<StaffForm staffId={staffId} />);
  }, [staffId]);

  const onEdit = (id: number) => {
    setStaffId(id);
    ctx.setShowModalForm(true);
  };

  React.useEffect(() => {
    ctx.setService(staffService);
  }, []);

  const staff = React.useMemo(() => ctx.data as Staff[], [ctx.data]);

  const statusesOptions = React.useMemo(
    () =>
      getSelectFilterOptions(
        staff,
        "is_active",
        (value) => (value ? "Active" : "Inactive"),
        (value) => value
      ),
    [staff]
  );

  React.useEffect(() => {
    if (staff) {
      const positions = staff
        .map((staff) => staff.position)
        .sort(
          (positionA, positionB) => positionA.sort_order - positionB.sort_order
        )
        .map((position) => position.name)
        .filter((ele, index, arr) => arr.findIndex((t) => t === ele) === index);
      setPositions(positions);
    }
  }, [staff]);

  const canEdit = hasPermission({ roles, allowed: [ROLES.EDIT] });

  const columns = React.useMemo<MRT_ColumnDef<Staff>[]>(
    () => [
      {
        accessorKey: "full_name",
        header: "Name",
        Cell: canEdit
          ? ({ cell, row, renderedCellValue }) => (
              <Restricted allowed={[ROLES.EDIT]} RenderError={undefined}>
                <ETGridTitle
                  to={"#"}
                  onClick={() => onEdit(row.original.id)}
                  enableTooltip={true}
                  tooltip={cell.getValue<string>()}
                >
                  {renderedCellValue}
                </ETGridTitle>
              </Restricted>
            )
          : undefined,
        sortingFn: "sortFn",
        filterFn: searchFilter,
      },
      {
        accessorKey: "phone",
        header: "Phone Number",
      },
      {
        accessorKey: "email",
        header: "Email",
      },
      {
        accessorKey: "position.name",
        header: "Position",
        filterVariant: "multi-select",
        Filter: ({ header, column }) => {
          return (
            <TableFilter
              isMulti
              header={header}
              column={column}
              variant="inline"
              name="positionsFilter"
            />
          );
        },
        filterSelectOptions: positions,
        filterFn: "multiSelectFilter",
      },
      {
        accessorKey: "is_active",
        header: "Status",
        filterVariant: "multi-select",
        filterSelectOptions: statusesOptions,
        size: 115,
        Filter: ({ header, column }) => {
          return (
            <Box sx={{ width: "100px" }}>
              <TableFilter
                isMulti
                header={header}
                column={column}
                variant="inline"
                name="rolesFilter"
              />
            </Box>
          );
        },
        filterFn: (row, id, filterValue) => {
          if (
            !filterValue.length ||
            filterValue.length > statusesOptions.length // select all is selected
          ) {
            return true;
          }

          const value: string = row.getValue(id);

          return filterValue.includes(value);
        },
        Cell: ({ cell }) => (
          <span>
            {cell.getValue<boolean>() && (
              <ActiveChip label="Active" color="primary" />
            )}
            {!cell.getValue<boolean>() && (
              <InactiveChip label="Inactive" color="error" />
            )}
          </span>
        ),
      },
    ],
    [positions]
  );
  return (
    <>
      <ETPageContainer
        direction="row"
        container
        columnSpacing={2}
        rowSpacing={3}
      >
        <Grid item xs={12}>
          <MasterTrackTable
            columns={columns}
            data={staff}
            initialState={{
              sorting: [
                {
                  id: "full_name",
                  desc: false,
                },
              ],
            }}
            state={{
              isLoading: ctx.loading,
              showGlobalFilter: true,
            }}
            renderTopToolbarCustomActions={() => (
              <Box
                sx={{
                  width: "100%",
                  display: "flex",
                  justifyContent: "right",
                }}
              >
                <Restricted
                  allowed={[ROLES.CREATE]}
                  errorProps={{ disabled: true }}
                >
                  <Button
                    variant="contained"
                    onClick={() => {
                      ctx.setShowModalForm(true);
                      setStaffId(undefined);
                    }}
                  >
                    Create Staff
                  </Button>
                </Restricted>
              </Box>
            )}
          />
        </Grid>
      </ETPageContainer>
    </>
  );
};

export default StaffList;
