import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { Grid } from "@mui/material";
import ControlledTextField from "../../../shared/controlledInputComponents/ControlledTextField";
import { ETFormLabel, ETFormLabelWithCharacterLimit } from "../../../shared";
import { IssuesContext } from "../IssuesContext";
import { CloneForm } from "../types";
import { descriptionCharacterLimit } from "./constants";
import ControlledDatePicker from "components/shared/controlledInputComponents/ControlledDatePicker";

const schema = yup.object().shape({
  posted_date: yup.string().required("Date is required"),
  description: yup
    .string()
    .required("Description is required")
    .max(descriptionCharacterLimit),
});

const EditIssueUpdate = () => {
  const {
    setUpdateToClone,
    updateToEdit,
    editIssueUpdate,
    setEditIssueUpdateFormIsOpen,
  } = React.useContext(IssuesContext);

  const methods = useForm<CloneForm>({
    resolver: yupResolver(schema),
    defaultValues: {
      posted_date: updateToEdit?.posted_date,
      description: updateToEdit?.description,
    },
    mode: "onSubmit",
  });

  const { handleSubmit, watch } = methods;

  const watchedDescription = watch("description");

  const onSubmitHandler = async (data: CloneForm) => {
    const validData = await schema.validate(data);

    editIssueUpdate(validData);

    setEditIssueUpdateFormIsOpen(false);
    setUpdateToClone(null);
  };

  return (
    <FormProvider {...methods}>
      <Grid
        component={"form"}
        id="issue-form"
        spacing={2}
        container
        sx={{
          width: "100%",
        }}
        onSubmit={handleSubmit(onSubmitHandler)}
      >
        <Grid item xs={12} container>
          <Grid item xs={6}>
            <ETFormLabel required>Date</ETFormLabel>
            <ControlledDatePicker name="posted_date" />
          </Grid>
        </Grid>
        <Grid item xs={12}>
          <ETFormLabelWithCharacterLimit
            characterCount={watchedDescription.length}
            maxCharacterLength={descriptionCharacterLimit}
          >
            Description
          </ETFormLabelWithCharacterLimit>
          <ControlledTextField
            name="description"
            fullWidth
            size="small"
            inputProps={{
              maxLength: descriptionCharacterLimit,
            }}
            multiline
            rows={4}
          />
        </Grid>
      </Grid>
    </FormProvider>
  );
};

export default EditIssueUpdate;
