# True Alarm Report

## What happened

Acto inserted a dummy annotation `ACTOKEY: ACTOKEY` in `spec.metadata.annotation` field of the CR. This leads to a failure in the reconcilliation of the Postgres backup job.

## Root Cause

This change is picked up by [reconcileReplicatedCreateBackup](https://github.com/CrunchyData/postgres-operator/blob/master/internal/controller/postgrescluster/pgbackrest.go#L2335) which manages backup jobs. The new annotation entry is [further propagated](https://github.com/CrunchyData/postgres-operator/blob/master/internal/controller/postgrescluster/pgbackrest.go#L2485)  into the `spec.template.metadata.annotations` field of the backupjob. Since the controller always [tries to stick to an existing job name](https://github.com/CrunchyData/postgres-operator/blob/master/internal/controller/postgrescluster/pgbackrest.go#L2467), K8S Job Controller eventually sees an updated job template for an existing resource and complains about `spec.template: Invalid value core.PodTemplateSpec{...} field is immutable`.

## Expected Behavior

The backup job controller should either try to delete the existing job first or create a new job with a new name if modification to the job template is required.

## Other Alarms

Analysis on false alarms and Acto misoperations are included as additional columns in the result.csv file.
