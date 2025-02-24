import React, { useEffect, useState } from "react";
import WorkForm from "../WorkForm";
import TrackDialog from "components/shared/TrackDialog";
import { Work } from "models/work";
import workService from "services/workService/workService";
import { showNotification } from "components/shared/notificationProvider";

type WorkDialogProps = {
  open: boolean;
  setOpen: (open: boolean) => void;
  workId?: number;
  saveWorkCallback?: () => void;
};
export const WorkDialog = ({
  workId,
  open,
  setOpen,
  saveWorkCallback = () => {
    return;
  },
}: WorkDialogProps) => {
  const [work, setWork] = useState<Work | null>(null);
  const [disableSave, setDisableSave] = useState(false);

  const fetchWork = async () => {
    if (!workId) return;
    try {
      const response = await workService.getById(String(workId));
      setWork(response.data);
    } catch (error) {
      showNotification("Could not load Work", {
        type: "error",
      });
    }
  };

  const createWork = async (data: any) => {
    try {
      await workService.create(data);
      showNotification("Work created successfully", {
        type: "success",
      });
      setWork(null);
    } catch (error) {
      showNotification("Could not create Work", {
        type: "error",
      });
    }
  };

  const editWork = async (data: any) => {
    try {
      await workService.update(data, String(workId));
      showNotification("Work updated successfully", {
        type: "success",
      });
      setWork(null);
    } catch (error) {
      showNotification("Could not update Work", {
        type: "error",
      });
    }
  };

  const saveWork = async (data: any) => {
    if (workId) {
      await editWork(data);
    } else {
      await createWork(data);
    }
    setOpen(false);
    saveWorkCallback();
  };

  useEffect(() => {
    if (open) {
      fetchWork();
    }
  }, [open]);

  return (
    <TrackDialog
      open={open}
      dialogTitle={workId ? "Edit Work" : "Create Work"}
      onClose={() => {
        setWork(null);
        setOpen(false);
      }}
      disableEscapeKeyDown
      fullWidth
      maxWidth="lg"
      okButtonText="Save"
      cancelButtonText="Cancel"
      isActionsRequired
      onCancel={() => {
        setWork(null);
        setOpen(false);
      }}
      formId={"work-form"}
      saveButtonProps={{
        disabled: disableSave,
      }}
    >
      <WorkForm
        work={work}
        fetchWork={fetchWork}
        saveWork={saveWork}
        setDisableDialogSave={setDisableSave}
      />
    </TrackDialog>
  );
};
